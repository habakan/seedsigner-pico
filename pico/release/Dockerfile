# The reference environment for the release build: Linux x86_64 with Arm GNU Toolchain 14.2.Rel1's Linux package.
# Arm's macOS package ships different libm/libc/libgcc builds, so a release is checked against this one.
#
#   docker build --platform linux/amd64 -t seedsigner-pico-release pico/release
#   docker run --rm --platform linux/amd64 -v "$PWD/out:/out" seedsigner-pico-release <commit>
FROM ubuntu:24.04@sha256:73b999393d07f2bf65a40373778a44dc9a6d54ad7718d29247d8ff9413c4d6a8

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential ca-certificates cmake curl git python3 xz-utils \
    && rm -rf /var/lib/apt/lists/*

ARG ARM_TOOLCHAIN=arm-gnu-toolchain-14.2.rel1-x86_64-arm-none-eabi
ARG ARM_SHA256=62a63b981fe391a9cbad7ef51b17e49aeaa3e7b0d029b36ca1e9c3b2a9b78823
RUN curl -fsSLo /tmp/arm.tar.xz https://developer.arm.com/-/media/Files/downloads/gnu/14.2.rel1/binrel/$ARM_TOOLCHAIN.tar.xz \
    && echo "$ARM_SHA256  /tmp/arm.tar.xz" | sha256sum -c - \
    && mkdir -p /opt/arm-toolchain && tar xJf /tmp/arm.tar.xz -C /opt/arm-toolchain --strip-components=1 \
    && rm /tmp/arm.tar.xz

COPY --from=ghcr.io/astral-sh/uv:0.6.17@sha256:4a6c9444b126bd325fba904bff796bf91fb777bf6148d60109c4cb1de2ffc497 /uv /usr/local/bin/uv
# rustup only: qr_reader's rust-toolchain.toml pins the Rust it builds with
RUN curl -fsSL https://sh.rustup.rs | sh -s -- -y --profile minimal --default-toolchain none
ENV PATH=/root/.cargo/bin:$PATH

COPY build.sh /usr/local/bin/build-release
ENTRYPOINT ["build-release"]
