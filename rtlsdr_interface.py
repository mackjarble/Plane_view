# rtlsdr_interface.py

from rtlsdr import RtlSdr

class RTLSDRInterface:
    def __init__(self, center_freq=1090e6, sample_rate=2.4e6, bandwidth=None):
        """Initialize the RTL-SDR dongle with the default or specified parameters.

        Args:
            center_freq (float): The center frequency in Hz (default is 1090 MHz for ADS-B).
            sample_rate (float): The sampling rate in Hz.
            bandwidth (float): The bandwidth in Hz. If None, the bandwidth is set to the sample rate.
        """
        self.center_freq = center_freq
        self.sample_rate = sample_rate
        self.bandwidth = bandwidth or sample_rate

        # Initialize the SDR device
        self.sdr = RtlSdr()

        # Set up the SDR parameters
        self.sdr.sample_rate = self.sample_rate
        self.sdr.center_freq = self.center_freq
        self.sdr.gain = 'auto'  # Use automatic gain control

    def set_center_frequency(self, frequency):
        """Set the center frequency of the SDR."""
        self.sdr.center_freq = frequency
        self.center_freq = frequency

    def set_sample_rate(self, rate):
        """Set the sample rate of the SDR."""
        self.sdr.sample_rate = rate
        self.sample_rate = rate

    def set_bandwidth(self, bandwidth):
        """Set the bandwidth of the SDR."""
        # Note: RTL-SDR does not have a direct way to set bandwidth independently;
        # it is usually inferred from the sample rate.
        self.bandwidth = bandwidth

    def read_samples(self, num_samples):
        """Read a block of samples from the SDR.

        Args:
            num_samples (int): The number of samples to read.

        Returns:
            numpy.ndarray: The block of complex samples read from the SDR.
        """
        return self.sdr.read_samples(num_samples)

    def close(self):
        """Close the SDR connection."""
        self.sdr.close()

# Example usage:
if __name__ == "__main__":
    # Create an instance of the RTLSDRInterface
    sdr_interface = RTLSDRInterface()
    print(f"Center Frequency: {sdr_interface.center_freq} Hz")
    print(f"Sample Rate: {sdr_interface.sample_rate} Hz")
    
    # Read samples (for demonstration purposes, use a small number of samples)
    samples = sdr_interface.read_samples(1024)
    print(f"Read {len(samples)} samples from RTL-SDR.")

    # Clean up
    sdr_interface.close()
