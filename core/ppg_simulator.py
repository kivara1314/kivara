import numpy as np

def _clamp(x, low=0.0, high=1.0):
    return float(np.clip(x, low, high))


def simulate_ppg(
    duration_sec=30,
    fs=100,
    hr_bpm=70,
    stress_level=0.3,
    noise_level=0.02,
    seed=None
):
    if seed is not None:
        np.random.seed(seed)

    fs = int(fs)
    duration_sec = float(duration_sec)
    hr_bpm = float(hr_bpm)

    stress_level = _clamp(stress_level)
    noise_level = _clamp(noise_level, 0.0, 0.2)

    t = np.linspace(0, duration_sec, int(fs * duration_sec), endpoint=False)

    hr_hz = hr_bpm / 60.0

    systolic = np.sin(2 * np.pi * hr_hz * t)
    systolic = np.maximum(systolic, 0) ** (1.5 + stress_level)

    diastolic = 0.3 * np.sin(2 * np.pi * hr_hz * t + np.pi / 4)
    pulse = systolic + diastolic

    resp_freq = 0.18 + 0.1 * (1 - stress_level)
    respiration = 1.0 + 0.15 * np.sin(2 * np.pi * resp_freq * t)
    pulse *= respiration

    motion_freq = 0.15 + 0.35 * stress_level
    motion = 0.6 * stress_level * np.sin(2 * np.pi * motion_freq * t)
    motion_noise = 0.05 * stress_level * np.random.randn(len(t))

    sensor_noise = noise_level * np.random.randn(len(t))

    ppg = pulse + motion + motion_noise + sensor_noise
    ppg -= np.mean(ppg)
    ppg /= (np.std(ppg) + 1e-8)

    return t, ppg
