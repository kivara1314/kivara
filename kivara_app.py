import streamlit as st
import matplotlib.pyplot as plt
from core.ppg_simulator import simulate_ppg
from core.processor import bandpass_filter, detect_peaks, calculate_hrv
from core.agent import KivaraAgent

FS = 100

st.set_page_config(
    page_title="KIVARA CORE",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 KIVARA CORE")
st.markdown("### دوقلوی دیجیتال هوشمند برای تشخیص استرس از PPG")

with st.sidebar:
    stress_level = st.slider("سطح استرس",0.0,1.0,0.4,0.05)
    duration = st.selectbox("مدت زمان (ثانیه)",[30,60,90,120],1)
    gender = st.radio("جنسیت",["مرد","زن"])
    cycle_day = st.slider("روز چرخه قاعدگی",1,28,15) if gender=="زن" else 1

if st.button("🚀 تحلیل PPG"):
    t, raw_signal = simulate_ppg(duration, stress_level)
    filtered = bandpass_filter(raw_signal)
    peaks = detect_peaks(filtered)
    hr, rmssd, lf_hf = calculate_hrv(peaks)
    expected_beats = duration*(75+stress_level*45)/60
    quality = min(1.0,max(len(peaks)/expected_beats,0.1))

    if hr is None:
        st.error("⚠️ پیک‌ها کافی نیستند.")
        st.stop()

    agent = KivaraAgent(gender[0],cycle_day)
    stress, mode, power = agent.get_decision(agent.estimate_stress(hr,rmssd,lf_hf,quality),quality)

    col1,col2,col3,col4 = st.columns(4)
    col1.metric("HR",f"{hr} bpm",delta=f"{hr-75:+.1f}")
    col2.metric("RMSSD",f"{rmssd} ms")
    col3.metric("سطح استرس",f"{stress:.2f}")
    col4.metric("کیفیت سیگنال",f"{quality:.2f}")

    st.markdown(f"### وضعیت فعلی: **{mode}** | مصرف انرژی: **{power}**")

    fig, axs = plt.subplots(3,1,figsize=(14,9))
    axs[0].plot(t,raw_signal,color="gray",alpha=0.7)
    axs[0].set_title("PPG خام"); axs[0].grid(True,alpha=0.3)

    axs[1].plot(t,filtered,color="#1f77b4")
    axs[1].plot(t[peaks],filtered[peaks],"ro",markersize=6)
    axs[1].set_title("PPG فیلترشده و پیک‌ها"); axs[1].grid(True,alpha=0.3)

    zoom_end=min(10*FS,len(t))
    axs[2].plot(t[:zoom_end],filtered[:zoom_end],color="green")
    axs[2].plot(t[peaks[peaks<zoom_end]],filtered[peaks[peaks<zoom_end]],"ro",markersize=8)
    axs[2].set_title("زوم روی ۱۰ ثانیه اول"); axs[2].grid(True,alpha=0.3)

    st.pyplot(fig)

st.caption("KIVARA CORE © 2025")
