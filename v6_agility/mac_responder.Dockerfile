# mac_responder.Dockerfile -- minimal Linux image to run the v6 SM-PQ-WireGuard
# daemon as the *responder* on a macOS host (the binary is Linux-only, so the
# Mac must run it inside a container). Builds the hybrid binary + keygen helper
# and ships the runtime tools needed to bring up the tunnel.
#
# Build (from artifacts_implementation/, so the build context has Cargo.toml/src):
#   cd workspace/v6_agility/artifacts_implementation
#   docker build -f ../mac_responder.Dockerfile -t smwg-responder .
#
# Run (publishes UDP 51820 on the Mac so the WSL initiator can reach it):
#   docker run -it --rm --name smwg \
#     --cap-add NET_ADMIN --device /dev/net/tun \
#     -p 51820:51820/udp \
#     smwg-responder bash
#
FROM rust:1-bookworm

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        cmake clang build-essential pkg-config libssl-dev \
        netcat-openbsd iproute2 iputils-ping xxd iperf3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
# Build context is artifacts_implementation/ -- copy the whole crate in.
COPY . .

# Build the hybrid daemon and the keygen helper (oqs/Classic McEliece compile
# from source via cmake here, so this layer takes a few minutes the first time).
RUN cargo build --release --features hybrid \
 && cargo build --release --features hybrid --example keygen_hybrid

# target/release/wireguard-rs-pq          -- the daemon
# target/release/examples/keygen_hybrid   -- prints "<priv_hex> <pub_hex>"
