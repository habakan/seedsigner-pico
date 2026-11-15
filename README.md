# SeedSigner on the Raspberry Pi Pico 2

SeedSigner's own Python, running on a $5 RP2350 with 520 KB of RAM instead of a Raspberry Pi Zero: the same
screens and flows, with the camera, a 240x240 screen, a joystick and three keys. Each signed PSBT is the
same bytes upstream SeedSigner produces.

This is an unofficial fork, not affiliated with the SeedSigner project and not a proposal to merge. For
SeedSigner itself, go to [SeedSigner/seedsigner](https://github.com/SeedSigner/seedsigner) and
[seedsigner.com](https://seedsigner.com).

- [pico/README.md](pico/README.md): what works, what was measured, how it differs from upstream, and how to
  build one
- [docs/pico.md](docs/pico.md): the engineering record, parts and wiring included
- A signet spend signed on the device through the camera:
  [43980b4e…](https://mempool.space/signet/tx/43980b4e4e75da68c2f9181fea3864603cc0d145885d42072cfa7c5d3e403a1a)

The rest of the tree is SeedSigner's, kept close to its `dev` branch so its changes can still be merged in.
The port is the commits on top of it: [all of them in one diff](https://github.com/habakan/seedsigner-pico/compare/ada81cd...main).
SeedSigner's own README is [upstream's](https://github.com/SeedSigner/seedsigner/blob/dev/README.md).

MIT, as SeedSigner ([LICENSE.md](LICENSE.md)).
