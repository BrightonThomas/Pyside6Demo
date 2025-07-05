import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView

class GeoJSONBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("geojson.io Viewer")
        self.setGeometry(100, 100, 1200, 800)

        self.web_view = QWebEngineView()
        self.web_view.load("https://geojson.io")

        layout = QVBoxLayout()
        layout.addWidget(self.web_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeoJSONBrowser()
    window.show()
    sys.exit(app.exec())
