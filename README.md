# Linux Browser

A small graphical browser for Linux, packaged as a normal Python application. It uses Qt WebEngine, which embeds Chromium, so pages are rendered with their real HTML, CSS, JavaScript, images, and network behavior rather than being converted to terminal text.

## Debian 12 / Ubuntu Installation

### Dependencies

Install graphics and browser libraries:

```bash
sudo apt update
sudo apt install -y \
  libgl1 libegl1 \
  libxkbcommon-x11-0 libxcb-cursor0 \
  libxcomposite1 libxdamage1 libxrandr2 \
  libnss3 libxshmfence1 libxtst6 \
  libasound2t64 xvfb xdg-utils
```

The PyPI wheels provide the Qt and Chromium components. A working display or Xvfb (virtual framebuffer) is required to render pages.

### Usage

**With a graphical display (desktop/GUI environment):**
```bash
linux-browser https://example.com
```

**Headless (no display server):**
```bash
QT_QPA_PLATFORM=offscreen xvfb-run -a linux-browser https://example.com
```

**Via SSH or in a container:**
```bash
export DISPLAY=:99
Xvfb :99 &
linux-browser https://example.com
```

## Install and run

```bash
python3 -m venv .venv
.venv/bin/python -m pip install linux-browser
.venv/bin/linux-browser
```

Open a specific page directly:

```bash
linux-browser https://example.com
```

The address bar accepts URLs and search terms. Back, forward, reload, and common keyboard shortcuts are available in the toolbar.

## Development

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e . pytest build
.venv/bin/python -m pytest
```

The WebEngine test loads an in-memory page and checks that CSS and JavaScript execute (powered by PySide6's built-in WebEngine). It is skipped when PySide6 is not installed, which keeps package metadata checks usable in minimal build environments.

## Build and publish

```bash
.venv/bin/python -m build
.venv/bin/python -m pip install twine
.venv/bin/twine check dist/*
.venv/bin/twine upload dist/*
```

Publishing requires a PyPI account and credentials configured for `twine`.