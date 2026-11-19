"""THIRD-PARTY-NOTICES.txt for the release firmware: each component linked or frozen into it, with its license.

    .venv/bin/python pico/release/notices.py MICROPYTHON_DIR BITWASM_SIGNER_DIR > THIRD-PARTY-NOTICES.txt

Run from the repository root. A component added to the firmware is added here too.
"""
import glob
import os
import sys

import urtypes

MPY, BWS = sys.argv[1], sys.argv[2]
LIC = "pico/release/licenses/"


def read(path, lines=None):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return "\n".join(text.splitlines()[lines[0]:lines[1]]) if lines else text.strip()


def header(path, end):
    # A file whose notice is only its header comment: the comment up to `end` lines
    return read(path, (0, end))


URTYPES_LICENSE = glob.glob(os.path.join(os.path.dirname(os.path.dirname(urtypes.__file__)), "urtypes-*.dist-info/licenses/LICENSE*"))[0]

COMPONENTS = [
    ("SeedSigner, and this port of it to the Pico (the seedsigner-icons font included)", "MIT", read("LICENSE.md")),
    ("MicroPython", "MIT", read(f"{MPY}/LICENSE")),
    ("micropython-lib: hmac, base64, zlib, datetime, os.path", "MIT", read(f"{MPY}/lib/micropython-lib/LICENSE")),
    ("Raspberry Pi Pico SDK", "BSD-3-Clause", read(f"{MPY}/lib/pico-sdk/LICENSE.TXT")),
    ("littlefs", "BSD-3-Clause", "Copyright (c) 2022, The littlefs authors.\nCopyright (c) 2017, Arm Limited. All rights reserved.\n\n"
     + read(LIC + "BSD-3-Clause.txt")),
    ("FatFs (MicroPython's ooFatFs)", "BSD-1-Clause", header(f"{MPY}/lib/oofatfs/ff.c", 23)),
    ("Mbed TLS", "Apache-2.0", read(f"{MPY}/lib/mbedtls/LICENSE")),
    ("bitwasm-signer: the signer, parser-no-ur.wasm, the Python host and the QR reader", "MIT", read(f"{BWS}/LICENSE")),
    ("libsecp256k1", "MIT", read(f"{BWS}/third_party/secp256k1/COPYING")),
    ("WebAssembly Micro Runtime (WAMR)", "Apache-2.0 WITH LLVM-exception", read(f"{BWS}/third_party/wasm-micro-runtime/LICENSE")),
    ("micropython-pil", "MIT", read("pico/third_party/micropython-pil/LICENSE")),
    ("QR Code generator library (C), in micropython-pil", "MIT", header("pico/third_party/micropython-pil/cmod/gfx/qrcodegen.c", 22)),
    ("Rust's core and compiler_builtins libraries", "MIT OR Apache-2.0",
     "Copyright (c) The Rust Project Contributors\n\n" + read(LIC + "MIT.txt")),
    ("ur2 (Foundation Devices' UR implementation, in SeedSigner)", "BSD-2-Clause-Patent", read("src/seedsigner/helpers/ur2/LICENSE")),
    ("urtypes", "MIT", read(URTYPES_LICENSE)),
    ("seedsigner-translations", "MIT", read("src/seedsigner/resources/seedsigner-translations/LICENSE")),
    ("Open Sans font", "Apache-2.0", "Digitized data copyright (c) 2010-2011, Google Corporation.\n\n"
     "Licensed under the Apache License, Version 2.0: its text is under Mbed TLS above."),
    ("Inconsolata font", "OFL-1.1",
     "Copyright 2006 The Inconsolata Project Authors (https://github.com/cyrealtype/Inconsolata)\n\n" + read(LIC + "OFL-1.1.txt")),
    ("Font Awesome 6 Free (Solid) font", "OFL-1.1", "Copyright (c) Font Awesome (https://fontawesome.com)\n\n"
     "Licensed under the SIL Open Font License, Version 1.1: its text is under Inconsolata above."),
    ("Arm GNU Toolchain runtime: newlib's C and math libraries, libgcc", "newlib's licenses; GPL-3.0 WITH GCC-exception-3.1",
     "newlib is under a set of BSD-style and similar licenses, listed in its COPYING.NEWLIB:\n"
     "https://sourceware.org/git/?p=newlib-cygwin.git;a=blob;f=COPYING.NEWLIB\n"
     "libgcc is under the GPL with the GCC Runtime Library Exception, which puts no terms on the firmware built with it."),
]

print("Third-party software in the SeedSigner Pico 2 release firmware\n")
for name, spdx, _ in COMPONENTS:
    print(f"- {name} ({spdx})")
for name, spdx, text in COMPONENTS:
    print("\n" + "=" * 100 + f"\n{name} ({spdx})\n" + "=" * 100 + "\n\n" + text)
