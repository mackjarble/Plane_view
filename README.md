# Real-Time ADS-B Receiver and Visualizer

This Python-based application uses an RTL-SDR dongle to receive and demodulate ADS-B signals from aircraft, allowing real-time visualization of planes flying in your vicinity. The application provides a GUI interface that displays:

- **Frequency Spectrum Plot**: A real-time plot of the frequency spectrum of the received signals.
- **Map Visualization**: A live map that shows the positions of aircraft and detailed information about them (ICAO address, callsign, position, velocity).
- **Aircraft Information**: Decoded ADS-B data such as aircraft positions, speed, altitude, and callsign.

## Features

- **RTL-SDR Interface**: Uses an RTL-SDR dongle to capture ADS-B signals at 1090 MHz.
- **ADS-B Demodulation & Decoding**: Demodulates and decodes ADS-B messages to extract information such as aircraft position, velocity, and ICAO code.
- **Real-Time GUI**: Displays a real-time frequency spectrum and aircraft positions on a live map.
- **Aircraft Information Display**: Shows the decoded information of each aircraft.

## Prerequisites

- **RTL-SDR Dongle**: A USB RTL-SDR dongle.
- **Python 3.x**
- **RTL-SDR Drivers**: Ensure the RTL-SDR drivers are installed and your dongle is working with software like `rtl_test`.

## Installation

1. Clone the repository or download the source code:

```bash
   git clone https://github.com/mackjarble/adsb-visualizer.git
   cd adsb-visualizer
```
2. Install the required dependencies:

```bash
    pip install -r requrements.txt
```
    If requirements.txt doesn't exist, manually install the following packages:

```bash 
    pip install numpy scipy pyModeS PyQt5 pyqtgraph folium geopy PyQtWebEngine pyrtlsdr pyrtlsdrlib
```

3. Ensure your RTL is set up correctly with appropriate drivers. 

## Usage

1. Run the main application:

```bash
python main.py
```
2. Once launched, the GUI will display:

    - A real-time frequency spectrum plot showing signal strength in dB across the frequency range.
    - A map visualizing the positions of aircraft based on ADS-B data.

3. Aircraft positions are updated every second, and the map displays markers for each detected aircraft. Clicking on a marker reveals additional information, such as the aircraft's ICAO address and callsign.

## Application Structure

- main.py: The main application file that ties the GUI, SDR interface, and ADS-B decoding together.
- rtlsdr_interface.py: Provides a class for interfacing with the RTL-SDR dongle, setting parameters like frequency and sample rate.
- adsb_decoder.py: Contains logic for detecting and decoding ADS-B messages from the raw IQ samples.
- requirements.txt: Contains all Python dependencies needed to run the application.

## GUI components

- Frequency Spectrum Plot

- Map Visualization

## Troubleshooting
# Map Not Rendering

If the map is not rendering in the application, make sure you have the following installed:

```bash
pip install PyQtWebEngine
```

You can also try rendering the map using a local HTML file instead of directly embedding the HTML content. See the update_map method in main.py for details.

# RTL-SDR Not Detected

If the RTL-SDR dongle is not being detected, ensure:

1. The dongle is plugged in.
2. The correct drivers are installed (rtl-sdr on Linux, or Zadig on Windows).
3. Run rtl_test to check if the dongle is working.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Thanks to the RTL-SDR community for providing tools and documentation.
Special thanks to the developers of pyModeS for ADS-B decoding.
