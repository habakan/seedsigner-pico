#!/bin/bash
# The release build of one commit from a fresh clone, as pico/README.md builds it, into /out with its SHA-256
set -euo pipefail
COMMIT=${1:?usage: build-release <commit>}
mkdir -p /work && cd /work
git clone -q https://github.com/habakan/seedsigner-pico
cd seedsigner-pico && git checkout -q "$COMMIT"
git submodule update -q --init pico/third_party/micropython-pil src/seedsigner/resources/seedsigner-translations
uv venv -q -p 3.12.10 .venv && uv pip install -q -p .venv/bin/python -r requirements.txt
uv pip install -q -p .venv/bin/python mpremote babel==2.16.0 setuptools
.venv/bin/python setup.py -q compile_catalog
git clone -q --depth 1 -b v1.29.0 https://github.com/micropython/micropython build/micropython
# v1.29.0's commit, as a tag can be moved
test "$(git -C build/micropython rev-parse HEAD)" = 0fd6c573ea815774668bbb16b8e197c8822368b2
make -s -C build/micropython/mpy-cross
# bitwasm-signer at the commit pico/README.md pins
git clone -q https://github.com/bitwasm-project/bitwasm-signer ../bitwasm-signer
(cd ../bitwasm-signer && git checkout -q --detach 5cd14a1e166045a037c5585f5f24b813c6695e48 && make deps wamr-deps > /dev/null)
export PICO_TOOLCHAIN_PATH=/opt/arm-toolchain
make -s -C build/micropython/ports/rp2 BOARD=RPI_PICO2 submodules > /dev/null
make -C pico rp2-release BITWASM_SIGNER=$PWD/../bitwasm-signer > /out/build.log 2>&1
B=build/micropython/ports/rp2/build-SEEDSIGNER_PICO2
cp $B/firmware.bin $B/firmware.elf $B/firmware.uf2 /out/
cd /out && sha256sum firmware.bin firmware.uf2 | tee SHA256SUMS
