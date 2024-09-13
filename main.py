# main.py

import sys
import numpy as np
import requests
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView
from adsb_decoder import ADSBDecoder
from rtlsdr_interface import RTLSDRInterface
import tempfile

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Setup the main window layout
        self.setWindowTitle("Real-Time ADS-B Receiver and Visualizer")
        self.setGeometry(100, 100, 1200, 800)

        # Create central widget
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # Frequency Spectrum Plot Widget
        self.spectrum_plot_widget = PlotWidget()
        self.spectrum_plot_widget.setYRange(0, 100)
        self.spectrum_plot_widget.setTitle("Frequency Spectrum")
        self.spectrum_plot_widget.setLabel('bottom', 'Frequency', 'Hz')
        self.spectrum_plot_widget.setLabel('left', 'Magnitude', 'dB')

        # Map Widget for Aircraft Positions
        self.map_view = QWebEngineView()
        self.map_widget = folium.Map(location=[0, 0], zoom_start=2)
        self.update_map()

        # Add widgets to layout
        self.splitter.addWidget(self.spectrum_plot_widget)
        self.splitter.addWidget(self.map_view)
        self.layout.addWidget(self.splitter)

        # Timer for updating data
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)  # Update every second
        self.timer.timeout.connect(self.update_data)

        # Initialize SDR and ADS-B Decoder
        self.sdr_interface = RTLSDRInterface()
        self.adsb_decoder = ADSBDecoder(self.sdr_interface)

        # Start the timer
        self.timer.start()

    def update_data(self):
        """Update the spectrum plot and the aircraft positions on the map."""
        # Read samples from SDR
        samples = self.sdr_interface.read_samples(256 * 1024)
        
        # Update frequency spectrum plot
        self.update_spectrum_plot(samples)

        # Decode ADS-B messages
        adsb_messages = self.adsb_decoder.demodulate_adsb(samples)
        decoded_data = self.adsb_decoder.decode_adsb_messages(adsb_messages)

        # Update map with aircraft positions
        self.update_map(decoded_data)

    def update_spectrum_plot(self, samples):
        """Update the frequency spectrum plot with new samples."""
        # Compute the FFT of the samples
        fft_result = np.fft.fftshift(np.fft.fft(samples))
        freq_axis = np.fft.fftshift(np.fft.fftfreq(len(samples), 1 / self.adsb_decoder.sample_rate))

        # Convert FFT result to dB scale
        magnitude = 20 * np.log10(np.abs(fft_result))

        # Plot the spectrum
        self.spectrum_plot_widget.clear()
        self.spectrum_plot_widget.plot(freq_axis, magnitude, pen='c')

    def update_map(self, aircraft_data=None):
        """Update the map with the positions of the aircraft.

        Args:
            aircraft_data (list): A list of decoded ADS-B data.
        """
        # Get the user's current location (lat, lon)
        lat, lon = get_current_location()

        # Reset map
        self.map_widget = folium.Map(location=[lat, lon], zoom_start=8)

        if aircraft_data:
            for data in aircraft_data:
                if data['Type'] == "Position" and data['Position']:
                    lat, lon = data['Position']
                    if lat is not None and lon is not None:
                        # Create a marker for each aircraft
                        marker = folium.Marker(
                            location=[lat, lon],
                            popup=f"ICAO: {data['ICAO']}, Callsign: {data.get('Callsign', 'Unknown')}"
                        )
                        marker.add_to(self.map_widget)

        # Save map to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        map_path = temp_file.name
        self.map_widget.save(map_path)
    
        # Load the temporary HTML file into QWebEngineView
        self.map_view.setHtml("<html><body><h1>Test Page</h1></body></html>")
        self.map_view.load(QtCore.QUrl.fromLocalFile(map_path))

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

def get_current_location():
    """Fetch current location based on IP address using the ipinfo.io API."""
    try:
        response = requests.get('https://ipinfo.io/')
        data = response.json()
        location = data['loc'].split(',')
        latitude = float(location[0])
        longitude = float(location[1])
        return latitude, longitude
    except Exception as e:
        print(f"Error fetching location: {e}")
        return 0.0, 0.0  # Fallback to default locationdef get

if __name__ == "__main__":
    main()
