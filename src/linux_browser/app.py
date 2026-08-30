"""Graphical browser application powered by Qt WebEngine."""

from __future__ import annotations

import os
import sys
from urllib.parse import quote


def _auto_select_platform() -> None:
    """Auto-detect and select the best Qt platform plugin.
    
    Uses offscreen rendering for headless environments, Wayland for Wayland
    sessions, and XCB for X11. Falls back to offscreen if a display is set
    but not accessible.
    
    MUST be called before importing any PySide6 modules.
    """
    if "QT_QPA_PLATFORM" in os.environ:
        return  # User has explicitly set the platform
    
    # Check for Wayland
    if os.environ.get("XDG_SESSION_TYPE") == "wayland" or os.environ.get("WAYLAND_DISPLAY"):
        os.environ["QT_QPA_PLATFORM"] = "wayland"
        return
    
    # Check for a valid X display
    display = os.environ.get("DISPLAY", "").strip()
    if not display:
        # No DISPLAY set; use offscreen for headless systems
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
        return
    
    # DISPLAY is set; try to verify it's actually accessible
    # In containers, DISPLAY might be set but the server doesn't exist
    try:
        import socket
        # Parse DISPLAY (format: [host]:display[.screen])
        if display.startswith(":"):
            host = "localhost"
            disp_part = display[1:].split(".")[0]
        elif ":" in display:
            host, disp_part = display.rsplit(":", 1)
            disp_part = disp_part.split(".")[0]
        else:
            host = "localhost"
            disp_part = display
        
        try:
            port = 6000 + int(disp_part)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            sock.connect((host, port))
            sock.close()
            # X server is accessible; use XCB (default)
        except (ConnectionRefusedError, socket.timeout, OSError, ValueError):
            # X server not accessible; fall back to offscreen
            os.environ["QT_QPA_PLATFORM"] = "offscreen"
    except Exception:
        # If anything goes wrong with the check, fall back to offscreen
        os.environ["QT_QPA_PLATFORM"] = "offscreen"


# Auto-select platform BEFORE importing PySide6
_auto_select_platform()

# Now safe to import Qt modules
from PySide6.QtCore import QUrl
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QApplication, QLineEdit, QMainWindow, QToolBar
from PySide6.QtWebEngineWidgets import QWebEngineView


class BrowserWindow(QMainWindow):
    """A minimal browser window with real Chromium page rendering."""

    def __init__(self, start_url: str = "https://duckduckgo.com") -> None:
        super().__init__()
        self.setWindowTitle("Linux Browser")
        self.resize(1280, 800)

        toolbar = QToolBar("Navigation")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        back_action = QAction("Back", self)
        back_action.setShortcut(QKeySequence("Alt+Left"))
        back_action.triggered.connect(lambda: self.web_view.back())
        toolbar.addAction(back_action)

        forward_action = QAction("Forward", self)
        forward_action.setShortcut(QKeySequence("Alt+Right"))
        forward_action.triggered.connect(lambda: self.web_view.forward())
        toolbar.addAction(forward_action)

        reload_action = QAction("Reload", self)
        reload_action.setShortcut(QKeySequence("Ctrl+R"))
        reload_action.triggered.connect(lambda: self.web_view.reload())
        toolbar.addAction(reload_action)

        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Enter a web address or search term")
        self.address_bar.setClearButtonEnabled(True)
        self.address_bar.returnPressed.connect(self.navigate)
        toolbar.addWidget(self.address_bar)

        self.web_view = QWebEngineView()
        self.web_view.urlChanged.connect(self.update_address)
        self.web_view.titleChanged.connect(self.update_title)
        self.setCentralWidget(self.web_view)
        self.navigate(start_url)

    def navigate(self, text: str | None = None) -> None:
        address = (text if text is not None else self.address_bar.text()).strip()
        if not address:
            return
        if " " in address or "." not in address and not address.startswith(("http://", "https://", "file:", "data:")):
            address = f"https://duckduckgo.com/?q={quote(address)}"
        elif not address.startswith(("http://", "https://", "file:", "data:")):
            address = f"https://{address}"
        self.web_view.setUrl(QUrl(address))

    def update_address(self, url: QUrl) -> None:
        self.address_bar.setText(url.toString())
        self.address_bar.setCursorPosition(0)

    def update_title(self, title: str) -> None:
        self.setWindowTitle(f"{title} - Linux Browser" if title else "Linux Browser")


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    app = QApplication([sys.argv[0], *args])
    app.setApplicationName("Linux Browser")
    window = BrowserWindow(args[0] if args else "https://duckduckgo.com")
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
