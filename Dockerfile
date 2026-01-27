# syntax=docker/dockerfile:1.4
# This ARG allows you to specify the Python base image version at build time
ARG PYTHON_VERSION=3.11-alpine
# NEW ARG: Use the version detected by your build_pyz.py script as a default.
ARG PYHABITAT_VERSION

##########################################
# STAGE 1: THE BUILDER (Heavy Dependencies)
##########################################
# We use this stage to run the build script and create the self-contained PYZ file.
FROM python:${PYTHON_VERSION} AS builder

# Set the working directory for the application
WORKDIR /app

# Install system packages needed for the build process (git, bash, curl, etc.)
RUN apk update \
    && apk upgrade \
    && apk add --no-cache bash curl git \
    && rm -rf /var/cache/apk/*

# Copy the entire project source tree (needed to run the build_pyz.py script)
COPY . .

# Install build dependencies (setuptools/wheel) and the project itself
RUN pip install -e . 

# Run the build script to create the single PYZ executable and make it executable.
# The filename is now constructed dynamically using the build argument.

RUN python build_pyz.py \
    && chmod +x ./dist/zipapp/pyhabitat-*.pyz \
    && mv $(ls ./dist/zipapp/pyhabitat-*.pyz | head -n 1) ./dist/pyhabitat-latest.pyz
##########################################
# STAGE 2: THE FINAL IMAGE (Minimal Runtime)
##########################################
# Start from the minimal Python runtime image again
FROM python:${PYTHON_VERSION}

# FIX: PROMOTE ARG TO ENV HERE (Re-added for Stage 2 as well)
# This ensures the COPY command in this stage also has access to the variable.
ENV PYHABITAT_VERSION=${PYHABITAT_VERSION}

# Set the working directory for consistency
WORKDIR /app

# Use a wildcard to find the PYZ, then rename it to just 'pyhabitat' in the destination
COPY --from=builder /app/dist/pyhabitat-latest.pyz /usr/local/bin/pyhabitat

# Expose ports (still placeholder, but kept for consistency)
EXPOSE 8000

# Set the entry point to the final CLI executable
# This is how the user runs the application: docker run pyhabitat:tag --help
ENTRYPOINT ["/usr/local/bin/pyhabitat"]


# Make the container available as a GitHub Package
LABEL org.opencontainers.image.source=https://github.com/city-of-memphis-wastewater/pyhabitat
# Add description for GHCR visibility
LABEL org.opencontainers.image.description="A lightweight, multi-architecture command-line tool for runtime and environment introspection."
