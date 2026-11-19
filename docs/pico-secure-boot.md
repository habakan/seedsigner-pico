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
2. **Check the chip's stepping.** The development build's REPL shows it: `machine.mem32[0x40000000] >> 28` is 2
   on RP2350 A2 and 3 after it, and the bootrom's version byte, `machine.mem8[0x13]`, is 4 on A4. On A2, fault injection (glitching the supply at boot) has been shown to
   bypass secure boot, in Raspberry Pi's 2024 hacking challenge and since; A4 fixes most of what was published
   by mid-2025. On an A2 board, secure boot still stops someone swapping the firmware in a few minutes with a USB
   cable, but not someone with the board, time and glitching equipment.
3. **Use your own key.** Releases ship no OTP values. Rebuild the release with `pico/release/Dockerfile` and sign
   its `out/firmware.elf` with your key, as `make -C pico rp2-release-signed` does; you then sign every update you
   install yourself.
4. **Check what you install.** The release builds to the same bytes from the same commit:
   `pico/release/Dockerfile` builds it from a fresh clone, and a signed image is that build plus a block at the
   end and links to it (`pico/README.md`, "Build one").
5. **Flash the signed UF2 before writing OTP**, and use it: a board with blank OTP runs it like any other build.
6. **Check the key's hash.** `picotool seal` writes it to `otp.json` as `bootkey0`. Compare it with the public
   key that `picotool info -a firmware-signed.uf2` shows (`echo -n <public key> | xxd -r -p | shasum -a 256`), and
   with your key's own (`openssl ec -in key.pem -pubout -conv_form uncompressed -outform DER | tail -c 64 |
   shasum -a 256`). A wrong hash leaves a secured board unable to boot anything.
7. **Write OTP in two stages**, with the board in BOOTSEL mode. Field by field rather than `picotool otp load`
   with a hand-edited `otp.json`, so that a misspelt name fails before it writes; `picotool otp get` reads each
   one back, and picotool writes every redundant copy of a row itself.

   First what does not secure the board yet, so that a mistake here still leaves it booting:
   ```sh
   python3 -c "import json; json.dump({'bootkey0': json.load(open('otp.json'))['bootkey0']}, open('key.json', 'w'))"
   picotool otp load key.json                               # the key's hash, into slot 0
   picotool otp set OTP_DATA_BOOT_FLAGS1.KEY_VALID 1        # slot 0
   picotool otp set OTP_DATA_BOOT_FLAGS1.KEY_INVALID 0xe    # slots 1 to 3, so that no key can be added later
   picotool otp set OTP_DATA_BOOT_FLAGS0.DISABLE_BOOTSEL_UART_BOOT 1
   picotool otp set OTP_DATA_BOOT_FLAGS0.DISABLE_OTP_BOOT 1
   picotool otp set OTP_DATA_BOOT_FLAGS0.DISABLE_SRAM_WINDOW_BOOT 1
   picotool otp set OTP_DATA_CRIT1.GLITCH_DETECTOR_ENABLE 1
   picotool otp get -z BOOTKEY0                             # the hash, two bytes a row, little-endian
   ```
   Boot the signed UF2 once like this (`picotool reboot`), and check the screen stays on the main menu: the
   glitch detector resets the chip on an abnormal supply or clock, and should not on yours.

   Then, in BOOTSEL mode again, what cannot be undone:
   ```sh
   picotool otp set OTP_DATA_CRIT1.DEBUG_DISABLE 1          # SWD closed: it could read the seed from RAM
   picotool otp set OTP_DATA_CRIT1.SECURE_DEBUG_DISABLE 1
   picotool otp set OTP_DATA_CRIT1.SECURE_BOOT_ENABLE 1     # also turns the RISC-V cores off for good
   ```
8. **Check it.** `picotool info -d` says `secure boot: 1` and `debug enable: 0`. The signed UF2 boots; the
   unsigned `firmware.uf2` does not, and the board comes back in BOOTSEL mode (flash the signed one again). After
   the first signed boot, `picotool otp get -r 0x4e` reads 1, the rollback version.
9. **Last, optionally, close picotool's interface**:
   `picotool otp set OTP_DATA_BOOT_FLAGS0.DISABLE_BOOTSEL_USB_PICOBOOT_IFC 1`. From the next BOOTSEL entry no one
   can write more OTP bits over USB (a stray `KEY_INVALID` bit for slot 0 would brick the board) or read memory;
   updates still work by copying a UF2 to the BOOTSEL drive, and picotool no longer sees the board at all.

Never lock OTP page 1 (datasheet section 13.5, "Page locks"): the board counts its rollback version there, rows
0x04e to 0x053.

These steps were done in this order on one board, an RP2350 A2, on 2026-11-19, following Raspberry Pi's RP2350
datasheet (sections 5.10.1, "Secure boot", and 10.5, "Secure boot enable procedure").

## Updates afterwards

Flash each new signed UF2 in BOOTSEL mode as before. Each image carries a rollback version (`ROLLBACK`, 1 by
default); once a secured Pico boots one, it records it in OTP itself and refuses any image with a lower one.
The version goes up only when older releases should stop booting, such as after a security fix.
