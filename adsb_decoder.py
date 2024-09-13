# adsb_decoder.py

import numpy as np
from scipy.signal import find_peaks
from rtlsdr_interface import RTLSDRInterface
import pyModeS as pms

class ADSBDecoder:
    def __init__(self, sdr_interface, sample_rate=2.4e6, center_freq=1090e6):
        """Initialize the ADS-B Decoder with an instance of RTLSDRInterface.

        Args:
            sdr_interface (RTLSDRInterface): The SDR interface to receive samples.
            sample_rate (float): The sample rate of the SDR.
            center_freq (float): The center frequency of the SDR.
        """
        self.sdr_interface = sdr_interface
        self.sample_rate = sample_rate
        self.center_freq = center_freq

        # Set the SDR parameters
        self.sdr_interface.set_center_frequency(self.center_freq)
        self.sdr_interface.set_sample_rate(self.sample_rate)

    def detect_preamble(self, samples, threshold=0.4):
        """Detect preambles in the samples to find the start of ADS-B messages.

        Args:
            samples (numpy.ndarray): The complex samples from the SDR.
            threshold (float): The threshold for detecting peaks.

        Returns:
            list: Indices where preambles were detected.
        """
        magnitude = np.abs(samples)
        peaks, _ = find_peaks(magnitude, height=threshold, distance=int(0.000008 * self.sample_rate))
        return peaks

    def demodulate_adsb(self, samples):
        """Demodulate ADS-B signals from complex samples.

        Args:
            samples (numpy.ndarray): The complex samples from the SDR.

        Returns:
            list: Demodulated binary ADS-B messages.
        """
        preamble_indices = self.detect_preamble(samples)
        adsb_messages = []

        for index in preamble_indices:
            # Extract 112-bit ADS-B message after preamble
            message_samples = samples[index:index + int(0.000112 * self.sample_rate)]
            if len(message_samples) < int(0.000112 * self.sample_rate):
                continue

            # Decode the binary message from the extracted samples
            message_bits = self.decode_bits(message_samples)
            adsb_messages.append(message_bits)

        return adsb_messages

    def decode_bits(self, samples):
        """Decode ADS-B message bits from demodulated samples.

        Args:
            samples (numpy.ndarray): Demodulated samples for one message.

        Returns:
            str: The binary representation of the ADS-B message.
        """
        bit_duration = int(0.000001 * self.sample_rate)  # Duration of one bit
        bits = ""

        for i in range(0, len(samples), bit_duration):
            bit_samples = samples[i:i + bit_duration]
            if np.mean(np.abs(bit_samples)) > 0.2:  # Adjust threshold based on signal strength
                bits += "1"
            else:
                bits += "0"

        return bits

    def decode_adsb_messages(self, messages):
        """Decode ADS-B messages using pyModeS.

        Args:
            messages (list): List of binary ADS-B messages.

        Returns:
            list: Decoded ADS-B data.
        """
        decoded_data = []

        for msg in messages:
            if len(msg) == 112:
                # Use pyModeS to decode ADS-B message
                icao = pms.adsb.icao(msg)
                typecode = pms.adsb.typecode(msg)

                # Decoding different types of ADS-B messages
                if typecode >= 1 and typecode <= 4:
                    # Callsign
                    callsign = pms.adsb.callsign(msg)
                    decoded_data.append({"ICAO": icao, "Type": "Callsign", "Callsign": callsign})
                elif typecode >= 9 and typecode <= 18:
                    # Position
                    position = pms.adsb.position_with_ref(msg, icao)
                    decoded_data.append({"ICAO": icao, "Type": "Position", "Position": position})
                elif typecode >= 19 and typecode <= 22:
                    # Velocity
                    velocity = pms.adsb.velocity(msg)
                    decoded_data.append({"ICAO": icao, "Type": "Velocity", "Velocity": velocity})

        return decoded_data

    def run_decoder(self, num_samples=256 * 1024):
        """Run the ADS-B decoder to receive and decode messages in real-time.

        Args:
            num_samples (int): Number of samples to read in each batch.
        """
        try:
            while True:
                # Read samples from the SDR
                samples = self.sdr_interface.read_samples(num_samples)

                # Demodulate ADS-B messages from the samples
                adsb_messages = self.demodulate_adsb(samples)

                # Decode ADS-B messages
                decoded_data = self.decode_adsb_messages(adsb_messages)

                # Display the decoded data
                for data in decoded_data:
                    print(data)

        except KeyboardInterrupt:
            print("Stopping decoder...")
        finally:
            self.sdr_interface.close()

# Example usage
if __name__ == "__main__":
    # Initialize the SDR interface
    sdr = RTLSDRInterface()

    # Create an instance of the ADSBDecoder
    decoder = ADSBDecoder(sdr)

    # Run the decoder
    decoder.run_decoder()