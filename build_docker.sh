docker buildx build \
    --platform linux/amd64,linux/arm64 \
    -t ghcr.io/city-of-memphis-wastewater/pyhabitat:multi-dev \
    -f Dockerfile.multi-dev . \
    --push