#!/usr/bin/env python3
"""
forgesim_server.py — Headless MTG Forge 4-AI Pod Simulation Cluster Daemon
==========================================================================
Runs inside the `forgesim.chayde.lab` (CT 201 on pve06) Docker container (or locally).
Maintains a pool of Pre-Warmed JVM Worker processes (`ForgePodRunner -daemon`) that
keep MTG Forge's 32,500+ card database initialized in RAM so 10-to-20 game Commander
pod simulations execute in parallel with 0.0s JVM startup latency.

Features:
  - Pre-Warmed JVM Worker Pool with per-game timeout isolation & auto-healing
  - Stateless REST API (`POST /api/v1/simulate`) accepting raw `.dck` text payloads
  - Live Web Control Panel (`GET /`) showing worker states, job history, and update controls
  - Dual Self-Update Engine:
      1. Hot-Code Pull & Recompile (`POST /api/v1/update`) driven by `forgesim_cluster/version.json` in GitHub or workstation LAN push
      2. Full Container Image Upgrade (`POST /api/v1/upgrade-container`) via Watchtower HTTP API

IMPORTANT VERSIONING RULE:
  Whenever ANY change is made to `forgesim_server.py` or `ForgePodRunner.java`, you MUST
  bump the `"version"`, `"released"`, and `"changelog"` fields in `forgesim_cluster/version.json`
  (and `SERVICE_VERSION` below) so the cluster's `Check for Updates` mechanism detects the new release.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SERVICE_VERSION = "1.3.0"
START_TIME = time.time()


def find_java_binaries() -> Tuple[str, str]:
    """Locates java and javac binaries across Linux containers and Windows hosts."""
    java_home = os.environ.get("JAVA_HOME")
    if java_home:
        ext = ".exe" if os.name == "nt" else ""
        j_bin = Path(java_home) / "bin" / f"java{ext}"
        jc_bin = Path(java_home) / "bin" / f"javac{ext}"
        if j_bin.exists() and jc_bin.exists():
            return str(j_bin), str(jc_bin)

    if os.name == "nt":
        candidates = [
            Path(r"C:\Program Files\Eclipse Adoptium\jdk-17.0.19.10-hotspot\bin"),
            Path(r"C:\Program Files\Eclipse Adoptium\jdk-21\bin"),
            Path(r"C:\Program Files\Java\jdk-17\bin"),
        ]
        for c in candidates:
            if (c / "java.exe").exists() and (c / "javac.exe").exists():
                return str(c / "java.exe"), str(c / "javac.exe")

    java_cmd = shutil.which("java") or "java"
    javac_cmd = shutil.which("javac") or "javac"
    return java_cmd, javac_cmd


def find_forge_install() -> Tuple[Path, Path]:
    """Locates the MTG Forge installation directory and desktop jar."""
    env_dir = os.environ.get("FORGE_DIR")
    candidates = []
    if env_dir:
        candidates.append(Path(env_dir))
    candidates.extend([
        Path("/opt/forge"),
        Path("/app/forge"),
        Path(r"C:\forge-mtg"),
    ])
    for d in candidates:
        if d.exists():
            jars = sorted(d.glob("forge-gui-desktop-*-jar-with-dependencies.jar"))
            if jars:
                return d, jars[-1]
    raise FileNotFoundError("Could not locate MTG Forge installation directory or desktop jar.")


class WarmJvmWorker:
    """Manages a single persistent `ForgePodRunner -daemon` JVM process."""

    def __init__(
        self,
        worker_id: int,
        java_bin: str,
        forge_dir: Path,
        forge_jar: Path,
        bridge_dir: Path,
        heap_mb: int = 1536,
    ):
        self.worker_id = worker_id
        self.java_bin = java_bin
        self.forge_dir = forge_dir
        self.forge_jar = forge_jar
        self.bridge_dir = bridge_dir
        self.heap_mb = heap_mb

        self.proc: Optional[subprocess.Popen] = None
        self.lock = threading.Lock()
        self.start_lock = threading.Lock()
        self.status: str = "STOPPED"  # STOPPED, WARMING, IDLE, BUSY, ERROR
        self.games_completed: int = 0
        self.total_game_ms: int = 0
        self.current_job: Optional[str] = None
        self.job_started_at: Optional[float] = None
        self.aborted_by_user: bool = False
        self.abort_reason: Optional[str] = None
        self.needs_rewarm: bool = False
        self.last_active: float = time.time()
        self.booted_at: Optional[float] = None
        self.last_error: Optional[str] = None

    def start(self) -> bool:
        """Starts the JVM subprocess and waits until FORGE_DAEMON_READY is emitted (thread-safe & timeout-bounded)."""
        with self.start_lock:
            with self.lock:
                self._kill_locked()
                self.status = "WARMING"
                self.current_job = None
                self.job_started_at = None
                self.aborted_by_user = False
                self.abort_reason = None
                self.needs_rewarm = False
                self.last_error = None
                cp_sep = ";" if os.name == "nt" else ":"
                classpath = f"{self.bridge_dir}{cp_sep}{self.forge_jar}"
                cmd = [
                    self.java_bin,
                    f"-Xmx{self.heap_mb}m",
                    "-Djava.awt.headless=true",
                    "-Dsun.java2d.d3d=false",
                    "-cp",
                    classpath,
                    "ForgePodRunner",
                    "-daemon",
                ]
                try:
                    self.proc = subprocess.Popen(
                        cmd,
                        cwd=str(self.forge_dir),
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        bufsize=1,
                    )
                    proc_ref = self.proc
                except Exception as e:
                    self.status = "ERROR"
                    self.last_error = f"Spawn failed: {e}"
                    return False

            ready_event = threading.Event()
            warmup_state: Dict[str, Any] = {"ok": False, "err": None}

            def _wait_ready():
                try:
                    while True:
                        if proc_ref.poll() is not None:
                            warmup_state["err"] = f"JVM exited during warmup with code {proc_ref.returncode}"
                            break
                        line = proc_ref.stdout.readline()
                        if not line:
                            warmup_state["err"] = "EOF waiting for FORGE_DAEMON_READY"
                            break
                        if "FORGE_DAEMON_READY" in line:
                            warmup_state["ok"] = True
                            break
                except Exception as ex:
                    warmup_state["err"] = str(ex)
                finally:
                    ready_event.set()

            threading.Thread(target=_wait_ready, daemon=True).start()
            ready_event.wait(timeout=60)

            if warmup_state["ok"]:
                with self.lock:
                    self.status = "IDLE"
                    self.current_job = None
                    self.job_started_at = None
                    self.booted_at = time.time()
                    self.last_active = time.time()
                return True

            with self.lock:
                self._kill_locked()
                self.status = "ERROR"
                self.last_error = warmup_state["err"] or "Timed out waiting for FORGE_DAEMON_READY"
                return False

    def _kill_locked(self):
        if self.proc is not None:
            try:
                self.proc.kill()
                self.proc.wait(timeout=3)
            except Exception:
                pass
            self.proc = None
        self.status = "STOPPED"
        self.current_job = None
        self.job_started_at = None

    def stop(self):
        with self.lock:
            self._kill_locked()

    def abort_current_job(self, reason: str = "Skipped via Web UI") -> Dict[str, Any]:
        """Immediately aborts the currently running game on this worker and triggers a re-warm."""
        with self.lock:
            was_busy = (self.status == "BUSY")
            prev_job = self.current_job
            self.aborted_by_user = True
            self.abort_reason = reason
            self.needs_rewarm = True
            self._kill_locked()
            self.last_error = f"{reason} ({prev_job or 'worker reset'})"
        if not was_busy:
            threading.Thread(target=self.start, daemon=True).start()
        return {
            "success": True,
            "worker_id": self.worker_id,
            "was_busy": was_busy,
            "aborted_job": prev_job,
            "message": f"Worker #{self.worker_id} {'aborted ' + str(prev_job) + ' and is re-warming' if was_busy else 'is restarting'}.",
        }

    def run_single_game_job(self, job_payload: Dict[str, Any], hard_timeout_sec: int) -> Dict[str, Any]:
        """Sends a 1-game job JSON line to the warm JVM and reads TELEMETRY_GAME_JSON."""
        if self.proc is None or self.proc.poll() is not None or self.status != "IDLE":
            ok = self.start()
            if not ok:
                self.needs_rewarm = True
                return {
                    "game_index": job_payload.get("game_index_start", 1),
                    "seed": job_payload.get("base_seed", 0),
                    "timed_out": False,
                    "exception_occurred": True,
                    "error_message": self.last_error or "Worker failed to start",
                }

        with self.lock:
            self.status = "BUSY"
            self.aborted_by_user = False
            self.abort_reason = None
            self.needs_rewarm = False
            self.current_job = f"Game #{job_payload.get('game_index_start', 1)} ({job_payload.get('hero_name', 'Pod')})"
            self.job_started_at = time.time()
            self.last_active = time.time()
            proc_ref = self.proc

        result_holder: Dict[str, Any] = {}
        done_event = threading.Event()

        def _reader_target():
            game_json: Optional[Dict[str, Any]] = None
            try:
                line_str = json.dumps(job_payload) + "\n"
                proc_ref.stdin.write(line_str)
                proc_ref.stdin.flush()

                while True:
                    line = proc_ref.stdout.readline()
                    if not line:
                        result_holder["error"] = "Worker EOF during simulation"
                        break
                    line = line.strip()
                    if line.startswith("TELEMETRY_GAME_JSON:"):
                        raw = line[len("TELEMETRY_GAME_JSON:"):].strip()
                        game_json = json.loads(raw)
                    elif line.startswith("FORGE_JOB_DONE:"):
                        break
                    elif line.startswith("FORGE_JOB_ERROR:"):
                        raw = line[len("FORGE_JOB_ERROR:"):].strip()
                        err_obj = json.loads(raw)
                        result_holder["error"] = err_obj.get("error", "Unknown job error")
                        break
            except Exception as ex:
                result_holder["error"] = str(ex)
            if game_json is not None:
                result_holder["telemetry"] = game_json
            done_event.set()

        reader_thread = threading.Thread(target=_reader_target, daemon=True)
        reader_thread.start()

        finished = done_event.wait(timeout=hard_timeout_sec)
        elapsed_ms = int((time.time() - (self.job_started_at or time.time())) * 1000)

        if self.aborted_by_user:
            reason = self.abort_reason or "Manually skipped via Web UI"
            with self.lock:
                self._kill_locked()
                self.needs_rewarm = True
                self.last_error = reason
            return {
                "game_index": job_payload.get("game_index_start", 1),
                "seed": job_payload.get("base_seed", 0),
                "duration_ms": elapsed_ms,
                "timed_out": True,
                "exception_occurred": False,
                "error_message": reason,
                "winner_player": "DRAW (Skipped via Web UI)",
                "winner_deck": "DRAW (Skipped via Web UI)",
                "winner_seat": 0,
                "win_reason": reason,
                "hero_deck": job_payload.get("hero_name", "Hero"),
                "seats": [],
            }

        if not finished:
            # Hard hang inside Forge engine — kill and mark for re-warm before returning to pool
            with self.lock:
                self._kill_locked()
                self.needs_rewarm = True
                self.last_error = f"Hard timeout ({hard_timeout_sec}s) exceeded; recycling worker"
            return {
                "game_index": job_payload.get("game_index_start", 1),
                "seed": job_payload.get("base_seed", 0),
                "duration_ms": hard_timeout_sec * 1000,
                "timed_out": True,
                "exception_occurred": False,
                "error_message": f"Worker hard timeout ({hard_timeout_sec}s)",
                "winner_player": "DRAW (Clock Timeout)",
                "winner_deck": "DRAW (Clock Timeout)",
                "winner_seat": 0,
                "win_reason": f"Worker Hard Timeout ({hard_timeout_sec}s)",
                "hero_deck": job_payload.get("hero_name", "Hero"),
                "seats": [],
            }

        if "telemetry" in result_holder:
            telem = result_holder["telemetry"]
            with self.lock:
                self.status = "IDLE"
                self.current_job = None
                self.job_started_at = None
                self.games_completed += 1
                self.total_game_ms += int(telem.get("duration_ms", 0))
                self.last_active = time.time()
            return telem

        # If error occurred without telemetry, mark for re-warm before returning to pool
        err_msg = result_holder.get("error", "Unknown worker error")
        with self.lock:
            self._kill_locked()
            self.needs_rewarm = True
            self.last_error = err_msg
        return {
            "game_index": job_payload.get("game_index_start", 1),
            "seed": job_payload.get("base_seed", 0),
            "duration_ms": elapsed_ms,
            "timed_out": False,
            "exception_occurred": True,
            "error_message": err_msg,
            "winner_player": "ERROR",
            "winner_deck": "ERROR",
            "winner_seat": 0,
            "win_reason": err_msg,
            "hero_deck": job_payload.get("hero_name", "Hero"),
            "seats": [],
        }

    def snapshot(self) -> Dict[str, Any]:
        avg_ms = round(self.total_game_ms / self.games_completed) if self.games_completed > 0 else 0
        uptime_s = round(time.time() - self.booted_at) if self.booted_at and self.status in ("IDLE", "BUSY") else 0
        job_elapsed_s = round(time.time() - self.job_started_at) if (self.status == "BUSY" and self.job_started_at) else 0
        return {
            "worker_id": self.worker_id,
            "pid": self.proc.pid if (self.proc and self.proc.poll() is None) else None,
            "status": self.status,
            "games_completed": self.games_completed,
            "avg_game_ms": avg_ms,
            "current_job": self.current_job if self.status == "BUSY" else None,
            "job_elapsed_sec": job_elapsed_s,
            "uptime_sec": uptime_s,
            "last_error": self.last_error,
        }


class ForgeSimClusterCoordinator:
    """Manages compilation, warm worker pool, simulation job dispatch, and self-updating."""

    def __init__(
        self,
        num_workers: int,
        heap_mb: int,
        forge_dir: Path,
        forge_jar: Path,
        java_source: Path,
        bridge_dir: Path,
    ):
        self.num_workers = num_workers
        self.heap_mb = heap_mb
        self.forge_dir = forge_dir
        self.forge_jar = forge_jar
        self.java_source = java_source
        self.bridge_dir = bridge_dir
        self.java_bin, self.javac_bin = find_java_binaries()

        self.workers: List[WarmJvmWorker] = []
        self.pool_lock = threading.Lock()
        self.idle_workers: "queue.Queue[WarmJvmWorker]" = queue.Queue()
        self.job_history: List[Dict[str, Any]] = []
        self.active_batch: Optional[Dict[str, Any]] = None
        self.cancel_batch_requested: bool = False
        self.total_batches_run = 0
        self.total_games_run = 0

        self.compile_bridge()
        self._init_workers()

    def compile_bridge(self) -> Tuple[bool, str]:
        """Compiles ForgePodRunner.java into bridge_dir."""
        self.bridge_dir.mkdir(parents=True, exist_ok=True)
        cmd = [
            self.javac_bin,
            "--release",
            "17",
            "-cp",
            str(self.forge_jar),
            "-d",
            str(self.bridge_dir),
            str(self.java_source),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            msg = f"javac failed: {res.stderr.strip()}"
            print(f"[ERROR] {msg}", file=sys.stderr)
            return False, msg
        print(f"[OK] Compiled {self.java_source.name} -> {self.bridge_dir}")
        return True, "Compiled ForgePodRunner.java successfully."

    def _init_workers(self):
        print(f"[*] Bootstrapping {self.num_workers} Pre-Warmed JVM Workers (Heap: {self.heap_mb}MB each)...")
        for i in range(1, self.num_workers + 1):
            w = WarmJvmWorker(
                worker_id=i,
                java_bin=self.java_bin,
                forge_dir=self.forge_dir,
                forge_jar=self.forge_jar,
                bridge_dir=self.bridge_dir,
                heap_mb=self.heap_mb,
            )
            self.workers.append(w)

        def _warm_single(worker: WarmJvmWorker):
            if worker.start():
                print(f"  [+] Worker #{worker.worker_id} (PID {worker.proc.pid}) is WARM and IDLE.")
                self.idle_workers.put(worker)
            else:
                print(f"  [-] Worker #{worker.worker_id} failed warmup: {worker.last_error}", file=sys.stderr)
                self.idle_workers.put(worker)

        threads = [threading.Thread(target=_warm_single, args=(w,), daemon=True) for w in self.workers]
        for t in threads:
            t.start()

    def recycle_workers(self) -> Dict[str, Any]:
        """Gracefully restarts all warm JVM workers (used after hot-recompiling ForgePodRunner.java)."""
        print("[*] Recycling all Pre-Warmed JVM Workers...")
        # Drain queue
        while not self.idle_workers.empty():
            try:
                self.idle_workers.get_nowait()
            except queue.Empty:
                break

        def _restart(w: WarmJvmWorker):
            w.stop()
            w.start()
            self.idle_workers.put(w)

        threads = [threading.Thread(target=_restart, args=(w,), daemon=True) for w in self.workers]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=65)

        ready_count = sum(1 for w in self.workers if w.status == "IDLE")
        return {"success": True, "workers_ready": ready_count, "total_workers": len(self.workers)}

    def kill_worker_job(self, worker_id: int, reason: str = "Skipped via Web UI") -> Dict[str, Any]:
        """Aborts a stuck/slow game on a specific worker (1-indexed) and re-warms that worker."""
        target = next((w for w in self.workers if w.worker_id == worker_id), None)
        if not target:
            return {"success": False, "message": f"Worker #{worker_id} not found."}
        return target.abort_current_job(reason=reason)

    def cancel_active_batch(self) -> Dict[str, Any]:
        """Cancels any remaining queued games in the active batch and aborts currently running games."""
        with self.pool_lock:
            if not self.active_batch:
                return {"success": False, "message": "No simulation batch is currently running."}
            self.cancel_batch_requested = True
            b_id = self.active_batch.get("batch_id", "?")
        aborted = 0
        for w in self.workers:
            if w.status == "BUSY":
                w.abort_current_job(reason="Batch cancelled via Web UI")
                aborted += 1
        return {
            "success": True,
            "message": f"Cancelled active batch {b_id} and aborted {aborted} in-flight worker games.",
        }

    def run_pod_simulation(self, req_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fans out `games` simulations across the warm JVM worker pool in parallel.
        Expects `req_data`:
          {
            "decks": [{"name": "Obeka", "dck_content": "..."}, ...], # 4 seats
            "games": 10,
            "timeout": 90,
            "ai_timeout": 2,
            "smart_mulligan": false,
            "seed": null
          }
        """
        t0 = time.time()
        decks = req_data.get("decks", [])
        if len(decks) < 2:
            raise ValueError("Request must include at least 2 decks in 'decks' array.")

        num_games = max(1, min(200, int(req_data.get("games", 4))))
        timeout_sec = max(15, min(600, int(req_data.get("timeout", 150))))
        ai_timeout_sec = max(1, min(30, int(req_data.get("ai_timeout", 2))))
        smart_mulligan = bool(req_data.get("smart_mulligan", False))
        base_seed = req_data.get("seed")
        hero_name = decks[0].get("name", "Hero")
        opp_names = [d.get("name", "?") for d in decks[1:]]

        batch_id = str(uuid.uuid4())[:8]
        results: List[Optional[Dict[str, Any]]] = [None] * num_games

        # Task queue for auto-requeue on timeout/skip (max 2 retries per game slot)
        task_q: "queue.Queue[Dict[str, Any]]" = queue.Queue()
        for i in range(1, num_games + 1):
            seed_val = (int(base_seed) + i - 1) if base_seed is not None else int(time.time_ns() + i * 100003)
            task_q.put({"slot": i, "attempt": 1, "seed": seed_val})

        with self.pool_lock:
            self.cancel_batch_requested = False
            self.active_batch = {
                "batch_id": batch_id,
                "hero_deck": hero_name,
                "opponents": opp_names,
                "games_total": num_games,
                "games_completed": 0,
                "hero_wins": 0,
                "timeouts": 0,
                "requeued_games": 0,
                "timeout_sec": timeout_sec,
                "started_at": t0,
            }

        def _rewarm_and_return(w: WarmJvmWorker):
            w.start()
            self.idle_workers.put(w)

        def _worker_consumer():
            while True:
                if self.cancel_batch_requested:
                    break
                try:
                    task = task_q.get_nowait()
                except queue.Empty:
                    break

                slot = task["slot"]
                attempt = task["attempt"]
                seed_val = task["seed"]

                worker = self.idle_workers.get()
                try:
                    if self.cancel_batch_requested:
                        task_q.task_done()
                        break

                    job_payload = {
                        "job_id": f"{batch_id}-g{slot}-a{attempt}",
                        "hero_name": hero_name,
                        "decks": decks,
                        "num_games": 1,
                        "game_index_start": slot,
                        "timeout_sec": timeout_sec,
                        "ai_timeout_sec": ai_timeout_sec,
                        "base_seed": seed_val,
                        "smart_mulligan": smart_mulligan,
                    }
                    telem = worker.run_single_game_job(job_payload, hard_timeout_sec=timeout_sec + 20)
                    telem["game_index"] = slot
                    telem["worker_id"] = worker.worker_id

                    # Check if game timed out or was skipped and qualifies for re-queue (max 2 retries)
                    if (telem.get("timed_out") or telem.get("exception_occurred")) and attempt < 3 and not self.cancel_batch_requested:
                        new_seed = int(time.time_ns() ^ (slot * 104729) ^ (attempt * 7919))
                        print(f"[*] Game #{slot} timed out/skipped (attempt {attempt}). Auto-requeuing with new seed {new_seed}...")
                        with self.pool_lock:
                            if self.active_batch:
                                self.active_batch["timeouts"] += 1
                                self.active_batch["requeued_games"] += 1
                        task_q.put({"slot": slot, "attempt": attempt + 1, "seed": new_seed})
                    else:
                        # Completed definitively (or exhausted 2 retries)
                        results[slot - 1] = telem
                        with self.pool_lock:
                            if self.active_batch:
                                self.active_batch["games_completed"] += 1
                                if telem.get("winner_seat") == 1:
                                    self.active_batch["hero_wins"] += 1
                                if telem.get("timed_out"):
                                    self.active_batch["timeouts"] += 1
                finally:
                    task_q.task_done()
                    if worker.needs_rewarm or worker.status != "IDLE":
                        threading.Thread(target=_rewarm_and_return, args=(worker,), daemon=True).start()
                    else:
                        self.idle_workers.put(worker)

        consumer_threads = [threading.Thread(target=_worker_consumer, daemon=True) for _ in range(len(self.workers))]
        for ct in consumer_threads:
            ct.start()
        task_q.join()
        for ct in consumer_threads:
            ct.join()

        wall_sec = round(time.time() - t0, 2)
        clean_games = [r for r in results if r is not None]
        wins = sum(1 for g in clean_games if g.get("winner_seat") == 1)

        with self.pool_lock:
            self.active_batch = None
            self.cancel_batch_requested = False
            self.total_batches_run += 1
            self.total_games_run += len(clean_games)
            timeouts_count = sum(1 for g in clean_games if g.get("timed_out"))
            self.job_history.insert(0, {
                "batch_id": batch_id,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "hero_deck": hero_name,
                "opponents": opp_names,
                "games": len(clean_games),
                "hero_wins": wins,
                "win_rate_pct": round(wins / max(1, len(clean_games)) * 100, 1),
                "timeouts": timeouts_count,
                "requeued_games": getattr(self, "_last_requeued", 0),
                "wall_sec": wall_sec,
                "avg_sec_per_game": round(wall_sec / max(1, len(clean_games)), 2),
            })
            if len(self.job_history) > 30:
                self.job_history = self.job_history[:30]

        return {
            "status": "ok",
            "batch_id": batch_id,
            "wall_clock_sec": wall_sec,
            "games_completed": len(clean_games),
            "games": clean_games,
        }

    def get_version_info(self) -> Dict[str, Any]:
        here = Path(__file__).resolve().parent
        manifest_file = here / "version.json"
        if not manifest_file.exists() and (here.parent / "forgesim_cluster" / "version.json").exists():
            manifest_file = here.parent / "forgesim_cluster" / "version.json"

        local_ver = SERVICE_VERSION
        released = ""
        changelog = ""
        if manifest_file.exists():
            try:
                mdata = json.loads(manifest_file.read_text(encoding="utf-8"))
                local_ver = str(mdata.get("version") or SERVICE_VERSION).strip()
                released = str(mdata.get("released") or "").strip()
                changelog = str(mdata.get("changelog") or "").strip()
            except Exception:
                pass

        commit_file = here / "commit.txt"
        local_commit = commit_file.read_text(encoding="utf-8").strip() if commit_file.exists() else ""
        if not local_commit:
            try:
                res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(here), capture_output=True, text=True, timeout=3)
                if res.returncode == 0:
                    local_commit = res.stdout.strip()
            except Exception:
                pass

        java_sha = ""
        if self.java_source.exists():
            java_sha = hashlib.sha256(self.java_source.read_bytes()).hexdigest()[:12]
        server_sha = hashlib.sha256(Path(__file__).resolve().read_bytes()).hexdigest()[:12]
        return {
            "service": "forgesim-cluster",
            "version": local_ver,
            "released": released,
            "changelog": changelog,
            "local_commit": local_commit[:7] if local_commit else f"v{local_ver}",
            "local_commit_full": local_commit,
            "java_bridge_sha": java_sha,
            "server_sha": server_sha,
            "forge_jar": self.forge_jar.name,
            "uptime_sec": round(time.time() - START_TIME),
        }

    def get_status(self) -> Dict[str, Any]:
        worker_snaps = [w.snapshot() for w in self.workers]
        idle_c = sum(1 for w in worker_snaps if w["status"] == "IDLE")
        busy_c = sum(1 for w in worker_snaps if w["status"] == "BUSY")
        warming_c = sum(1 for w in worker_snaps if w["status"] == "WARMING")
        ver = self.get_version_info()
        active_b = None
        with self.pool_lock:
            if self.active_batch:
                elapsed_s = round(time.time() - self.active_batch["started_at"], 1)
                gt = max(1, self.active_batch["games_total"])
                gc = self.active_batch["games_completed"]
                active_b = {
                    **self.active_batch,
                    "elapsed_sec": elapsed_s,
                    "pct_complete": round(100.0 * gc / gt, 1),
                }
        return {
            **ver,
            "workers_total": len(self.workers),
            "workers_idle": idle_c,
            "workers_busy": busy_c,
            "workers_warming": warming_c,
            "total_batches_run": self.total_batches_run,
            "total_games_run": self.total_games_run,
            "active_batch": active_b,
            "workers": worker_snaps,
            "recent_jobs": self.job_history[:10],
        }


COORDINATOR: Optional[ForgeSimClusterCoordinator] = None


def _parse_semver(ver_str: str) -> Tuple[int, ...]:
    """Parses a semantic version string like '1.2.3' into a comparable integer tuple."""
    cleaned = ver_str.strip().lstrip("vV").split("-")[0]
    parts = []
    for p in cleaned.split("."):
        try:
            parts.append(int(p))
        except ValueError:
            parts.append(0)
    return tuple(parts) if parts else (0, 0, 0)


def _fetch_github_file(owner: str, repo: str, branch: str, path: str, headers: Dict[str, str]) -> str:
    """Downloads a UTF-8 file from GitHub Contents API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
        return base64.b64decode(payload["content"]).decode("utf-8")


def check_github_for_updates() -> Dict[str, Any]:
    """
    Checks `forgesim_cluster/version.json` in `chayde/mtg-deck-collection` on GitHub
    and compares the manifest version against the running service version.
    Commits to decks or unrelated files do NOT trigger false update notifications.
    """
    owner = os.environ.get("GITHUB_OWNER", "chayde")
    repo = os.environ.get("GITHUB_REPO", "mtg-deck-collection")
    branch = os.environ.get("GITHUB_BRANCH", "master")
    token = os.environ.get("GITHUB_PAT", "").strip()

    ver = COORDINATOR.get_version_info() if COORDINATOR else {}
    local_version = ver.get("version", SERVICE_VERSION)

    headers = {"User-Agent": "forgesim-cluster-daemon"}
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        raw_manifest = _fetch_github_file(owner, repo, branch, "forgesim_cluster/version.json", headers)
        remote_manifest = json.loads(raw_manifest)
        remote_version = str(remote_manifest.get("version", "")).strip()
        remote_released = str(remote_manifest.get("released", "")).strip()
        remote_changelog = str(remote_manifest.get("changelog", "")).strip()

        update_available = bool(
            remote_version
            and (
                _parse_semver(remote_version) > _parse_semver(local_version)
                or remote_version != local_version
            )
        )
        return {
            "updateAvailable": update_available,
            "localVersion": local_version,
            "remoteVersion": remote_version or "unknown",
            "released": remote_released,
            "changelog": remote_changelog,
            # Backwards-compatible aliases for older CLI/UI callers:
            "localCommit": f"v{local_version}",
            "remoteCommit": f"v{remote_version}" if remote_version else "unknown",
            "latestCommitMsg": remote_changelog,
            "latestCommitDate": remote_released,
            "repo": f"{owner}/{repo}@{branch}",
        }
    except Exception as e:
        return {
            "updateAvailable": False,
            "localVersion": local_version,
            "localCommit": f"v{local_version}",
            "error": f"GitHub version.json check failed ({owner}/{repo}@{branch}): {e}",
        }


def apply_hot_update_from_github() -> Dict[str, Any]:
    """
    Pulls the latest `forgesim_cluster/version.json`, `scripts/ForgePodRunner.java`,
    and `forgesim_cluster/forgesim_server.py` from `chayde/mtg-deck-collection`,
    recompiles `ForgePodRunner.java`, recycles warm JVM workers, and restarts the
    daemon process if `forgesim_server.py` itself changed.
    """
    owner = os.environ.get("GITHUB_OWNER", "chayde")
    repo = os.environ.get("GITHUB_REPO", "mtg-deck-collection")
    branch = os.environ.get("GITHUB_BRANCH", "master")
    token = os.environ.get("GITHUB_PAT", "").strip()

    headers = {"User-Agent": "forgesim-cluster-daemon"}
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        # 1. Fetch remote version.json manifest
        raw_manifest = _fetch_github_file(owner, repo, branch, "forgesim_cluster/version.json", headers)
        manifest_data = json.loads(raw_manifest)
        new_version = str(manifest_data.get("version", SERVICE_VERSION)).strip()
        files_cfg = manifest_data.get("files", {})
        bridge_path = files_cfg.get("bridge", "scripts/ForgePodRunner.java")
        server_path = files_cfg.get("server", "forgesim_cluster/forgesim_server.py")

        # 2. Fetch latest ForgePodRunner.java (fallback to forgesim_cluster/ForgePodRunner.java)
        try:
            java_code = _fetch_github_file(owner, repo, branch, bridge_path, headers)
        except Exception:
            java_code = _fetch_github_file(owner, repo, branch, "forgesim_cluster/ForgePodRunner.java", headers)

        COORDINATOR.java_source.write_text(java_code, encoding="utf-8")
        ok, msg = COORDINATOR.compile_bridge()
        if not ok:
            return {"success": False, "message": msg}

        # 3. Save updated version.json locally
        here = Path(__file__).resolve().parent
        (here / "version.json").write_text(raw_manifest, encoding="utf-8")

        # 4. Check if forgesim_server.py also changed in GitHub
        server_restarting = False
        try:
            remote_server_code = _fetch_github_file(owner, repo, branch, server_path, headers)
            this_file = Path(__file__).resolve()
            local_sha = hashlib.sha256(this_file.read_bytes()).hexdigest()
            remote_sha = hashlib.sha256(remote_server_code.encode("utf-8")).hexdigest()
            if local_sha != remote_sha:
                this_file.write_text(remote_server_code, encoding="utf-8")
                server_restarting = True
        except Exception as srv_err:
            print(f"[WARN] Could not check/update {server_path}: {srv_err}", file=sys.stderr)

        if server_restarting:
            def _delayed_exec_restart():
                time.sleep(1.5)
                print(f"[*] Restarting forgesim_server.py process to activate v{new_version}...")
                for w in COORDINATOR.workers:
                    w.stop()
                os.execv(sys.executable, [sys.executable] + sys.argv)

            threading.Thread(target=_delayed_exec_restart, daemon=True).start()
            return {
                "success": True,
                "mode": "github-hot-reload+restart",
                "version": new_version,
                "message": f"Updated to v{new_version} from {owner}/{repo}@{branch} (both ForgePodRunner.java and forgesim_server.py updated). Restarting daemon & warm JVM pool now...",
            }

        recycle_info = COORDINATOR.recycle_workers()
        return {
            "success": True,
            "mode": "github-hot-reload",
            "version": new_version,
            "message": f"Updated to v{new_version} from {owner}/{repo}@{branch}, recompiled ForgePodRunner.java, and recycled {recycle_info['workers_ready']} warm JVM workers.",
        }
    except Exception as e:
        return {"success": False, "message": f"GitHub hot-update failed: {e}"}


def trigger_watchtower_upgrade() -> Dict[str, Any]:
    """Triggers Watchtower HTTP update API (identical to rsltool /api/upgrade)."""
    wt_url = os.environ.get("WATCHTOWER_HTTP_API_URL", "http://watchtower:8080/v1/update")
    wt_token = os.environ.get("WATCHTOWER_HTTP_API_TOKEN", "watchtower-secret-token-123")

    headers = {"User-Agent": "forgesim-cluster-daemon"}
    if wt_token:
        headers["Authorization"] = f"Bearer {wt_token}"

    try:
        req = urllib.request.Request(wt_url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return {
                "success": True,
                "mode": "watchtower",
                "message": f"Watchtower container update triggered (HTTP {resp.status}). {body}",
            }
    except Exception as e:
        return {
            "success": False,
            "mode": "watchtower",
            "message": f"Watchtower trigger failed ({wt_url}): {e}",
        }


DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MTG Forge Pod Simulation Cluster — forgesim.chayde.lab</title>
<style>
  :root {
    --bg: #0b0f17;
    --panel: #151c28;
    --border: #263248;
    --text: #e2e8f0;
    --muted: #94a3b8;
    --accent: #38bdf8;
    --green: #22c55e;
    --amber: #f59e0b;
    --red: #ef4444;
    --purple: #a855f7;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 24px 32px;
    background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }
  .header {
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 16px;
    border-bottom: 1px solid var(--border); padding-bottom: 18px; margin-bottom: 22px;
  }
  .title-block h1 { margin: 0 0 6px 0; font-size: 1.55rem; color: #fff; }
  .title-block .sub { color: var(--muted); font-size: 0.9rem; }
  .controls { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
  button {
    background: #1e293b; color: var(--text); border: 1px solid var(--border);
    padding: 9px 14px; border-radius: 7px; cursor: pointer; font-weight: 600; font-size: 0.85rem;
    transition: all 0.15s;
  }
  button:hover { border-color: var(--accent); color: #fff; }
  button.primary { background: #0284c7; border-color: #38bdf8; color: #fff; }
  button.primary:hover { background: #0369a1; }
  button.update-avail { background: #16a34a; border-color: #4ade80; color: #fff; animation: pulse 2s infinite; }
  @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(34,197,94,0.5); } 70% { box-shadow: 0 0 0 8px rgba(34,197,94,0); } 100% { box-shadow: 0 0 0 0 rgba(34,197,94,0); } }
  .kpi-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 14px; margin-bottom: 24px;
  }
  .kpi {
    background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px;
  }
  .kpi .label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); }
  .kpi .val { font-size: 1.55rem; font-weight: 700; margin-top: 4px; color: #fff; }
  .kpi .note { font-size: 0.8rem; color: var(--muted); margin-top: 4px; }
  .banner {
    background: #172554; border: 1px solid #3b82f6; border-radius: 8px;
    padding: 12px 16px; margin-bottom: 20px; display: none; justify-content: space-between; align-items: center;
  }
  .batch-progress-card {
    background: #111827; border: 1px solid #38bdf8; border-radius: 10px;
    padding: 14px 18px; margin-bottom: 22px; display: none;
  }
  .progress-track {
    width: 100%; height: 10px; background: #1e293b; border-radius: 6px; overflow: hidden; margin-top: 10px;
  }
  .progress-fill {
    height: 100%; background: linear-gradient(90deg, #0284c7, #22c55e); width: 0%; transition: width 0.3s ease;
  }
  button.btn-mini {
    padding: 4px 9px; font-size: 0.74rem; border-radius: 5px; margin-top: 6px;
  }
  button.btn-warn {
    background: rgba(239,68,68,0.18); border-color: #ef4444; color: #fca5a5;
  }
  button.btn-warn:hover {
    background: #dc2626; color: #fff;
  }
  h2 { font-size: 1.15rem; margin: 22px 0 12px 0; color: #f8fafc; }
  .worker-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px;
  }
  .worker-card {
    background: var(--panel); border: 1px solid var(--border); border-radius: 9px; padding: 12px 14px;
  }
  .w-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
  .badge {
    padding: 2px 8px; border-radius: 12px; font-size: 0.72rem; font-weight: 700;
  }
  .badge.IDLE { background: rgba(34,197,94,0.18); color: #4ade80; border: 1px solid #22c55e; }
  .badge.BUSY { background: rgba(245,158,11,0.2); color: #fbbf24; border: 1px solid #f59e0b; }
  .badge.WARMING { background: rgba(56,189,248,0.18); color: #38bdf8; border: 1px solid #0284c7; }
  .badge.ERROR, .badge.STOPPED { background: rgba(239,68,68,0.2); color: #f87171; border: 1px solid #ef4444; }
  table { width: 100%; border-collapse: collapse; background: var(--panel); border-radius: 10px; overflow: hidden; border: 1px solid var(--border); }
  th, td { padding: 10px 14px; text-align: left; border-bottom: 1px solid var(--border); font-size: 0.88rem; }
  th { background: #0f172a; color: var(--muted); font-size: 0.76rem; text-transform: uppercase; }
</style>
</head>
<body>
  <div class="header">
    <div class="title-block">
      <h1>⚡ MTG Forge 4-AI Pod Simulation Cluster</h1>
      <div class="sub" id="sub-meta">Connecting to cluster coordinator...</div>
    </div>
    <div class="controls">
      <button onclick="checkUpdate()">🔍 Check for Updates</button>
      <button id="btn-hot-update" class="primary" onclick="triggerHotUpdate()">⚡ Pull GitHub Update &amp; Recompile</button>
      <button onclick="triggerWatchtower()">🐳 Watchtower Image Upgrade</button>
      <button onclick="recyclePool()">🔄 Recycle Warm JVMs</button>
    </div>
  </div>

  <div class="banner" id="status-banner">
    <span id="banner-text"></span>
    <button onclick="document.getElementById('status-banner').style.display='none'">Dismiss</button>
  </div>

  <div class="batch-progress-card" id="active-batch-card">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
      <div>
        <strong style="color:#38bdf8; font-size:0.95rem;" id="ab-title">Active Batch Running...</strong>
        <div style="color:#94a3b8; font-size:0.82rem; margin-top:3px;" id="ab-sub">-</div>
      </div>
      <button class="btn-warn" onclick="cancelActiveBatch()">🛑 Stop Batch Early</button>
    </div>
    <div class="progress-track"><div class="progress-fill" id="ab-bar"></div></div>
  </div>

  <div class="kpi-grid">
    <div class="kpi"><div class="label">Warm JVM Workers</div><div class="val" id="k-workers">-</div><div class="note" id="k-workers-note">Pre-loaded with 32.5k cards</div></div>
    <div class="kpi"><div class="label">Total Pod Games Run</div><div class="val" id="k-games">0</div><div class="note" id="k-batches">0 batches completed</div></div>
    <div class="kpi"><div class="label">Cluster Version</div><div class="val" id="k-commit">-</div><div class="note" id="k-jar">-</div></div>
    <div class="kpi"><div class="label">Node Uptime</div><div class="val" id="k-uptime">-</div><div class="note">0.0s cold-start latency</div></div>
  </div>

  <h2>Pre-Warmed JVM Worker Pool</h2>
  <div class="worker-grid" id="worker-grid"></div>

  <h2>Recent 4-Player Pod Simulation Batches (Click row to expand details)</h2>
  <table>
    <thead>
      <tr><th>Time</th><th>Batch ID</th><th>Hero Deck (Seat 1)</th><th>Gauntlet Opponents</th><th>Games</th><th>Hero Win Rate</th><th>Wall Clock</th><th>Effective / Game</th></tr>
    </thead>
    <tbody id="jobs-tbody"><tr><td colspan="8" style="color:#94a3b8;">No simulation batches run since boot.</td></tr></tbody>
  </table>

<script>
function showBanner(msg, isUpdate=false) {
  const b = document.getElementById('status-banner');
  document.getElementById('banner-text').innerText = msg;
  b.style.display = 'flex';
}

async function refreshStatus() {
  try {
    const r = await fetch('/api/v1/status');
    const d = await r.json();
    document.getElementById('sub-meta').innerText = `Service v${d.version} ${d.released ? '('+d.released+')' : ''} | Engine: ${d.forge_jar} | Bridge SHA: ${d.java_bridge_sha}`;
    document.getElementById('k-workers').innerText = `${d.workers_idle} Idle / ${d.workers_busy} Busy`;
    document.getElementById('k-workers-note').innerText = `${d.workers_total} total (${d.workers_warming} warming)`;
    document.getElementById('k-games').innerText = d.total_games_run;
    document.getElementById('k-batches').innerText = `${d.total_batches_run} batches completed`;
    document.getElementById('k-commit').innerText = `v${d.version}`;
    document.getElementById('k-jar').innerText = `Bridge SHA: ${d.java_bridge_sha}`;
    const mins = Math.floor(d.uptime_sec / 60);
    document.getElementById('k-uptime').innerText = mins > 60 ? `${(mins/60).toFixed(1)}h` : `${mins}m ${d.uptime_sec%60}s`;

    const abCard = document.getElementById('active-batch-card');
    if (d.active_batch) {
      const ab = d.active_batch;
      abCard.style.display = 'block';
      document.getElementById('ab-title').innerText = `⚡ Batch ${ab.batch_id} in Progress: ${ab.hero_deck} vs. ${(ab.opponents || []).join(', ')}`;
      document.getElementById('ab-sub').innerText = `${ab.games_completed} / ${ab.games_total} games completed (${ab.pct_complete}%) • Hero Wins: ${ab.hero_wins} • Timeouts/Skips: ${ab.timeouts} • Elapsed: ${ab.elapsed_sec}s (Cap: ${ab.timeout_sec}s/game)`;
      document.getElementById('ab-bar').style.width = `${ab.pct_complete}%`;
    } else {
      abCard.style.display = 'none';
    }

    const wg = document.getElementById('worker-grid');
    wg.innerHTML = d.workers.map(w => {
      const elapsedTag = (w.status === 'BUSY' && w.job_elapsed_sec !== undefined)
        ? ` <strong style="color:${w.job_elapsed_sec > 75 ? '#f87171' : '#38bdf8'};">(${w.job_elapsed_sec}s)</strong>`
        : '';
      const actionBtn = (w.status === 'BUSY')
        ? `<button class="btn-mini btn-warn" onclick="killWorker(${w.worker_id}, true)">⏭️ Skip / Kill Game</button>`
        : `<button class="btn-mini" onclick="killWorker(${w.worker_id}, false)">🔄 Restart Worker</button>`;
      return `
      <div class="worker-card">
        <div class="w-head">
          <strong>Worker #${w.worker_id}</strong>
          <span class="badge ${w.status}">${w.status}</span>
        </div>
        <div style="font-size:0.8rem;color:#94a3b8;">
          PID: <code style="color:#e2e8f0;">${w.pid || '-'}</code> &bull; Games: <strong style="color:#e2e8f0;">${w.games_completed}</strong><br>
          Avg Game: <strong>${w.avg_game_ms ? (w.avg_game_ms/1000).toFixed(1)+'s' : '-'}</strong><br>
          ${w.current_job ? `<span style="color:#fbbf24;">▶ ${w.current_job}${elapsedTag}</span>` : (w.last_error ? `<span style="color:#f87171;">${w.last_error}</span>` : 'Ready for instant dispatch')}<br>
          ${actionBtn}
        </div>
      </div>
      `;
    }).join('');

    const tb = document.getElementById('jobs-tbody');
    if (d.recent_jobs && d.recent_jobs.length > 0) {
      tb.innerHTML = d.recent_jobs.map((j, idx) => `
        <tr style="cursor:pointer;" onclick="toggleBatchDetail(${idx})">
          <td>${j.timestamp}</td>
          <td><code>${j.batch_id}</code> ▾</td>
          <td><strong>${j.hero_deck}</strong></td>
          <td>${(j.opponents || []).join(', ')}</td>
          <td>${j.games}</td>
          <td><strong style="color:${j.hero_wins > 0 ? '#4ade80' : '#f87171'};">${j.win_rate_pct}%</strong> (${j.hero_wins}/${j.games})</td>
          <td><strong>${j.wall_sec}s</strong></td>
          <td>${j.avg_sec_per_game}s/game</td>
        </tr>
        <tr id="batch-det-${idx}" style="display:none; background:#0d1522;">
          <td colspan="8" style="padding:14px 20px;">
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:12px; font-size:0.83rem;">
              <div><strong>Batch ID:</strong> <code>${j.batch_id}</code></div>
              <div><strong>Hero Wins:</strong> ${j.hero_wins} / ${j.games} (${j.win_rate_pct}%)</div>
              <div><strong>Timeouts / Retries:</strong> ${j.timeouts || 0} (${j.requeued_games || 0} auto-requeued)</div>
              <div><strong>Avg Game Duration:</strong> ${j.avg_sec_per_game}s</div>
              <div><strong>Opponent Pod:</strong> ${(j.opponents || []).join(', ')}</div>
            </div>
          </td>
        </tr>
      `).join('');
    }
  } catch (e) {
    console.error(e);
  }
}

async function checkUpdate() {
  showBanner('Checking forgesim_cluster/version.json in GitHub (chayde/mtg-deck-collection)...');
  const r = await fetch('/api/v1/check-update');
  const d = await r.json();
  const btn = document.getElementById('btn-hot-update');
  if (d.updateAvailable) {
    btn.className = 'update-avail';
    btn.innerText = `⬆️ Update Available (v${d.remoteVersion}) — Click to Apply`;
    showBanner(`New ForgeSim release available on GitHub: v${d.remoteVersion} (Running: v${d.localVersion}) — "${d.changelog || ''}". Click "Update Available" to pull & recompile!`);
  } else {
    btn.className = 'primary';
    btn.innerText = '⚡ Pull GitHub Update & Recompile';
    showBanner(`Up to date! Running ForgeSim v${d.localVersion} (GitHub manifest: v${d.remoteVersion || d.localVersion}). ${d.error || ''}`);
  }
}

async function triggerHotUpdate() {
  showBanner('Pulling latest version.json, ForgePodRunner.java, and forgesim_server.py from GitHub, recompiling, and recycling warm JVM workers...');
  const r = await fetch('/api/v1/update', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({mode: 'github'})});
  const d = await r.json();
  showBanner(d.message || JSON.stringify(d));
  document.getElementById('btn-hot-update').className = 'primary';
  document.getElementById('btn-hot-update').innerText = '⚡ Pull GitHub Update & Recompile';
  setTimeout(refreshStatus, 2000);
}

async function triggerWatchtower() {
  showBanner('Sending container upgrade trigger to Watchtower HTTP API...');
  const r = await fetch('/api/v1/upgrade-container', {method: 'POST'});
  const d = await r.json();
  showBanner(d.message || JSON.stringify(d));
}

async function recyclePool() {
  showBanner('Recycling all Pre-Warmed JVM Workers...');
  const r = await fetch('/api/v1/recycle', {method: 'POST'});
  const d = await r.json();
  showBanner(`Worker pool recycled: ${d.workers_ready}/${d.total_workers} workers IDLE.`);
  refreshStatus();
}

async function killWorker(workerId, isBusy) {
  const actionLabel = isBusy ? `Skipping current game on Worker #${workerId} and re-warming...` : `Restarting Worker #${workerId}...`;
  showBanner(actionLabel);
  const r = await fetch('/api/v1/kill-worker', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({worker_id: workerId})
  });
  const d = await r.json();
  showBanner(d.message || JSON.stringify(d));
  refreshStatus();
}

async function cancelActiveBatch() {
  showBanner('Stopping active batch and aborting in-flight games...');
  const r = await fetch('/api/v1/cancel-batch', {method: 'POST'});
  const d = await r.json();
  showBanner(d.message || JSON.stringify(d));
  refreshStatus();
}

function toggleBatchDetail(idx) {
  const row = document.getElementById(`batch-det-${idx}`);
  if (row) {
    row.style.display = (row.style.display === 'none' ? 'table-row' : 'none');
  }
}

refreshStatus();
setInterval(refreshStatus, 2500);
</script>
</body>
</html>
"""


class ForgeSimHttpHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for the Forge Pod Simulation Cluster."""

    def _send_json(self, status_code: int, payload: Dict[str, Any]):
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(raw)

    def _read_json_body(self) -> Dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        return json.loads(raw) if raw.strip() else {}

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            raw = DASHBOARD_HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return

        if self.path in ("/health", "/api/v1/health"):
            st = COORDINATOR.get_status()
            self._send_json(200, {
                "status": "healthy",
                "workers_total": st["workers_total"],
                "workers_idle": st["workers_idle"],
                "workers_busy": st["workers_busy"],
                "version": st["version"],
            })
            return

        if self.path in ("/api/v1/status", "/api/status"):
            self._send_json(200, COORDINATOR.get_status())
            return

        if self.path in ("/api/v1/version", "/api/version"):
            self._send_json(200, COORDINATOR.get_version_info())
            return

        if self.path in ("/api/v1/check-update", "/api/check-update"):
            self._send_json(200, check_github_for_updates())
            return

        self._send_json(404, {"error": f"Unknown endpoint: {self.path}"})

    def do_POST(self):
        if self.path in ("/api/v1/simulate", "/simulate"):
            try:
                body = self._read_json_body()
                result = COORDINATOR.run_pod_simulation(body)
                self._send_json(200, result)
            except Exception as e:
                self._send_json(400, {"status": "error", "error": str(e)})
            return

        if self.path in ("/api/v1/recycle", "/api/recycle"):
            res = COORDINATOR.recycle_workers()
            self._send_json(200, res)
            return

        if self.path in ("/api/v1/kill-worker", "/api/kill-worker"):
            body = self._read_json_body()
            w_id = int(body.get("worker_id", 0))
            res = COORDINATOR.kill_worker_job(w_id, reason=body.get("reason", "Skipped via Web UI"))
            self._send_json(200 if res.get("success") else 400, res)
            return

        if self.path in ("/api/v1/cancel-batch", "/api/cancel-batch"):
            res = COORDINATOR.cancel_active_batch()
            self._send_json(200, res)
            return

        if self.path in ("/api/v1/update", "/api/update"):
            body = self._read_json_body()
            mode = body.get("mode", "github")
            if mode == "push":
                # Direct LAN push of ForgePodRunner.java (and optional version.json / forgesim_server.py) from workstation
                java_code = body.get("java_source", "")
                commit_sha = body.get("commit", "")
                version_json_str = body.get("version_json", "")
                server_code = body.get("server_source", "")
                if not java_code:
                    self._send_json(400, {"success": False, "message": "Missing java_source in push payload."})
                    return
                COORDINATOR.java_source.write_text(java_code, encoding="utf-8")
                ok, msg = COORDINATOR.compile_bridge()
                if not ok:
                    self._send_json(500, {"success": False, "message": msg})
                    return
                here = Path(__file__).resolve().parent
                if commit_sha:
                    (here / "commit.txt").write_text(commit_sha + "\n", encoding="utf-8")
                if version_json_str:
                    (here / "version.json").write_text(version_json_str, encoding="utf-8")
                if server_code:
                    this_file = Path(__file__).resolve()
                    if hashlib.sha256(this_file.read_bytes()).hexdigest() != hashlib.sha256(server_code.encode("utf-8")).hexdigest():
                        this_file.write_text(server_code, encoding="utf-8")
                        def _delayed_exec_restart():
                            time.sleep(1.5)
                            for w in COORDINATOR.workers:
                                w.stop()
                            os.execv(sys.executable, [sys.executable] + sys.argv)
                        threading.Thread(target=_delayed_exec_restart, daemon=True).start()
                        self._send_json(200, {
                            "success": True,
                            "mode": "lan-push+restart",
                            "message": f"Pushed & compiled ForgePodRunner.java and updated forgesim_server.py. Restarting daemon & warm JVM pool now...",
                        })
                        return
                rec = COORDINATOR.recycle_workers()
                self._send_json(200, {
                    "success": True,
                    "mode": "lan-push",
                    "message": f"Pushed & compiled updated ForgePodRunner.java ({len(java_code)} bytes) and recycled {rec['workers_ready']} warm JVM workers.",
                })
                return
            elif mode == "watchtower":
                self._send_json(200, trigger_watchtower_upgrade())
                return
            else:
                self._send_json(200, apply_hot_update_from_github())
            return

        if self.path in ("/api/v1/upgrade-container", "/api/upgrade"):
            self._send_json(200, trigger_watchtower_upgrade())
            return

        self._send_json(404, {"error": f"Unknown POST endpoint: {self.path}"})

    def log_message(self, fmt: str, *args: Any):
        # Suppress noisy polling logs for /api/v1/status
        if "/api/v1/status" in (args[0] if args else ""):
            return
        sys.stdout.write(f"[HTTP] {self.address_string()} - {fmt % args}\n")


def main():
    global COORDINATOR
    parser = argparse.ArgumentParser(description="MTG Forge 4-AI Pod Simulation Cluster Daemon")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8080")), help="HTTP listen port (default: 8080)")
    parser.add_argument("--workers", type=int, default=int(os.environ.get("WORKERS", "16")), help="Number of Pre-Warmed JVM Workers (default: 10)")
    parser.add_argument("--heap-mb", type=int, default=int(os.environ.get("WORKER_HEAP_MB", "1536")), help="Max heap MB per JVM worker (default: 1536)")
    parser.add_argument("--forge-dir", type=str, default=os.environ.get("FORGE_DIR"), help="Path to MTG Forge directory")
    parser.add_argument("--java-source", type=str, default=None, help="Path to ForgePodRunner.java")
    args = parser.parse_args()

    if args.forge_dir:
        forge_dir = Path(args.forge_dir)
        jars = sorted(forge_dir.glob("forge-gui-desktop-*-jar-with-dependencies.jar"))
        if not jars:
            raise FileNotFoundError(f"No forge-gui-desktop jar found in {forge_dir}")
        forge_jar = jars[-1]
    else:
        forge_dir, forge_jar = find_forge_install()

    here = Path(__file__).resolve().parent
    if args.java_source:
        java_source = Path(args.java_source).resolve()
    elif (here / "ForgePodRunner.java").exists():
        java_source = here / "ForgePodRunner.java"
    else:
        java_source = here.parent / "scripts" / "ForgePodRunner.java"

    bridge_dir = here / "build"

    COORDINATOR = ForgeSimClusterCoordinator(
        num_workers=args.workers,
        heap_mb=args.heap_mb,
        forge_dir=forge_dir,
        forge_jar=forge_jar,
        java_source=java_source,
        bridge_dir=bridge_dir,
    )

    server = ThreadingHTTPServer(("0.0.0.0", args.port), ForgeSimHttpHandler)
    print("======================================================================")
    print(f" MTG FORGE POD SIMULATION CLUSTER DAEMON LISTENING ON :{args.port}")
    print(f" Web Dashboard : http://localhost:{args.port}/")
    print(f" Sim Endpoint  : POST http://localhost:{args.port}/api/v1/simulate")
    print(f" Update API    : POST http://localhost:{args.port}/api/v1/update")
    print("======================================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down warm JVM workers...")
        for w in COORDINATOR.workers:
            w.stop()


if __name__ == "__main__":
    main()
