# vpx-rtp-py

[![PyPI version](https://badge.fury.io/py/vpx-rtp-py.svg)](https://badge.fury.io/py/vpx-rtp-py)

a creatively named python library for encoding/decoding video rtp streams using `cffi` bindings to `libvpx`, loosely forked / slimmed down from [aiortc](https://github.com/aiortc/aiortc).

narrowly constructed for the use cases of [Tutor Intelligence](http://tutorintelligence.com/), but feel free to post an issue or PR if relevant to you.

### install steps

be sure you have `libvpx` installed on your computer, otherwise `vpx-rtp-py` will not work (even if installed via `pip`).  to do so:

```
# ubuntu
sudo apt install libvpx-dev
```

```
# mac
brew install libvpx
```

then install via pypi:

```
pip install vpx-rtp-py
```

### limitations

 - does not really support RTCP or anything special/bidirectional (eg packet loss acknowledgement, retransmission packets)
 - does not support SSL
 - only supports `vp8` and `vp9` video encoding
 - pypi pre-built wheels only support linux + x86_64 + python 3.10.  if you want to add support for other platforms, feel free to update our `cd.yml` in a PR.