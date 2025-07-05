from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication,QMainWindow,QPushButton,QSlider,QWidget
# Only needed for access to command line arguments
import sys

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Earthquake Analysis Tool")
        self.resize(1000, 1000)

        self.button=QPushButton("Analyze")
        self.button.setToolTip("Click to analyze earthquake data")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.button1_clicked)
        self.setCentralWidget(self.button)
        self.button.show()

        #slider
        self.slider=QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.setCentralWidget(self.slider)
        self.slider.valueChanged.connect(self.slider_changed)
        self.slider.show()

    def button1_clicked(self):
        print("Button clicked!")

    def slider_changed(self, value):
        print(f"Slider value changed: {value}")


app=QApplication(sys.argv)

window=MainWindow()
window.show()

app.exec()  # This starts the event loop and waits for events to be processed.

