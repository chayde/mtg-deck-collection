# ==============================================================================
# Dockerfile — MTG Forge 4-AI Pod Simulation Cluster Daemon (forgesim.chayde.lab)
# ==============================================================================
FROM eclipse-temurin:17-jdk-jammy

ENV DEBIAN_FRONTEND=noninteractive
ARG FORGE_VERSION=2.0.15

# Install Python 3, curl, bzip2, git, and headless AWT font dependencies required by Forge
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    ca-certificates \
    curl \
    bzip2 \
    git \
    libfreetype6 \
    fontconfig \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Download and unpack official MTG Forge release into /opt/forge
WORKDIR /opt/forge
RUN curl -fSL "https://github.com/Card-Forge/forge/releases/download/forge-${FORGE_VERSION}/forge-installer-${FORGE_VERSION}.tar.bz2" -o /tmp/forge.tar.bz2 \
    && tar -xjf /tmp/forge.tar.bz2 -C /opt/forge \
    && rm -f /tmp/forge.tar.bz2 \
    && rm -rf /opt/forge/adventure-editor* /opt/forge/forge-gui-mobile* /opt/forge/res/music /opt/forge/res/sound

# Copy cluster application, version manifest & Java telemetry bridge into /app
WORKDIR /app
COPY version.json /app/version.json
COPY ForgePodRunner.java /app/ForgePodRunner.java
COPY forgesim_server.py /app/forgesim_server.py

# Pre-compile ForgePodRunner.java during image build
RUN mkdir -p /app/build \
    && javac --release 17 -cp "/opt/forge/forge-gui-desktop-${FORGE_VERSION}-jar-with-dependencies.jar" -d /app/build /app/ForgePodRunner.java

ENV FORGE_DIR=/opt/forge
ENV PORT=8080
ENV WORKERS=10
ENV WORKER_HEAP_MB=1536

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=45s --retries=3 \
    CMD curl -fsS http://localhost:8080/health || exit 1

CMD ["python3", "/app/forgesim_server.py"]
