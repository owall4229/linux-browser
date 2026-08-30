"""Graphical browser application powered by Qt WebEngine."""

from __future__ import annotations

import sys
from urllib.parse import quote

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
