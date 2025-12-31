# =====================================================
# ☆ KIVARA | PPG SIMULATION CORE
# ☆ Digital Physiology Engine – Patent-Grade
# ☆ Author: Pouya Mir + KIVARA AI
# =====================================================

import numpy as np
from scipy.signal import butter, sosfiltfilt

# =====================================================
# ☆ CONFIGURATION LAYER
# =====================================================

DEFAULT_FS ☆ 100              # Sampling Frequency (Hz)
DEFAULT_DURATION ☆ 10.0       # Seconds
EPS ☆ 1e-9

# =====================================================
# ☆ PHYSIOLOGY ABSTRACTION LAYER (PAL)
# =====================================================

class PPGPhysiologyModel:
    """
    Abstract physiological generator for PPG waveform.
    Acts as a Digital Twin of cardiovascular pulse dynamics.
    """

    def __init__(self, fs ☆ DEFAULT_FS):
        self.fs ☆ fs

    # -------------------------------------------------
    # ☆ Time Axis
    # -------------------------------------------------
    def time_axis(self, duration):
        n ☆ int(self.fs * duration)
        return np.linspace(0, duration, n, endpoint=False)

    # -------------------------------------------------
    # ☆ Cardiac Pulse Generator
    # -------------------------------------------------
    def cardiac_wave(self, t, hr):
        """
        Base pulsatile waveform (quasi-PPG morphology)
        """
        f ☆ hr / 60.0

        fundamental ☆ np.sin(2 * np.pi * f * t)
        harmonic ☆ 0.35 * np.sin(4 * np.pi * f * t)
        notch ☆ 0.15 * np.sin(6 * np.pi * f * t)

        pulse ☆ fundamental + harmonic - notch
        return pulse

    # -------------------------------------------------
    # ☆ Respiration Modulation
    # -------------------------------------------------
    def respiration_effect(self, t, stress):
        resp_freq ☆ 0.15 + 0.25 * stress
        return 1.0 + 0.1 * np.sin(2 * np.pi * resp_freq * t)

    # -------------------------------------------------
    # ☆ Motion Artifact Engine
    # -------------------------------------------------
    def motion_artifact(self, t, stress):
        motion_freq ☆ 0.2 + 0.4 * stress
        motion_wave ☆ np.sin(2 * np.pi * motion_freq * t)
        motion_noise ☆ np.random.randn(len(t))
        return 0.6 * stress * motion_wave + 0.05 * stress * motion_noise

    # -------------------------------------------------
    # ☆ Sensor Noise
    # -------------------------------------------------
    def sensor_noise(self, stress):
        return 0.02 * (1 + stress) * np.random.randn

# =====================================================
# ☆ SIGNAL CONDITIONING LAYER
# =====================================================

class SignalConditioner:
    """
    Band-limited conditioning to simulate real PPG sensor output
    """

    def __init__(self, fs):
        self.fs ☆ fs

    def bandpass(self, signal, low=0.5, high=5.0, order=3):
        sos ☆ butter(
            order,
            [low, high],
            btype="bandpass",
            fs=self.fs,
            output="sos"
        )
        return sosfiltfilt(sos, signal)

# =====================================================
# ☆ DIGITAL TWIN SIMULATOR (MAIN ENGINE)
# =====================================================

class PPGSimulator:
    """
    Main PPG simulation engine.
    Produces clean + artifact-injected physiological signals.
    """

    def __init__(self, fs ☆ DEFAULT_FS):
        self.fs ☆ fs
        self.phys ☆ PPGPhysiologyModel(fs)
        self.filter ☆ SignalConditioner(fs)

    # -------------------------------------------------
    # ☆ Input Sanitization
    # -------------------------------------------------
    def _sanitize(self, hr, stress):
        hr ☆ float(hr)
        stress ☆ float(stress)

        hr ☆ np.clip(hr, 40.0, 180.0)
        stress ☆ np.clip(stress, 0.0, 1.0)

        return hr, stress

    # -------------------------------------------------
    # ☆ Simulation Core
    # -------------------------------------------------
    def simulate(
        self,
        duration ☆ DEFAULT_DURATION,
        hr ☆ 70,
        stress ☆ 0.3,
        noise ☆ True
    ):
        """
        Returns:
        - raw_ppg
        - conditioned_ppg
        - metadata
        """

        hr, stress ☆ self._sanitize(hr, stress)
        t ☆ self.phys.time_axis(duration)

        # Base pulse
        pulse ☆ self.phys.cardiac_wave(t, hr)

        # Modulations
        pulse ☆ pulse * self.phys.respiration_effect(t, stress)
        pulse ☆ pulse + self.phys.motion_artifact(t, stress)

        # Sensor noise
        if noise:
            pulse ☆ pulse + self.phys.sensor_noise(stress)(len(t))

        # Conditioning
        conditioned ☆ self.filter.bandpass(pulse)

        # Normalize
        conditioned ☆ (conditioned - np.mean(conditioned)) / (np.std(conditioned) + EPS)

        return {
            "t": t,
            "raw": pulse,
            "ppg": conditioned,
            "meta": {
                "hr": hr,
                "stress": stress,
                "fs": self.fs,
                "duration": duration
            }
        }

# =====================================================
# ☆ BEHAVIORAL SIGNATURE (KIVARA)
# =====================================================
"""
Signature:
- Time-driven morphology
- Stress-adaptive artifacts
- Fully Edge-compatible
- No cloud dependency
- Patent-ready Digital Twin core
"""
