import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- CONFIG & BRANDING ---
st.set_page_config(page_title="ProCARE CARE Portal", layout="wide")
MANAGER_PASSWORD = "procareadmin"

# --- MOCK DATA: LONGITUDINAL TRENDS ---
# ProCARE requires tracking signals over time to predict churn [cite: 66, 69]
def get_procare_data():
    data = {
        'Employee_ID': ['EMP-1', 'EMP-2', 'EMP-3', 'EMP-4', 'EMP-5'],
        'Wellbeing_Score': [8.5, 4.2, 7.8, 3.5, 9.2],
        'Attendance_Rate': [98, 65, 92, 45, 100], # Attendance % [cite: 66]
        'Sick_Leave_Spikes': [0, 5, 1, 7, 0], # Recent unexpected leave [cite: 61]
        'Satisfaction_eNPS': [9, 3, 8, 2, 10], # Employee Net Promoter Score [cite: 66]
        'Risk_Tier': ['Low', 'High', 'Medium', 'Severe', 'Low'],
        'Trend': ['Stable', 'Declining', 'Stable', 'Severe Drop', 'Stable']
    }
    return pd.DataFrame(data)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ ProCARE Portal")
    st.write("CARE Initiative: Wellness & Retention")
    role = st.radio("Select View:", ["Employee Check-in", "Manager Dashboard"])

# --- VIEW 1: EMPLOYEE CHECK-IN ---
if role == "Employee Check-in":
    st.header("🌟 CARE Daily Pulse")
    st.info("Continuous evaluation of holistic state: Physical, Mental, and Professional.")

    # Wellbeing & Satisfaction
    st.subheader("1. Holistic Wellbeing")
    wellbeing = st.slider("Rate your overall wellbeing (Mental/Physical) today:", 1, 10, 7)
    
    st.subheader("2. Workplace Satisfaction")
    satisfaction = st.select_slider(
        "How likely are you to recommend ProCARE as a great place to work?",
        options=range(1, 11), value=8
    )

    if st.button("Submit Pulse"):
        st.success("Data captured anonymously. Thank you for contributing to our CARE Culture.")
        st.balloons()

    # Navy SEAL Intervention (PFC Engagement)
    st.divider()
    st.subheader("Navy SEAL Box Breathing")
    st.write("Goal: Reset your nervous system and re-engage your Prefrontal Cortex.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Inhale", "4 Sec")
    col2.metric("Hold", "4 Sec")
    col3.metric("Exhale", "4 Sec")
    col4.metric("Hold", "4 Sec")
    
    st.caption("Repeat 4 times to shift from 'Stress Mode' to 'Executive Focus'.")

# --- VIEW 2: MANAGER DASHBOARD ---
elif role == "Manager Dashboard":
    pwd = st.text_input("Enter Manager Credentials:", type="password")
    if pwd == MANAGER_PASSWORD:
        st.header("📈 Retention Intelligence Dashboard")
        st.write("Identify burnout and churn risk 60-90 days in advance.")
        
        df = get_procare_data()

        # Key Metrics [cite: 75]
        m1, m2, m3 = st.columns(3)
        m1.metric("Avg. Wellbeing", f"{df['Wellbeing_Score'].mean()}/10")
        m2.metric("Attendance Stability", f"{df['Attendance_Rate'].mean()}%")
        m3.metric("High-Risk Alerts", "2")

        # Attendance vs. Wellbeing Matrix [cite: 66]
        st.subheader("Predictive Signal Architecture: Attendance & Wellbeing Trends")
        # Attendance vs. Wellbeing Matrix
        st.subheader("Predictive Signal Architecture: Attendance & Wellbeing Trends")
        
        # Proactive Model: Mapping key wellness signals to identify at-risk employees (cite: 41, 46)
        fig = px.scatter(df, 
                         x="Wellbeing_Score", 
                         y="Attendance_Rate", 
                         size="Sick_Leave_Spikes", 
                         color="Risk_Level",
                         hover_name="Employee_ID",
                         # Includes Trends and Satisfaction (eNPS) as predictive relevance (cite: 66)
                         hover_data=["Trend", "Satisfaction_eNPS"], 
                         title="ProCARE Risk Stratification Matrix")
        
        st.plotly_chart(fig, use_container_width=True)
        st.plotly_chart(fig, use_container_width=True)

        # Risk Stratification [cite: 54, 55]
        st.subheader("Risk Tier Monitoring")
        st.dataframe(df.style.highlight_max(axis=0, subset=['Sick_Leave_Spikes'], color='#ffcccc'))

        # Intervention Playbooks [cite: 56, 80]
        st.divider()
        st.subheader("Targeted Interventions")
        selected = st.selectbox("Review at-risk employee:", df[df['Risk_Level'] != 'Low']['Employee_ID'])
        
        if selected:
            st.warning(f"Warning: {selected} shows declining attendance and satisfaction trends.")
            st.write("**Action Plan:**")
            st.write("- [ ] **Workload Audit:** Review after-hours login frequency.")
            st.write("- [ ] **Manager Check-in:** Address perceived loss of autonomy.")
            st.write("- [ ] **Recognition Cycle:** Ensure employee has received recent feedback.")

    elif pwd:
        st.error("Invalid Credentials.")