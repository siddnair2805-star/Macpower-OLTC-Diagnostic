import streamlit as st
import pandas as pd
import numpy as np
import time

# Page Configuration
st.set_page_config(page_title="Macpower Smart-OLTC Platform", layout="wide")

# Professional Light Theme CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
        .main-header {
            background: #ffffff;
            padding: 40px;
            border-radius: 15px;
            border-bottom: 5px solid #0d9488;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .metric-card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .stButton>button {
            background-color: #0d9488;
            color: white;
            border-radius: 8px;
            width: 100%;
            height: 3em;
            font-weight: 700;
        }
    </style>
""", unsafe_allow_html=True)

# Executive Header
st.markdown(f"""
    <div class="main-header">
        <h1 style='color: #0f172a; margin:0; font-size: 36px;'>⚡ MACPOWER SWITCHGEAR PVT LTD</h1>
        <p style='color: #0d9488; margin:10px 0 0 0; font-weight:700; font-size:18px;'>IoT-Enabled Intelligent Digital Twin & Predictive Diagnostic Platform</p>
        <hr style="width: 50px; border: 2px solid #0d9488; margin: 20px auto;">
        <p style='color: #64748b; font-size:14px;'>Developed by: <b>Siddhant Nair</b> | 3rd Year ECE, PSG College of Technology</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar Simulation Controls
st.sidebar.header("🕹️ Field Simulation Controls")
ops_count = st.sidebar.slider("Total Operations Logged", 0, 15000, 9950)
t_trans = st.sidebar.slider("Mechanical Transition Time (s)", 1.0, 6.0, 2.1)
peak_i = st.sidebar.slider("Motor Peak Current (A)", 0.5, 5.0, 1.4)
delta_t = st.sidebar.slider("Tank Temp Differential (°C)", 0.0, 40.0, 4.5)

# --- THE CRUX: Engineering Models ---

# 1. Arrhenius Model for Oil BDV Prediction
# BDV decreases based on temperature stress and operations
initial_bdv = 60.0
degradation = (delta_t * 0.5) + (ops_count * 0.001)
predicted_bdv = max(15.0, initial_bdv - degradation)

# 2. Reliability State
if t_trans > 4.0:
    health_status = "CRITICAL: SLUGGISH DRIVE"
    status_color = "#ef4444"
elif predicted_bdv < 30.0:
    health_status = "WARNING: OIL DEGRADED"
    status_color = "#f97316"
elif ops_count >= 10000:
    health_status = "MAINTENANCE DUE"
    status_color = "#eab308"
else:
    health_status = "SYSTEM HEALTHY"
    status_color = "#10b981"

# --- UI Metrics ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-card"><p style="color:#64748b; font-size:12px; font-weight:700;">PREDICTED OIL BDV</p><h2 style="color:#0f172a;">{predicted_bdv:.1f} kV</h2></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card"><p style="color:#64748b; font-size:12px; font-weight:700;">TRANSITION TIME</p><h2 style="color:#0f172a;">{t_trans} s</h2></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-card"><p style="color:#64748b; font-size:12px; font-weight:700;">OP. COUNTER</p><h2 style="color:#0f172a;">{ops_count:,}</h2></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-card" style="border-top: 5px solid {status_color};"><p style="color:#64748b; font-size:12px; font-weight:700;">HEALTH STATUS</p><h2 style="color:{status_color}; font-size:20px;">{health_status}</h2></div>', unsafe_allow_html=True)

st.write("")

# --- DIGITAL TWIN & CHARTS ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🖥️ Physical Digital Twin")
    canvas_html = f"""
    <div style="background:#f1f5f9; padding:20px; border-radius:12px; border:1px solid #e2e8f0; text-align:center;">
        <canvas id="twinCanvas" width="400" height="250" style="background:white; border-radius:8px; border:1px solid #cbd5e1;"></canvas>
        <br><button id="tapBtn" style="margin-top:20px; width:100%; padding:12px; background:#0d9488; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:700;">TRIGGER TAP CHANGE SEQUENCE</button>
    </div>
    <script>
        const canvas = document.getElementById('twinCanvas');
        const ctx = canvas.getContext('2d');
        const btn = document.getElementById('tapBtn');
        let progress = 0; let animating = false;
        const duration = {t_trans} * 60;

        function draw(p) {{
            ctx.clearRect(0,0,400,250);
            // Contacts
            ctx.fillStyle = '#cbd5e1';
            ctx.beginPath(); ctx.arc(100,125,15,0,7); ctx.fill();
            ctx.beginPath(); ctx.arc(300,125,15,0,7); ctx.fill();
            // Arm
            let angle = animating ? (p/duration)*Math.PI : 0;
            ctx.strokeStyle = '#0d9488'; ctx.lineWidth = 10; ctx.lineCap = 'round';
            ctx.beginPath(); ctx.moveTo(200,125);
            ctx.lineTo(200-Math.cos(angle)*100, 125+Math.sin(angle)*100); ctx.stroke();
            // Arc Spark
            if(animating && p > duration*0.4 && p < duration*0.6) {{
                ctx.fillStyle = '#f59e0b'; ctx.font='bold 14px Inter'; ctx.fillText('⚡ ARCING', 170, 50);
            }}
        }}
        function anim() {{
            if(!animating) return; progress++; draw(progress);
            if(progress<duration) requestAnimationFrame(anim); else {{ animating=false; progress=0; draw(0); }}
        }}
        btn.onclick = () => {{ if(!animating) {{ animating=true; anim(); }} }}
        draw(0);
    </script>
    """
    st.components.v1.html(canvas_html, height=400)

with col_right:
    st.subheader("📈 Motor Current Signature")
    t = np.linspace(0, t_trans + 0.5, 100)
    # Model: Startup inrush + nominal running
    i_sig = np.where(t < t_trans, (peak_i * 2 * np.exp(-3*t)) + (peak_i * 0.5), 0)
    chart_data = pd.DataFrame({"Time (s)": t, "Current (A)": i_sig}).set_index("Time (s)")
    st.line_chart(chart_data)

# --- ECONOMICS ---
st.markdown("---")
st.subheader("💰 Hardware Cost Analysis (Real-time Implementation)")
bom_data = {
    "Component": ["ESP32 Controller", "CT Clamp (SCT-013)", "Optocoupler (TLP521)", "Temp Probes (DS18B20)", "Casing & Power"],
    "Role": ["Edge Analytics", "Motor Current Sensing", "Safety Isolation", "Oil Temp Monitoring", "IP65 Protection"],
    "Cost (INR)": [380, 420, 90, 280, 460]
}
df_bom = pd.DataFrame(bom_data)
st.table(df_bom)
st.markdown(f"### **Total Estimated Cost per Unit: ₹1,630**")