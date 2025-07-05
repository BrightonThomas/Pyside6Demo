import sys
import geopandas as gpd
import pandas as pd

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QDoubleSpinBox, QPushButton, QListWidget
)

class EarthquakeFilterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Earthquake Magnitude Filter")
        self.setGeometry(100, 100, 600, 500)

        # Load data
        gdf = gpd.read_file("all_month.geojson")
        important_columns = ['mag', 'place', 'time', 'geometry', 'status', 'type', 'title']
        self.df = gdf[important_columns].copy()

        # GUI layout
        layout = QVBoxLayout()

        # Magnitude controls
        mag_layout = QHBoxLayout()
        mag_layout.addWidget(QLabel("Min Magnitude:"))
        self.min_mag = QDoubleSpinBox()
        self.min_mag.setRange(-1.0, 10.0)
        self.min_mag.setValue(0.0)
        mag_layout.addWidget(self.min_mag)

        mag_layout.addWidget(QLabel("Max Magnitude:"))
        self.max_mag = QDoubleSpinBox()
        self.max_mag.setRange(-1.0, 10.0)
        self.max_mag.setValue(10.0)
        mag_layout.addWidget(self.max_mag)

        layout.addLayout(mag_layout)

        # Filter button
        self.filter_button = QPushButton("Apply Filter")
        self.filter_button.clicked.connect(self.filter_data)
        layout.addWidget(self.filter_button)

        # Output list
        self.places_list = QListWidget()
        layout.addWidget(self.places_list)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Initial filter
        self.filter_data()

    def filter_data(self):
        min_val = self.min_mag.value()
        max_val = self.max_mag.value()

        df_filtered = self.df[self.df['mag'].between(min_val, max_val, inclusive='both')].copy()
        self.places_list.clear()

        if df_filtered.empty:
            self.places_list.addItem("No earthquakes found in range.")
        else:
            for place in df_filtered['place']:
                self.places_list.addItem(str(place))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EarthquakeFilterApp()
    window.show()
    sys.exit(app.exec())
