# Linux Browser

A small graphical browser for Linux, packaged as a normal Python application. It uses Qt WebEngine, which embeds Chromium, so pages are rendered with their real HTML, CSS, JavaScript, images, and network behavior rather than being converted to terminal text.

## Debian 12

Install a display server (a desktop session is fine) and the runtime libraries used by Qt:

```bash
sudo apt update
sudo apt install libegl1 libgl1 libnss3 libxkbcommon-x11-0 libxcb-cursor0 \
	libxcomposite1 libxdamage1 libxrandr2 libasound2 xdg-utils
```

The PyPI wheels provide the Qt and Chromium components. A working graphical session and graphics driver are still required to show the window. On a headless machine, run it inside a desktop container or an X server such as Xvfb.

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

The WebEngine test loads an in-memory page and checks that CSS and JavaScript execute. It is skipped when PySide6 is not installed, which keeps package metadata checks usable in minimal build environments.

## Build and publish

```bash
.venv/bin/python -m build
.venv/bin/python -m pip install twine
.venv/bin/twine check dist/*
.venv/bin/twine upload dist/*
```

Publishing requires a PyPI account and credentials configured for `twine`.