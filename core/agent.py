import numpy as np

class KivaraAgent:
    def __init__(self, gender="M", cycle_day=1):
        self.gender = gender.upper()
        self.cycle_day = cycle_day
        self.baseline_hr = 75.0
        self.baseline_rmssd = 45.0
        self.stress_history = []
        self.anomaly = 0.0

    def update_cycle_factor(self):
        if self.gender != "F": return 1.0
        d = self.cycle_day
        if d <= 5: return 0.7
        if 6 <= d <= 13: return 1.0
        if 14 <= d <= 16: return 1.35
        return 0.9

    def estimate_stress(self, hr, rmssd, lf_hf, quality):
        cycle_factor = self.update_cycle_factor()
        hr_dev = max(0, (hr - self.baseline_hr)/25)
        hrv_dev = max(0, (self.baseline_rmssd - rmssd)/35)
        freq_dev = min(1.0, (lf_hf - 1)/4)

        stress = 0.5*hr_dev + 0.35*hrv_dev + 0.15*freq_dev
        stress = np.clip(stress*quality,0.0,1.0)
        if self.gender=="F":
            stress *= (2.0 - cycle_factor)

        self.baseline_hr = 0.92*self.baseline_hr + 0.08*hr
        self.baseline_rmssd = 0.92*self.baseline_rmssd + 0.08*rmssd

        return stress

    def get_decision(self, stress, quality):
        self.stress_history.append(stress)
        if len(self.stress_history)>15:
            self.stress_history.pop(0)

        mean_stress = np.mean(self.stress_history)
        if len(self.stress_history)>5 and stress>mean_stress+0.3:
            self.anomaly = min(1.0,self.anomaly+0.3)
        else:
            self.anomaly *=0.9

        if self.anomaly>0.7:
            mode="🚨 هشدار"; power="FULL_POWER"
        elif mean_stress>0.75:
            mode="🔴 استرس بالا"; power="FULL_POWER"
        elif mean_stress>0.5:
            mode="🟡 استرس متوسط"; power="NORMAL"
        elif mean_stress<0.25:
            mode="🟢 آرام"; power="POWER_SAVE"
        else:
            mode="🔵 عادی"; power="NORMAL"

        return mean_stress, mode, power
