# Secure boot on the Pico 2: decide before you burn

The RP2350 can be told, in its OTP, to run only firmware signed by one key. That cannot be undone. Read this
page before writing anything to OTP, and if in doubt, don't: everything except the last step can be taken back.

## Don't use secure boot if

- **you develop on this board**, or want to try changes, your own builds or someone else's. A secured Pico runs
  only images signed by the key whose hash it holds.
- **you want updates the key holder has not signed.** A fix on `main` reaches a secured Pico only when that key
  signs a release with it.
- **you cannot keep the key**, if it is yours. Lose it and the board can never be updated again (it keeps
  running what it has). If it leaks, anyone can make firmware the board will run.
- **you may want the development build back**, the RISC-V cores, or SWD to recover the board. A secured Pico
  cannot boot unsigned code, and with debug disabled SWD is gone too.

For all of these, use the release build without OTP (below), or keep a second Pico for development. A Pico 2
costs little next to a board you cannot change.

## The four kinds of board

| | build | USB REPL | runs | reversible |
|---|---|---|---|---|
| development | `make -C pico rp2` | yes | anything | yes |
| release | `make -C pico rp2-release` | no | anything | yes, flash another build in BOOTSEL mode |
| signed release, blank OTP | `make -C pico rp2-release-signed KEY=...` | no | anything; the signature is not checked | yes |
| secured | a signed release, plus the key's hash and secure boot written to OTP | no | only images signed by that key, at or above its rollback version | **no** |

A secured Pico still enters BOOTSEL mode and takes any UF2, but boots only a correctly signed one.

## If you do use it

1. **Run the release build first**, for long enough to know you want this board as a signer and nothing else.
2. **Choose whose key.** Writing a release's `otp.json` ties the board to whoever signed that release. Writing
   your own key's hash means you build and sign every update yourself.
3. **Check what you install.** The release builds to the same bytes from the same commit:
   `pico/release/Dockerfile` builds it from a fresh clone, and a signed image is that build plus a block at the
   end and a 4-byte link to it (`pico/README.md`, "Build one").
4. **Write OTP**, with the signed image's `otp.json` (the key's hash, secure boot on), with the board in BOOTSEL
   mode: `picotool otp load otp.json`. Then flash the signed UF2. The datasheet also recommends marking the
   unused key slots invalid (`BOOT_FLAGS1.KEY_INVALID`), so that no one can add a key later. Disabling debug
   (`CRIT1.DEBUG_DISABLE`) is a separate, also permanent, choice: it closes SWD, which could otherwise read the
   seed from RAM.

This project has not yet secured a board itself; the steps above follow Raspberry Pi's RP2350 datasheet
(sections 5.10.1, "Secure boot", and 10.5, "Secure boot enable procedure") and picotool, and will be updated
when it has.

## Updates afterwards

Flash each new signed UF2 in BOOTSEL mode as before. Each image carries a rollback version (`ROLLBACK`, 1 by
default); once a secured Pico boots one, it records it in OTP itself and refuses any image with a lower one.
The version goes up only when older releases should stop booting, such as after a security fix.
