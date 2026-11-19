# Security policy for this Pico port

This repository is a port of SeedSigner to the Raspberry Pi Pico 2, not SeedSigner itself. The `SECURITY.md` at its
root is upstream's: please don't use it for this port, so that SeedSigner's maintainers are not sent reports about code
they do not ship.

## Reporting a vulnerability

Please don't open a public issue. Report it privately through GitHub:
https://github.com/habakan/seedsigner-pico/security/advisories/new

Include the release or commit, what an attacker can do, and how to reproduce it.

- A flaw in `bitwasm-signer` itself (the signer, the PSBT parser): https://github.com/bitwasm-project/bitwasm-signer/security/advisories/new
- A flaw that is also in upstream SeedSigner, in code this port has not changed: upstream's policy applies, in the
  root `SECURITY.md`. If you are not sure which it is, report it here and it will be passed on.

## Releases

This port's releases are not signed with `seedsigner_pubkey.gpg`, which is upstream's key. Each release carries the
SHA-256 of its files, and a signed image's signature can be checked with `picotool info -a`; `pico/README.md` says how
to rebuild a release from its commit and compare.
