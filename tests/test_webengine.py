import sys
import unittest


try:
    from PySide6.QtCore import QEventLoop, QTimer
    from PySide6.QtWidgets import QApplication
    from PySide6.QtWebEngineWidgets import QWebEngineView
except ImportError:
    QWebEngineView = None


@unittest.skipUnless(QWebEngineView, "PySide6-WebEngine is not installed")
class WebEngineSmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.application = QApplication.instance() or QApplication(sys.argv)

    def test_renders_css_and_runs_javascript(self) -> None:
        view = QWebEngineView()
        loaded = []
        view.loadFinished.connect(loaded.append)
        view.setHtml(
            "<html><head><style>body { color: rgb(1, 2, 3); }</style></head>"
            "<body><main id='content'>initial</main>"
            "<script>document.title = 'Rendered';"
            "document.querySelector('#content').textContent = 'JavaScript ran';</script>"
            "</body></html>"
        )

        loop = QEventLoop()
        view.loadFinished.connect(loop.quit)
        QTimer.singleShot(5000, loop.quit)
        loop.exec()
        self.assertTrue(loaded and loaded[-1])

        result = []
        view.page().runJavaScript(
            "[document.title, document.querySelector('#content').textContent, "
            "getComputedStyle(document.body).color]",
            result.append,
        )
        QTimer.singleShot(1000, loop.quit)
        loop.exec()
        self.assertEqual(result, [["Rendered", "JavaScript ran", "rgb(1, 2, 3)"]])
        view.deleteLater()