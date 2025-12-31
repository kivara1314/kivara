# =====================================================
# KIVARA CORE — Signal Processor
# Stable / Streamlit-safe / Edge-ready
# =====================================================

import numpy as np
from scipy.signal import butter, sosfiltfilt, find_peaks


# =====================================================
# Utility
# =====================================================

def _safe_array(x):
    if x is None:
        return np.array([])
    return np.asarray(x, dtype=float)


# =====================================================
# Bandpass Filter (STABLE - SOS)
# =====================================================

def bandpass_filter(signal, fs=100):
    """
    Stable bandpass filter using SOS representation.
    Prevents filtfilt instability on Streamlit Cloud.
    """
    signal = _safe_array(signal)

    # --- Guard for short signals ---
    if len(signal) < fs:
        return signal

    nyq = fs / 2.0
    low = 0.5 / nyq
    high = 8.0 / nyq

    sos = butter(
        N=4,
        Wn=[low, high],
        btype="band",
        output="sos"
    )

    return sosfiltfilt(sos, signal)


# =====================================================
# Peak Detection (PPG)
# =====================================================

def detect_peaks(ppg_signal, fs=100):
    """
    Detect systolic peaks in PPG signal.
    """
    ppg_signal = _safe_array(ppg_signal)

    if len(ppg_signal) < fs:
