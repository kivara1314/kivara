from scipy.signal import butter, filtfilt, find_peaks, welch
import numpy as np

FS = 100

def bandpass_filter(signal):
    nyq = FS / 2
    b, a = butter(4, [0.5 / nyq, 8 / nyq], btype="band")
    return filtfilt(b, a, signal)

def detect_peaks(signal):
    z = (signal - np.mean(signal)) / (np.std(signal) + 1e-8)
    peaks, _ = find_peaks(z, prominence=0.6, distance=int(FS*0.4), height=0.3)
    return peaks

def calculate_hrv(peaks):
    if len(peaks) < 6:
        return None, None, None

    ibi = np.diff(peaks) / FS
    hr = 60 / np.mean(ibi)
    rmssd = np.sqrt(np.mean(np.diff(ibi)**2)) * 1000

    if len(ibi) < 10:
        lf_hf = 1.0 + np.std(ibi) * 15
    else:
        f, pxx = welch(ibi, fs=4, nperseg=min(len(ibi),64))
        lf = np.trapz(pxx[(f>=0.04)&(f<0.15)])
        hf = np.trapz(pxx[(f>=0.15)&(f<=0.4)])
        lf_hf = lf/(hf+1e-8) if hf>0 else 6.0

    return round(hr,1), round(rmssd,1), round(lf_hf,2)
