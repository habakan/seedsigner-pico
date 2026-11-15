# SeedSigner on the Raspberry Pi Pico 2

> [!NOTE]
> **An unofficial fork of [SeedSigner](https://github.com/SeedSigner/seedsigner).** Nearly all of the code here
> is the SeedSigner project's, written by [its contributors](https://github.com/SeedSigner/seedsigner/graphs/contributors),
> which is why they fill this repository's contributor list. This fork adds the Pico 2 port on top. It is not
> affiliated with the SeedSigner project and not a proposal to merge; for SeedSigner itself, go to
> [SeedSigner/seedsigner](https://github.com/SeedSigner/seedsigner) and [seedsigner.com](https://seedsigner.com).

SeedSigner's own Python, running on an RP2350 with 520 KB of RAM instead of a Raspberry Pi Zero: the same
screens and flows, with the camera, a 240x240 screen, a joystick and three keys. Each signed PSBT is the
same bytes upstream SeedSigner produces.

https://github.com/user-attachments/assets/372af8fe-e810-4cb7-9dda-7da3a6c179f7

- [pico/README.md](pico/README.md): what works, what was measured, how it differs from upstream, and how to
  build one
- [docs/pico.md](docs/pico.md): the engineering record, parts and wiring included
- A signet spend signed on the device through the camera:
  [43980b4e…](https://mempool.space/signet/tx/43980b4e4e75da68c2f9181fea3864603cc0d145885d42072cfa7c5d3e403a1a)

The rest of the tree is SeedSigner's, kept close to its `dev` branch so its changes can still be merged in.
The port is the commits on top of it: [all of them in one diff](https://github.com/habakan/seedsigner-pico/compare/ada81cd...main).
SeedSigner's own README is [upstream's](https://github.com/SeedSigner/seedsigner/blob/dev/README.md).

MIT, as SeedSigner ([LICENSE.md](LICENSE.md)).
