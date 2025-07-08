import sys
import os
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.io as pio

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QDoubleSpinBox, QPushButton, QListWidget, QComboBox,
    QMenuBar, QMenu
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from pathlib import Path

def generate_plot(df, html_path="filtered_map.html"):
    if df.empty or "latitude" not in df or "longitude" not in df:
        fig = px.scatter_mapbox(lat=[], lon=[], zoom=1)
    else:
        fig = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            hover_name="place",
            size="mag",
            color="mag",
            zoom=1,
            color_continuous_scale="Turbo",
            height=600
        )

    fig.update_layout(
        mapbox_style="open-street-map",
        margin=dict(l=0, r=0, t=50, b=0)
    )

    pio.write_html(fig, file=html_path, full_html=True, include_plotlyjs='directory')

class EarthquakeFilterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Earthquake Magnitude Filter + Map")
        self.setGeometry(100, 100, 1000, 800)

        # Create menu bar
        self.create_menu_bar()

        # Load GeoJSON data
        gdf = gpd.read_file("all_month.geojson")
        important_columns = ['mag', 'place', 'time', 'geometry', 'status', 'type', 'title']
        self.df = gdf[important_columns].copy()

        # Get unique status values
        self.status_values = ['All'] + sorted(self.df['status'].dropna().unique().tolist())

        # GUI Layout
        layout = QVBoxLayout()

        # Magnitude Filter
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

        # Status Filter
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Status:"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(self.status_values)
        status_layout.addWidget(self.status_combo)
        layout.addLayout(status_layout)

        # Filter Button
        self.filter_button = QPushButton("Apply Filters")
        self.filter_button.clicked.connect(self.filter_data)
        layout.addWidget(self.filter_button)

        # Earthquake List
        self.places_list = QListWidget()
        layout.addWidget(self.places_list)

        # Plotly Map View
        self.map_view = QWebEngineView()
        layout.addWidget(self.map_view)

        # Set Layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.setStyleSheet("""
            QMainWindow {
                background-image: url(background.);
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
                background-size: cover;
            }
        """)

        # Initial Data Display
        self.filter_data()
        #self.set_background()

    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu = menubar.addMenu("Options")
        file_menu = menubar.addMenu("Settings")
        file_menu = menubar.addMenu("Info")
        file_menu = menubar.addMenu("About")
        
        # Quit action
        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.close)

    def filter_data(self):
        min_val = self.min_mag.value()
        max_val = self.max_mag.value()
        selected_status = self.status_combo.currentText()

        # Apply magnitude filter
        df_filtered = self.df[
            self.df['mag'].notna() & self.df['mag'].between(min_val, max_val)
        ].copy()

        # Apply status filter if not 'All'
        if selected_status != 'All':
            df_filtered = df_filtered[df_filtered['status'] == selected_status]

        # Extract lat/lon from geometry
        df_filtered["longitude"] = df_filtered["geometry"].apply(lambda p: p.x)
        df_filtered["latitude"] = df_filtered["geometry"].apply(lambda p: p.y)

        # Update List
        self.places_list.clear()
        if df_filtered.empty:
            self.places_list.addItem("No earthquakes found with current filters.")
        else:
            for place in df_filtered['place']:
                self.places_list.addItem(str(place))

        # Generate and load map
        generate_plot(df_filtered)
        html_file = Path("filtered_map.html").resolve().as_uri()
        self.map_view.setUrl(html_file)

    # def set_background(self):
    #         self.setStyleSheet("""
    #         QMainWindow {
    #         background-image: url(background.png);
    #         background-repeat: no-repeat;
    #         background-position: center;
    #         background-attachment: fixed;
    #         background-size: cover;
    #     }
    #     QWidget {
    #         background-color: rgba(255, 255, 255, 0.7);
    #     }
    #     QListWidget, QWebEngineView, QComboBox, QDoubleSpinBox {
    #         background-color: rgba(255, 255, 255, 0.85);
    #     }
    #     QPushButton {
    #         background-color: #4a90e2;
    #         color: white;
    #         border: 1px solid #2a70c2;
    #         padding: 5px;
    #         border-radius: 3px;
    #     }
    #     QPushButton:hover {
    #         background-color: #5aa0f2;
    #     }
    # """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EarthquakeFilterApp()
    window.show()
    sys.exit(app.exec())