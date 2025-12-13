
import json
import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

# Load the baseline FFT
with open("Codette_Quantum_Harmonic_Baseline_FFT.json") as f:
    baseline = json.load(f)

baseline_freqs = np.array(baseline["frequency_hz"])
baseline_ffts = {k: np.array(v) for k, v in baseline["fft_magnitudes"].items()}

# Insert your new signal here (example placeholder)
# new_signal = your_velocity_data
# Example: new_signal = np.sin(2 * np.pi * 440 * np.linspace(0, 1, 2500))

# Simulated example signal
new_signal = np.sin(2 * np.pi * 440 * np.linspace(0, 1, 2500))
n = len(new_signal)
dt = 100 / 2500
new_freqs = fftfreq(n, dt)[:n // 2]
new_fft = np.abs(fft(new_signal)[:n // 2])

# Plot comparison
plt.figure(figsize=(12, 6))
plt.plot(baseline_freqs, baseline_ffts["AI_Node_1"], label="Baseline Node 1", color="blue")
plt.plot(new_freqs, new_fft, label="New Signal", color="orange", linestyle="--")
plt.title("FFT Comparison: Baseline vs New")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
