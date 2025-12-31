import numpy as np

FS = 100

def simulate_ppg(duration=60, stress_level=0.0, seed=42):
    np.random.seed(seed)
    t = np.linspace(0, duration, duration * FS, endpoint=False)
    hr = 75 + stress_level * 45
    ibi_mean = 60 / hr

    rr_var = max(0.005, 0.04 - stress_level * 0.035)
    n_beats = int(duration / ibi_mean + 15)
    rr_intervals = np.random.normal(ibi_mean, ibi_mean * rr_var, n_beats)
    rr_intervals = np.clip(rr_intervals, 0.4, 1.4)
    beat_times = np.cumsum(rr_intervals)
    beat_times = beat_times[beat_times < duration]

    phase = (t[:, None] - beat_times) / ibi_mean
    mask = (phase >= 0) & (phase < 1)

    systolic = np.exp(-((phase - 0.15) * 15) ** 2) * mask
    diastolic = 0.35 * np.exp(-((phase - 0.5) * 10) ** 2) * mask
    ppg_clean = np.sum(systolic + diastolic, axis=1)

    noise = 0.05 * np.random.randn(len(t))
    motion = stress_level * 0.8 * np.sin(2 * np.pi * np.array([0.3,1.2,2.5]) @ t) * np.random.randn(len(t))

    return t, ppg_clean + motion.sum(axis=0 if motion.ndim > 1 else 0) + noise
