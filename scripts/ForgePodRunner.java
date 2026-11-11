import com.google.common.eventbus.Subscribe;
import com.google.gson.Gson;
import forge.GuiDesktop;
import forge.LobbyPlayer;
import forge.ai.AIOption;
import forge.ai.ComputerUtil;
import forge.ai.LobbyPlayerAi;
import forge.ai.PlayerControllerAi;
import forge.deck.Deck;
import forge.deck.io.DeckSerializer;
import forge.error.ExceptionHandler;
import forge.game.Game;
import forge.game.GameEndReason;
import forge.game.GameOutcome;
import forge.game.GameRules;
import forge.game.GameType;
import forge.game.Match;
import forge.game.card.Card;
import forge.game.card.CardCollectionView;
import forge.game.card.CardView;
import forge.game.event.*;
import forge.game.phase.PhaseType;
import forge.game.player.Player;
import forge.game.player.PlayerOutcome;
import forge.game.player.PlayerView;
import forge.game.player.RegisteredPlayer;
import forge.game.spellability.SpellAbilityView;
import forge.game.spellability.StackItemView;
import forge.game.zone.ZoneType;
import forge.game.zone.ZoneView;
import forge.gui.GuiBase;
import forge.model.FModel;
import forge.player.GamePlayerUtil;
import forge.util.MyRandom;
import forge.view.TimeLimitedCodeBlock;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/**
 * ForgePodRunner — Headless 4-Player Commander Pod Telemetry Bridge
 *
 * Runs automated 4-AI Commander games using the local MTG Forge rules engine
 * while attaching an event-bus telemetry listener and custom Hero AI controller to capture:
 *   - Seat 1 (Hero Deck) exact rejected mulligan hands, London bottomed cards, and final kept hand
 *   - Optional Smart Synergy-Aware Mulligan override (-smartMulligan) rejecting Synergy Traps
 *   - Seat 1 turn-by-turn card draws (exact card names from Library -> Hand)
 *   - Seat 1 turn-by-turn land drops, spell casts, commander casts, and end-of-turn board states
 *   - Opponent interaction targeted at Seat 1, damage vectors, player eliminations, and match outcomes
 *
 * Emits one structured JSON line per game prefixed with "TELEMETRY_GAME_JSON:".
 */
public class ForgePodRunner {

    public static class DrawRecord {
        public int hero_turn;
        public int global_turn;
        public String card;
        public String phase;
    }

    public static class LandPlayRecord {
        public int hero_turn;
        public int global_turn;
        public String card;
        public boolean tapped;
    }

    public static class SpellCastRecord {
        public int hero_turn;
        public int global_turn;
        public String card;
        public boolean is_commander;
        public String targets;
    }

    public static class InteractionRecord {
        public int hero_turn;
        public int global_turn;
        public String by_player;
        public String card;
        public boolean is_spell;
        public String targets;
    }

    public static class HeroTurnSnapshot {
        public int hero_turn;
        public int global_turn;
        public int lands_total;
        public int lands_untapped;
        public int mana_sources_total;
        public int mana_sources_ready;
        public int creatures_count;
        public int total_power;
        public boolean commander_in_play;
        public int hand_size;
        public List<String> hand_cards = new ArrayList<>();
        public int graveyard_size;
        public int hero_life;
        public int opponents_alive;
        public List<String> actions_this_turn = new ArrayList<>();
    }

    public static class EliminationRecord {
        public int seat;
        public String player;
        public String deck;
        public int global_turn;
        public int hero_turn;
        public String reason;
    }

    public static class SeatSummary {
        public int seat;
        public String player;
        public String deck;
        public String commander;
        public int mulligans;
        public int opening_hand_size;
        public int turn_order_pos;
        public int final_life;
        public boolean has_won;
        public boolean has_lost;
        public String outcome_text;
        public int commander_casts;
        public List<Integer> commander_cast_turns = new ArrayList<>();
        public int spells_cast;
        public int peak_lands_in_play;
        public int peak_creatures_in_play;
        public int peak_power_in_play;
        public Map<String, Integer> commander_damage_taken = new LinkedHashMap<>();
    }

    public static class GameTelemetry {
        public int game_index;
        public long seed;
        public long duration_ms;
        public boolean timed_out;
        public boolean exception_occurred;
        public String error_message;
        public int total_global_turns;
        public int total_hero_turns;
        public String winner_player;
        public String winner_deck;
        public int winner_seat;
        public String win_reason;

        // Hero (Seat 1) Opening Hand & Mulligan Telemetry
        public String hero_deck;
        public String hero_commander;
        public int hero_turn_order_pos;
        public int hero_mulligans;
        public int hero_opening_hand_size;
        public List<List<String>> hero_mulliganed_hands = new ArrayList<>();
        public List<String> hero_bottomed_cards = new ArrayList<>();
        public List<String> hero_kept_hand = new ArrayList<>();

        // Hero Progression & Action Telemetry
        public List<Integer> hero_commander_cast_turns = new ArrayList<>();
        public List<Integer> hero_commander_global_turns = new ArrayList<>();
        public List<DrawRecord> hero_draws = new ArrayList<>();
        public List<LandPlayRecord> hero_land_plays = new ArrayList<>();
        public List<SpellCastRecord> hero_spell_casts = new ArrayList<>();
        public List<InteractionRecord> opp_interaction_vs_hero = new ArrayList<>();
        public List<InteractionRecord> hero_interaction_vs_opp = new ArrayList<>();
        public List<HeroTurnSnapshot> hero_turn_snapshots = new ArrayList<>();

        // Combat & Damage Stats
        public int hero_combat_damage_dealt = 0;
        public int hero_noncombat_damage_dealt = 0;
        public int hero_commander_damage_dealt = 0;
        public int hero_damage_taken = 0;
        public int hero_permanents_destroyed_or_exiled = 0;
        public int hero_commander_removed_count = 0;

        // Pod Summary
        public List<EliminationRecord> eliminations = new ArrayList<>();
        public List<SeatSummary> seats = new ArrayList<>();
    }

    // Shared reference to current game's telemetry for HeroLobbyPlayerAi
    private static volatile GameTelemetry activeTelemetry = null;
    private static volatile boolean useSmartMulligan = true;

    public static class HeroControllerAi extends PlayerControllerAi {
        private final Player hero;

        public HeroControllerAi(Game game, Player p, LobbyPlayer lp) {
            super(game, p, lp);
            this.hero = p;
        }

        @Override
        public boolean mulliganKeepHand(Player firstPlayer, int cardsToReturn) {
            List<String> handNames = extractZoneCardNames(hero, ZoneType.Hand);
            boolean keep;

            if (useSmartMulligan && cardsToReturn <= 2) {
                int lands = 0;
                int earlyPlays = 0;
                int heavyPayoffs = 0;
                for (Card c : hero.getCardsIn(ZoneType.Hand)) {
                    if (c.isLand() || c.hasPlayableLandFace()) {
                        lands++;
                    } else {
                        int cmc = c.getCMC();
                        if (cmc <= 3) earlyPlays++;
                        if (cmc >= 5) heavyPayoffs++;
                    }
                }
                boolean isSynergyTrap = (lands >= 3 && earlyPlays == 0 && heavyPayoffs >= 3);
                if (lands < 2 || lands > 5 || isSynergyTrap) {
                    keep = false;
                } else {
                    keep = !ComputerUtil.wantMulligan(hero, cardsToReturn);
                }
            } else {
                keep = !ComputerUtil.wantMulligan(hero, cardsToReturn);
            }

            if (!keep && activeTelemetry != null && !handNames.isEmpty()) {
                activeTelemetry.hero_mulliganed_hands.add(handNames);
            }
            return keep;
        }

        @Override
        public CardCollectionView tuckCardsViaMulligan(CardCollectionView hand, int cardsToReturn) {
            CardCollectionView tucked = super.tuckCardsViaMulligan(hand, cardsToReturn);
            if (tucked != null && activeTelemetry != null) {
                for (Card c : tucked) {
                    activeTelemetry.hero_bottomed_cards.add(cleanCardName(c));
                }
            }
            return tucked;
        }
    }

    public static class HeroLobbyPlayerAi extends LobbyPlayerAi {
        public HeroLobbyPlayerAi(String name, Set<AIOption> options) {
            super(name, options);
        }

        @Override
        public Player createIngamePlayer(Game game, int id) {
            Player p = new Player(getName(), game, id);
            HeroControllerAi ctrl = new HeroControllerAi(game, p, this);
            p.setFirstController(ctrl);
            return p;
        }
    }

    private static String cleanCardName(CardView cv) {
        if (cv == null) return "Unknown";
        String oracle = cv.getOracleName();
        if (oracle != null && !oracle.isEmpty()) return oracle;
        String name = cv.getName();
        return (name != null && !name.isEmpty()) ? name : cv.toString();
    }

    private static String cleanCardName(Card c) {
        if (c == null) return "Unknown";
        String name = c.getName();
        return (name != null && !name.isEmpty()) ? name : c.toString();
    }

    private static List<String> extractZoneCardNames(Player p, ZoneType zt) {
        List<String> res = new ArrayList<>();
        if (p == null) return res;
        CardCollectionView cards = p.getCardsIn(zt);
        if (cards != null) {
            for (Card c : cards) {
                res.add(cleanCardName(c));
            }
        }
        return res;
    }

    public static class PodTelemetryVisitor extends IGameEventVisitor.Base<Void> {
        private final Game game;
        private final Player heroPlayer;
        private final List<Player> podPlayers;
        private final Map<PlayerView, Integer> viewToSeat = new HashMap<>();
        private final Map<PlayerView, String> viewToDeck = new HashMap<>();
        private final GameTelemetry telemetry;

        private int currentGlobalTurn = 0;
        private int currentHeroTurn = 0;
        private String currentPhase = "PREGAME";
        private boolean openingHandCaptured = false;
        private boolean heroTurnActive = false;
        private List<String> currentHeroTurnActions = new ArrayList<>();
        private final Set<Integer> recordedEliminations = new HashSet<>();
        private final Map<Integer, Integer> seatSpellsCast = new HashMap<>();
        private final Map<Integer, List<Integer>> seatCmdCastTurns = new HashMap<>();
        private final Map<Integer, Integer> seatTurnOrderPos = new HashMap<>();
        private final Map<Integer, Integer> seatPeakLands = new HashMap<>();
        private final Map<Integer, Integer> seatPeakCreatures = new HashMap<>();
        private final Map<Integer, Integer> seatPeakPower = new HashMap<>();

        public PodTelemetryVisitor(Game game, List<Player> podPlayers, List<String> deckNames, GameTelemetry telemetry) {
            this.game = game;
            this.podPlayers = podPlayers;
            this.heroPlayer = podPlayers.get(0);
            this.telemetry = telemetry;
            for (int i = 0; i < podPlayers.size(); i++) {
                Player p = podPlayers.get(i);
                int seat = i + 1;
                viewToSeat.put(p.getView(), seat);
                viewToDeck.put(p.getView(), deckNames.get(i));
                seatSpellsCast.put(seat, 0);
                seatCmdCastTurns.put(seat, new ArrayList<>());
                seatTurnOrderPos.put(seat, seat);
                seatPeakLands.put(seat, 0);
                seatPeakCreatures.put(seat, 0);
                seatPeakPower.put(seat, 0);
            }
        }

        @Subscribe
        public void receive(GameEvent ev) {
            try {
                ev.visit(this);
            } catch (Exception ignored) {
                // Never disrupt the game engine on telemetry visitor errors
            }
        }

        private void updatePodPeaks() {
            for (int i = 0; i < podPlayers.size(); i++) {
                Player p = podPlayers.get(i);
                if (p.hasLost()) continue;
                int seat = i + 1;
                int lands = p.getLandsInPlay().size();
                int creat = p.getCreaturesInPlay().size();
                int pwr = 0;
                for (Card c : p.getCreaturesInPlay()) {
                    pwr += Math.max(0, c.getNetPower());
                }
                if (lands > seatPeakLands.getOrDefault(seat, 0)) seatPeakLands.put(seat, lands);
                if (creat > seatPeakCreatures.getOrDefault(seat, 0)) seatPeakCreatures.put(seat, creat);
                if (pwr > seatPeakPower.getOrDefault(seat, 0)) seatPeakPower.put(seat, pwr);
            }
        }

        @Override
        public Void visit(GameEventTurnPhase ev) {
            if (ev.phase() != null) {
                currentPhase = ev.phase().name();
            }
            if (ev.phase() == PhaseType.CLEANUP) {
                updatePodPeaks();
                if (heroTurnActive) {
                    recordHeroTurnSnapshot();
                    heroTurnActive = false;
                }
            }
            return null;
        }

        @Override
        public Void visit(GameEventTurnBegan ev) {
            currentGlobalTurn = ev.turnNumber();
            telemetry.total_global_turns = Math.max(telemetry.total_global_turns, currentGlobalTurn);

            if (!openingHandCaptured) {
                openingHandCaptured = true;
                captureOpeningHandsAndTurnOrder();
            }

            updatePodPeaks();
            checkEliminations();

            PlayerView turnOwner = ev.turnOwner();
            if (turnOwner != null && turnOwner.equals(heroPlayer.getView())) {
                if (heroTurnActive) {
                    recordHeroTurnSnapshot();
                }
                currentHeroTurn++;
                telemetry.total_hero_turns = currentHeroTurn;
                heroTurnActive = true;
                currentHeroTurnActions = new ArrayList<>();
            } else if (heroTurnActive) {
                recordHeroTurnSnapshot();
                heroTurnActive = false;
            }
            return null;
        }

        private void captureOpeningHandsAndTurnOrder() {
            telemetry.hero_kept_hand = extractZoneCardNames(heroPlayer, ZoneType.Hand);
            telemetry.hero_mulligans = Math.max(
                    heroPlayer.getStats().getMulliganCount(),
                    telemetry.hero_mulliganed_hands.size()
            );
            telemetry.hero_opening_hand_size = telemetry.hero_kept_hand.size();

            List<Player> turnOrder = new ArrayList<>();
            for (Player p : game.getPlayersInTurnOrder()) {
                turnOrder.add(p);
            }
            for (int i = 0; i < podPlayers.size(); i++) {
                Player p = podPlayers.get(i);
                int pos = turnOrder.indexOf(p);
                seatTurnOrderPos.put(i + 1, (pos >= 0) ? (pos + 1) : (i + 1));
            }
            telemetry.hero_turn_order_pos = seatTurnOrderPos.getOrDefault(1, 1);
        }

        private void recordHeroTurnSnapshot() {
            HeroTurnSnapshot snap = new HeroTurnSnapshot();
            snap.hero_turn = currentHeroTurn;
            snap.global_turn = currentGlobalTurn;

            int landsTotal = 0;
            int landsUntapped = 0;
            for (Card c : heroPlayer.getLandsInPlay()) {
                landsTotal++;
                if (c.isUntapped()) landsUntapped++;
            }
            snap.lands_total = landsTotal;
            snap.lands_untapped = landsUntapped;

            int manaTotal = 0;
            int manaReady = 0;
            boolean cmdInPlay = false;
            for (Card c : heroPlayer.getCardsIn(ZoneType.Battlefield)) {
                if (c.isCommander() && c.getOwner().equals(heroPlayer)) {
                    cmdInPlay = true;
                }
                boolean hasMana = c.isLand() || (c.getManaAbilities() != null && !c.getManaAbilities().isEmpty());
                if (hasMana) {
                    manaTotal++;
                    boolean sickCreature = c.isCreature() && c.isSick();
                    if (!sickCreature) {
                        manaReady++;
                    }
                }
            }
            snap.mana_sources_total = manaTotal;
            snap.mana_sources_ready = manaReady;
            snap.commander_in_play = cmdInPlay;

            int creatures = 0;
            int totalPower = 0;
            for (Card c : heroPlayer.getCreaturesInPlay()) {
                creatures++;
                totalPower += Math.max(0, c.getNetPower());
            }
            snap.creatures_count = creatures;
            snap.total_power = totalPower;

            snap.hand_cards = extractZoneCardNames(heroPlayer, ZoneType.Hand);
            snap.hand_size = snap.hand_cards.size();
            snap.graveyard_size = heroPlayer.getCardsIn(ZoneType.Graveyard).size();
            snap.hero_life = heroPlayer.getLife();

            int oppsAlive = 0;
            for (int i = 1; i < podPlayers.size(); i++) {
                if (!podPlayers.get(i).hasLost()) oppsAlive++;
            }
            snap.opponents_alive = oppsAlive;
            snap.actions_this_turn = new ArrayList<>(currentHeroTurnActions);

            telemetry.hero_turn_snapshots.add(snap);
        }

        @Override
        public Void visit(GameEventCardChangeZone ev) {
            ZoneView from = ev.from();
            ZoneView to = ev.to();
            CardView card = ev.card();
            if (from == null || to == null || card == null) return null;

            ZoneType fromZt = from.zoneType();
            ZoneType toZt = to.zoneType();
            PlayerView toPlayer = to.player();
            PlayerView fromPlayer = from.player();

            // Card Drawn (Library -> Hand after game starts)
            if (currentGlobalTurn >= 1 && fromZt == ZoneType.Library && toZt == ZoneType.Hand) {
                if (toPlayer != null && toPlayer.equals(heroPlayer.getView())) {
                    DrawRecord dr = new DrawRecord();
                    dr.hero_turn = Math.max(1, currentHeroTurn);
                    dr.global_turn = currentGlobalTurn;
                    dr.card = cleanCardName(card);
                    dr.phase = currentPhase;
                    telemetry.hero_draws.add(dr);
                }
            }

            // Hero permanent leaving Battlefield -> Graveyard / Exile / Command
            if (currentGlobalTurn >= 1 && fromZt == ZoneType.Battlefield
                    && (toZt == ZoneType.Graveyard || toZt == ZoneType.Exile || toZt == ZoneType.Command)) {
                if (fromPlayer != null && fromPlayer.equals(heroPlayer.getView()) && !card.isToken()) {
                    telemetry.hero_permanents_destroyed_or_exiled++;
                    if (card.isCommander()) {
                        telemetry.hero_commander_removed_count++;
                    }
                }
            }
            return null;
        }

        @Override
        public Void visit(GameEventLandPlayed ev) {
            PlayerView pv = ev.player();
            CardView land = ev.land();
            if (pv != null && land != null && pv.equals(heroPlayer.getView())) {
                LandPlayRecord lpr = new LandPlayRecord();
                lpr.hero_turn = Math.max(1, currentHeroTurn);
                lpr.global_turn = currentGlobalTurn;
                lpr.card = cleanCardName(land);
                lpr.tapped = land.isTapped();
                telemetry.hero_land_plays.add(lpr);
                currentHeroTurnActions.add("Land: " + lpr.card + (lpr.tapped ? " (tapped)" : ""));
            }
            return null;
        }

        @Override
        public Void visit(GameEventSpellAbilityCast ev) {
            SpellAbilityView sa = ev.sa();
            StackItemView si = ev.si();
            if (sa == null || si == null) return null;

            PlayerView activator = si.getActivatingPlayer();
            CardView host = sa.getHostCard();
            boolean isSpell = sa.isSpell();
            boolean isTrigger = si.isTrigger();
            if (activator == null || host == null) return null;

            String cardName = cleanCardName(host);
            boolean isCmd = host.isCommander();
            String targetDesc = ev.targetDescription() != null ? ev.targetDescription() : "";
            Integer seat = viewToSeat.get(activator);

            if (isSpell && seat != null) {
                seatSpellsCast.put(seat, seatSpellsCast.getOrDefault(seat, 0) + 1);
                if (isCmd) {
                    int roundEst = (seat == 1) ? Math.max(1, currentHeroTurn) : Math.max(1, (currentGlobalTurn + 3) / 4);
                    seatCmdCastTurns.get(seat).add(roundEst);
                }
            }

            if (activator.equals(heroPlayer.getView())) {
                if (isSpell) {
                    SpellCastRecord scr = new SpellCastRecord();
                    scr.hero_turn = Math.max(1, currentHeroTurn);
                    scr.global_turn = currentGlobalTurn;
                    scr.card = cardName;
                    scr.is_commander = isCmd;
                    scr.targets = targetDesc;
                    telemetry.hero_spell_casts.add(scr);
                    currentHeroTurnActions.add("Cast: " + cardName + (isCmd ? " [COMMANDER]" : ""));

                    if (isCmd) {
                        telemetry.hero_commander_cast_turns.add(Math.max(1, currentHeroTurn));
                        telemetry.hero_commander_global_turns.add(currentGlobalTurn);
                    }
                }

                if (!isTrigger && hasOpponentTarget(si, heroPlayer.getView())) {
                    InteractionRecord ir = new InteractionRecord();
                    ir.hero_turn = Math.max(1, currentHeroTurn);
                    ir.global_turn = currentGlobalTurn;
                    ir.by_player = activator.getName();
                    ir.card = cardName;
                    ir.is_spell = isSpell;
                    ir.targets = targetDesc;
                    telemetry.hero_interaction_vs_opp.add(ir);
                }
            } else {
                if (!isTrigger && targetsPlayerOrPermanents(si, heroPlayer.getView())) {
                    InteractionRecord ir = new InteractionRecord();
                    ir.hero_turn = Math.max(1, currentHeroTurn);
                    ir.global_turn = currentGlobalTurn;
                    ir.by_player = activator.getName();
                    ir.card = cardName;
                    ir.is_spell = isSpell;
                    ir.targets = targetDesc;
                    telemetry.opp_interaction_vs_hero.add(ir);
                }
            }
            return null;
        }

        private boolean targetsPlayerOrPermanents(StackItemView si, PlayerView targetPv) {
            try {
                if (si.getTargetPlayers() != null && si.getTargetPlayers().contains(targetPv)) {
                    return true;
                }
                if (si.getTargetCards() != null) {
                    for (CardView cv : si.getTargetCards()) {
                        if (cv != null && targetPv.equals(cv.getController())) {
                            return true;
                        }
                    }
                }
            } catch (Exception ignored) {
            }
            return false;
        }

        private boolean hasOpponentTarget(StackItemView si, PlayerView selfPv) {
            try {
                if (si.getTargetPlayers() != null) {
                    for (PlayerView pv : si.getTargetPlayers()) {
                        if (pv != null && !pv.equals(selfPv)) return true;
                    }
                }
                if (si.getTargetCards() != null) {
                    for (CardView cv : si.getTargetCards()) {
                        if (cv != null && cv.getController() != null && !cv.getController().equals(selfPv)) {
                            return true;
                        }
                    }
                }
            } catch (Exception ignored) {
            }
            return false;
        }

        @Override
        public Void visit(GameEventPlayerDamaged ev) {
            PlayerView target = ev.target();
            CardView source = ev.source();
            int amt = ev.amount();
            if (amt <= 0 || target == null) return null;

            if (target.equals(heroPlayer.getView())) {
                telemetry.hero_damage_taken += amt;
            } else if (source != null && heroPlayer.getView().equals(source.getController())) {
                if (ev.combat()) {
                    telemetry.hero_combat_damage_dealt += amt;
                    if (source.isCommander()) {
                        telemetry.hero_commander_damage_dealt += amt;
                    }
                } else {
                    telemetry.hero_noncombat_damage_dealt += amt;
                }
            }
            return null;
        }

        public void checkEliminations() {
            for (int i = 0; i < podPlayers.size(); i++) {
                int seat = i + 1;
                if (recordedEliminations.contains(seat)) continue;
                Player p = podPlayers.get(i);
                if (p.hasLost()) {
                    recordedEliminations.add(seat);
                    EliminationRecord er = new EliminationRecord();
                    er.seat = seat;
                    er.player = p.getName();
                    er.deck = viewToDeck.getOrDefault(p.getView(), "Unknown");
                    er.global_turn = currentGlobalTurn;
                    er.hero_turn = Math.max(1, currentHeroTurn);
                    PlayerOutcome po = p.getOutcome();
                    er.reason = (po != null) ? po.toString() : "Lost";
                    telemetry.eliminations.add(er);
                }
            }
        }

        public void finalizeTelemetry(List<String> deckNames) {
            if (!openingHandCaptured) {
                captureOpeningHandsAndTurnOrder();
            }
            updatePodPeaks();
            if (heroTurnActive) {
                recordHeroTurnSnapshot();
                heroTurnActive = false;
            }
            checkEliminations();

            for (int i = 0; i < podPlayers.size(); i++) {
                Player p = podPlayers.get(i);
                int seat = i + 1;
                SeatSummary ss = new SeatSummary();
                ss.seat = seat;
                ss.player = p.getName();
                ss.deck = deckNames.get(i);

                List<Card> cmds = p.getCommanders();
                if (cmds != null && !cmds.isEmpty()) {
                    List<String> cNames = new ArrayList<>();
                    for (Card c : cmds) cNames.add(cleanCardName(c));
                    ss.commander = String.join(" // ", cNames);
                } else {
                    ss.commander = "Unknown";
                }
                if (seat == 1) {
                    telemetry.hero_commander = ss.commander;
                }

                ss.mulligans = (seat == 1) ? telemetry.hero_mulligans : p.getStats().getMulliganCount();
                ss.opening_hand_size = (seat == 1 && telemetry.hero_opening_hand_size > 0)
                        ? telemetry.hero_opening_hand_size
                        : p.getStats().getOpeningHandSize();
                ss.turn_order_pos = seatTurnOrderPos.getOrDefault(seat, seat);
                ss.final_life = p.getLife();
                ss.has_won = p.hasWon();
                ss.has_lost = p.hasLost();
                PlayerOutcome po = p.getOutcome();
                ss.outcome_text = (po != null) ? po.toString() : (ss.has_won ? "Won" : (ss.has_lost ? "Lost" : "Alive at Timeout"));
                ss.commander_casts = p.getTotalCommanderCast();
                ss.commander_cast_turns = seatCmdCastTurns.getOrDefault(seat, new ArrayList<>());
                ss.spells_cast = seatSpellsCast.getOrDefault(seat, 0);
                ss.peak_lands_in_play = seatPeakLands.getOrDefault(seat, 0);
                ss.peak_creatures_in_play = seatPeakCreatures.getOrDefault(seat, 0);
                ss.peak_power_in_play = seatPeakPower.getOrDefault(seat, 0);

                for (Map.Entry<Card, Integer> entry : p.getCommanderDamage()) {
                    if (entry.getKey() != null && entry.getValue() != null && entry.getValue() > 0) {
                        ss.commander_damage_taken.put(cleanCardName(entry.getKey()), entry.getValue());
                    }
                }
                telemetry.seats.add(ss);
            }
        }
    }

    public static class DaemonDeckPayload {
        public String name;
        public String path;
        public String dck_content;
    }

    public static class DaemonJobRequest {
        public String command;
        public String job_id;
        public String deck_dir;
        public List<String> deck_files;
        public List<DaemonDeckPayload> decks;
        public Integer num_games;
        public Integer game_index_start;
        public Integer timeout_sec;
        public Integer ai_timeout_sec;
        public Long base_seed;
        public Boolean smart_mulligan;
    }

    private static Deck resolveDeckFromSpec(String deckDir, String df, DaemonDeckPayload payload, File scratchDir) throws Exception {
        if (payload != null && payload.dck_content != null && !payload.dck_content.trim().isEmpty()) {
            String safeName = (payload.name != null && !payload.name.isEmpty())
                    ? payload.name.replaceAll("[^a-zA-Z0-9_\\-.]", "_")
                    : "temp_deck";
            if (!safeName.endsWith(".dck")) {
                safeName += ".dck";
            }
            if (!scratchDir.exists()) {
                scratchDir.mkdirs();
            }
            File tempFile = new File(scratchDir, UUID.randomUUID().toString().substring(0, 8) + "_" + safeName);
            Files.write(tempFile.toPath(), payload.dck_content.getBytes(StandardCharsets.UTF_8));
            try {
                Deck d = DeckSerializer.fromFile(tempFile);
                return d;
            } finally {
                try {
                    tempFile.delete();
                } catch (Exception ignored) {
                }
            }
        }

        String pathCandidate = (payload != null && payload.path != null && !payload.path.isEmpty()) ? payload.path : df;
        if (pathCandidate == null) {
            return null;
        }
        File f = (deckDir != null && !new File(pathCandidate).isAbsolute())
                ? new File(deckDir, pathCandidate)
                : new File(pathCandidate);
        if (!f.exists() && !pathCandidate.endsWith(".dck")) {
            f = (deckDir != null && !new File(pathCandidate).isAbsolute())
                    ? new File(deckDir, pathCandidate + ".dck")
                    : new File(pathCandidate + ".dck");
        }
        if (!f.exists()) {
            return null;
        }
        return DeckSerializer.fromFile(f);
    }

    public static void executePodBatch(
            String deckDir,
            List<String> deckFiles,
            List<DaemonDeckPayload> deckPayloads,
            int numGames,
            int gameIndexStart,
            int timeoutSec,
            int aiTimeoutSec,
            Long baseSeed,
            boolean smartMull,
            Gson gson
    ) throws Exception {
        useSmartMulligan = smartMull;
        GameType gameType = GameType.Commander;
        GameRules rules = new GameRules(gameType);
        rules.setAppliedVariants(EnumSet.of(gameType));
        rules.setSimTimeout(timeoutSec);

        List<RegisteredPlayer> registeredPlayers = new ArrayList<>();
        List<String> cleanDeckNames = new ArrayList<>();
        File scratchDir = new File(System.getProperty("java.io.tmpdir"), "forgesim_scratch");

        int count = (deckPayloads != null && !deckPayloads.isEmpty()) ? deckPayloads.size() : (deckFiles != null ? deckFiles.size() : 0);
        if (count < 2) {
            throw new IllegalArgumentException("At least 2 decks are required for a Commander pod.");
        }

        for (int i = 0; i < count; i++) {
            String df = (deckFiles != null && i < deckFiles.size()) ? deckFiles.get(i) : null;
            DaemonDeckPayload payload = (deckPayloads != null && i < deckPayloads.size()) ? deckPayloads.get(i) : null;
            Deck deck = resolveDeckFromSpec(deckDir, df, payload, scratchDir);
            if (deck == null) {
                String label = (payload != null && payload.name != null) ? payload.name : String.valueOf(df);
                throw new IllegalArgumentException("Could not load or parse deck for Seat " + (i + 1) + ": " + label);
            }
            int seat = i + 1;
            String dName = deck.getName();
            if ((dName == null || dName.trim().isEmpty()) && payload != null && payload.name != null) {
                dName = payload.name.replace(".dck", "");
            }
            cleanDeckNames.add(dName);
            String aiLabel = "Ai(" + seat + ")-" + dName;
            RegisteredPlayer rp = RegisteredPlayer.forCommander(deck);
            LobbyPlayer lp;
            if (seat == 1) {
                lp = new HeroLobbyPlayerAi(aiLabel, EnumSet.noneOf(AIOption.class));
            } else {
                lp = GamePlayerUtil.createAiPlayer(aiLabel, i, "");
            }
            rp.setPlayer(lp);
            registeredPlayers.add(rp);
        }

        Match match = new Match(rules, registeredPlayers, "CommanderPodTest");

        for (int gIdx = 1; gIdx <= numGames; gIdx++) {
            int reportedIdx = gameIndexStart + gIdx - 1;
            long gameSeed = (baseSeed != null) ? (baseSeed + gIdx - 1) : System.nanoTime();
            MyRandom.setRandom(new Random(gameSeed));

            GameTelemetry telemetry = new GameTelemetry();
            telemetry.game_index = reportedIdx;
            telemetry.seed = gameSeed;
            telemetry.hero_deck = cleanDeckNames.get(0);
            activeTelemetry = telemetry;

            long t0 = System.currentTimeMillis();
            final Game game = match.createGame();
            game.setNoGUIUser();
            game.AI_TIMEOUT = aiTimeoutSec;

            List<Player> podPlayers = new ArrayList<>();
            for (Player p : game.getRegisteredPlayers()) {
                podPlayers.add(p);
            }

            PodTelemetryVisitor visitor = new PodTelemetryVisitor(game, podPlayers, cleanDeckNames, telemetry);
            game.subscribeToEvents(visitor);

            try {
                TimeLimitedCodeBlock.runWithTimeout(new Runnable() {
                    @Override
                    public void run() {
                        match.startGame(game);
                    }
                }, timeoutSec, TimeUnit.SECONDS);
            } catch (TimeoutException te) {
                telemetry.timed_out = true;
                try {
                    game.setGameOver(GameEndReason.Draw);
                } catch (Exception ignored) {
                }
            } catch (Throwable t) {
                telemetry.exception_occurred = true;
                telemetry.error_message = t.getClass().getSimpleName() + ": " + t.getMessage();
                try {
                    game.setGameOver(GameEndReason.Draw);
                } catch (Exception ignored) {
                }
            }

            telemetry.duration_ms = System.currentTimeMillis() - t0;
            visitor.finalizeTelemetry(cleanDeckNames);

            GameOutcome outcome = game.getOutcome();
            if (telemetry.timed_out) {
                telemetry.winner_player = "DRAW (Clock Timeout)";
                telemetry.winner_deck = "DRAW (Clock Timeout)";
                telemetry.winner_seat = 0;
                telemetry.win_reason = "Clock Timeout (" + timeoutSec + "s)";
            } else if (outcome != null && !outcome.isDraw() && outcome.getWinningLobbyPlayer() != null) {
                String winName = outcome.getWinningLobbyPlayer().getName();
                telemetry.winner_player = winName;
                int winSeat = 0;
                String winDeck = "Unknown";
                for (int i = 0; i < podPlayers.size(); i++) {
                    if (podPlayers.get(i).getName().equals(winName)) {
                        winSeat = i + 1;
                        winDeck = cleanDeckNames.get(i);
                        break;
                    }
                }
                telemetry.winner_seat = winSeat;
                telemetry.winner_deck = winDeck;
                telemetry.win_reason = (outcome.getWinCondition() != null) ? outcome.getWinCondition().name() : "AllOpponentsLost";
            } else {
                telemetry.winner_player = "DRAW";
                telemetry.winner_deck = "DRAW";
                telemetry.winner_seat = 0;
                telemetry.win_reason = "Draw";
            }

            System.out.println("TELEMETRY_GAME_JSON:" + gson.toJson(telemetry));
            System.out.flush();
        }
    }

    public static void main(String[] args) {
        System.setProperty("java.awt.headless", "true");
        System.setProperty("java.util.Arrays.useLegacyMergeSort", "true");
        System.setProperty("sun.java2d.d3d", "false");

        String deckDir = null;
        List<String> deckFiles = new ArrayList<>();
        int numGames = 1;
        int timeoutSec = 90;
        int aiTimeoutSec = 2;
        Long baseSeed = null;
        boolean daemonMode = false;

        for (int i = 0; i < args.length; i++) {
            String a = args[i];
            if ("-D".equals(a) && i + 1 < args.length) {
                deckDir = args[++i];
            } else if ("-d".equals(a)) {
                while (i + 1 < args.length && !args[i + 1].startsWith("-")) {
                    deckFiles.add(args[++i]);
                }
            } else if ("-n".equals(a) && i + 1 < args.length) {
                numGames = Integer.parseInt(args[++i]);
            } else if ("-c".equals(a) && i + 1 < args.length) {
                timeoutSec = Integer.parseInt(args[++i]);
            } else if ("-ai".equals(a) && i + 1 < args.length) {
                aiTimeoutSec = Integer.parseInt(args[++i]);
            } else if ("-s".equals(a) && i + 1 < args.length) {
                baseSeed = Long.parseLong(args[++i]);
            } else if ("-stockMulligan".equals(a)) {
                useSmartMulligan = false;
            } else if ("-smartMulligan".equals(a)) {
                useSmartMulligan = true;
            } else if ("-daemon".equals(a) || "--daemon".equals(a)) {
                daemonMode = true;
            }
        }

        if (!daemonMode && deckFiles.size() < 2) {
            System.err.println("Usage: ForgePodRunner [-daemon] | [-D <deckDir> -d <Hero.dck> <Opp1.dck> <Opp2.dck> <Opp3.dck> [-n <games>] [-c <timeoutSec>] [-s <seed>] [-smartMulligan|-stockMulligan]]");
            System.exit(1);
        }

        GuiBase.setInterface(new GuiDesktop());
        ExceptionHandler.registerErrorHandling();
        FModel.initialize(null, null);
        Gson gson = new Gson();

        if (daemonMode) {
            System.out.println("FORGE_DAEMON_READY");
            System.out.flush();
            BufferedReader reader = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
            String line;
            try {
                while ((line = reader.readLine()) != null) {
                    line = line.trim();
                    if (line.isEmpty()) {
                        continue;
                    }
                    String jobId = "unknown";
                    try {
                        DaemonJobRequest req = gson.fromJson(line, DaemonJobRequest.class);
                        if (req == null) {
                            continue;
                        }
                        if ("shutdown".equalsIgnoreCase(req.command) || "quit".equalsIgnoreCase(req.command)) {
                            break;
                        }
                        if ("ping".equalsIgnoreCase(req.command)) {
                            System.out.println("FORGE_DAEMON_PONG");
                            System.out.flush();
                            continue;
                        }
                        if (req.job_id != null) {
                            jobId = req.job_id;
                        }
                        String jDeckDir = (req.deck_dir != null) ? req.deck_dir : deckDir;
                        int jGames = (req.num_games != null && req.num_games > 0) ? req.num_games : 1;
                        int jStart = (req.game_index_start != null && req.game_index_start > 0) ? req.game_index_start : 1;
                        int jTimeout = (req.timeout_sec != null && req.timeout_sec > 0) ? req.timeout_sec : timeoutSec;
                        int jAiTimeout = (req.ai_timeout_sec != null && req.ai_timeout_sec > 0) ? req.ai_timeout_sec : aiTimeoutSec;
                        boolean jSmart = (req.smart_mulligan != null) ? req.smart_mulligan : useSmartMulligan;

                        executePodBatch(
                                jDeckDir,
                                req.deck_files,
                                req.decks,
                                jGames,
                                jStart,
                                jTimeout,
                                jAiTimeout,
                                req.base_seed,
                                jSmart,
                                gson
                        );

                        Map<String, Object> doneMsg = new LinkedHashMap<>();
                        doneMsg.put("job_id", jobId);
                        doneMsg.put("status", "ok");
                        doneMsg.put("games", jGames);
                        System.out.println("FORGE_JOB_DONE:" + gson.toJson(doneMsg));
                        System.out.flush();
                    } catch (Throwable jobErr) {
                        Map<String, Object> errMsg = new LinkedHashMap<>();
                        errMsg.put("job_id", jobId);
                        errMsg.put("status", "error");
                        errMsg.put("error", jobErr.getClass().getSimpleName() + ": " + jobErr.getMessage());
                        System.out.println("FORGE_JOB_ERROR:" + gson.toJson(errMsg));
                        System.out.flush();
                    }
                }
            } catch (Exception ioEx) {
                System.err.println("Daemon loop exited: " + ioEx.getMessage());
            }
            System.exit(0);
        } else {
            try {
                executePodBatch(
                        deckDir,
                        deckFiles,
                        null,
                        numGames,
                        1,
                        timeoutSec,
                        aiTimeoutSec,
                        baseSeed,
                        useSmartMulligan,
                        gson
                );
            } catch (Throwable t) {
                System.err.println("ERROR: " + t.getMessage());
                t.printStackTrace(System.err);
                System.exit(2);
            }
            System.exit(0);
        }
    }
}
