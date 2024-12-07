# CHANGELOG


## v0.5.0 (2024-12-07)

### Features

- Allow more pyav versions ([#5](https://github.com/tutorintelligence/vpx-rtp-py/pull/5),
  [`d64cdab`](https://github.com/tutorintelligence/vpx-rtp-py/commit/d64cdab9b071c87b13bc49e83df8689cc5a71864))


## v0.4.0 (2024-06-24)

### Features

- **jitter**: Report sequence numbers in JitterFrame
  ([`95df488`](https://github.com/tutorintelligence/vpx-rtp-py/commit/95df48826fda06a436af3a1d38962c5e03435b19))


## v0.3.5 (2024-06-05)

### Bug Fixes

- **stats**: Allow access to default values before first packet
  ([#4](https://github.com/tutorintelligence/vpx-rtp-py/pull/4),
  [`1ed39c8`](https://github.com/tutorintelligence/vpx-rtp-py/commit/1ed39c8d0b2281e6133a9a3e829fbfcc7a77013c))

* Revert "fix: Need a change to generate a new package"

This reverts commit 7cec89b646f7747043b372025050729ae2459600.

* Revert "refactor(stats): Adopt functional style and satisfy mypy"

This reverts commit 1263b787dcc5855a2d18cc0729d6ec028fff6981.

* Satisfy mypy


## v0.3.4 (2024-06-05)

### Bug Fixes

- Need a change to generate a new package
  ([`7cec89b`](https://github.com/tutorintelligence/vpx-rtp-py/commit/7cec89b646f7747043b372025050729ae2459600))

### Chores

- Add missing import and reformat
  ([`9e74133`](https://github.com/tutorintelligence/vpx-rtp-py/commit/9e74133090a5315765fbbeb2791383dc73e2b712))

### Refactoring

- **stats**: Adopt functional style and satisfy mypy
  ([`1263b78`](https://github.com/tutorintelligence/vpx-rtp-py/commit/1263b787dcc5855a2d18cc0729d6ec028fff6981))


## v0.3.3 (2024-06-05)

### Bug Fixes

- **stats**: Add missing imports
  ([`239144c`](https://github.com/tutorintelligence/vpx-rtp-py/commit/239144c6651c9aeb7ace888142cb0ecded31fbf7))


## v0.3.2 (2024-06-04)

### Bug Fixes

- Clock rate import path
  ([`59b89b9`](https://github.com/tutorintelligence/vpx-rtp-py/commit/59b89b983061e76000909fef29885267a97ae51a))

### Documentation

- Add comments for stats properties
  ([`601d47b`](https://github.com/tutorintelligence/vpx-rtp-py/commit/601d47b07a7ce0af94d2f785a217caf6d122c31c))


## v0.3.1 (2024-06-04)

### Bug Fixes

- Remove undefined function
  ([`a77576b`](https://github.com/tutorintelligence/vpx-rtp-py/commit/a77576bb1fe6627b4de69c421a9986914b8d92ef))


## v0.3.0 (2024-06-04)

### Chores

- Update black and sort out dev deps ([#2](https://github.com/tutorintelligence/vpx-rtp-py/pull/2),
  [`504ee90`](https://github.com/tutorintelligence/vpx-rtp-py/commit/504ee90f7d43f66e6299ecf3c838bc8e93e7172a))

### Features

- Add utils for received stream stats ([#3](https://github.com/tutorintelligence/vpx-rtp-py/pull/3),
  [`119f279`](https://github.com/tutorintelligence/vpx-rtp-py/commit/119f2795c38f806580147c0398cd4d439b8e5a64))

* feat: Add received stream stats

* feat: Make constructor parameter implicit


## v0.2.2 (2024-06-04)

### Bug Fixes

- Some docs ([#1](https://github.com/tutorintelligence/vpx-rtp-py/pull/1),
  [`97b906b`](https://github.com/tutorintelligence/vpx-rtp-py/commit/97b906b6e21a5e36005dbdc619179e67e5b41ff4))

### Documentation

- Improve readme
  ([`f956e5c`](https://github.com/tutorintelligence/vpx-rtp-py/commit/f956e5c8fabd135f217517947e0ab408c10aa493))


## v0.2.1 (2024-06-02)

### Bug Fixes

- Remove min/max bitrates from vp8/9 encoder
  ([`4d65fb6`](https://github.com/tutorintelligence/vpx-rtp-py/commit/4d65fb6898860ef7b3da3250a6292b428437d048))


## v0.2.0 (2024-06-02)

### Features

- Vp9 encoding by default
  ([`688821a`](https://github.com/tutorintelligence/vpx-rtp-py/commit/688821ae53f917c3b85e833443eac12f45b39e73))


## v0.1.3 (2024-06-02)

### Bug Fixes

- Passes typing
  ([`43096f6`](https://github.com/tutorintelligence/vpx-rtp-py/commit/43096f6d242791dc363e4186432cd4fec1cd1ee1))


## v0.1.2 (2024-06-02)

### Bug Fixes

- Finally include compiled artifacts in wheel
  ([`89faf8f`](https://github.com/tutorintelligence/vpx-rtp-py/commit/89faf8f6c5287c06d496b202899474a9bcf035a0))


## v0.1.1 (2024-06-02)

### Bug Fixes

- Trigger new version :'(
  ([`7153e07`](https://github.com/tutorintelligence/vpx-rtp-py/commit/7153e07a8a447ad9c9421023639efed0259bdd6c))


## v0.1.0 (2024-06-02)

### Features

- Initial fork/cutdown from aiortc
  ([`2c2f22c`](https://github.com/tutorintelligence/vpx-rtp-py/commit/2c2f22c3c502736b8be92e75319e223f9d3437f4))
