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
        'Employee_ID': ['EMP-101', 'EMP-102', 'EMP-103', 'EMP-104', 'EMP-105'],
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
# --- MANAGER DASHBOARD (Predictive Intelligence Layer) ---
elif role == "Manager Dashboard":
    pwd = st.text_input("Enter Manager Credentials:", type="password")
    if pwd == MANAGER_PASSWORD:
        st.header("📈 ProCARE Retention Intelligence")
        
        # Fetch the data
        df = get_procare_data()

        # SAFETY CHECK: Ensure all required columns exist for Plotly
        required_cols = ["Wellbeing_Score", "Attendance_Rate", "Sick_Leave_Spikes", "Risk_Level", "Trend", "Satisfaction_eNPS"]
        for col in required_cols:
            if col not in df.columns:
                df[col] = 0 if "Score" in col or "Rate" in col else "Unknown"

        # 2. Predictive Signal Matrix
        st.subheader("Predictive Signal Architecture: Attendance & Wellbeing")
        
        try:
            fig = px.scatter(df, 
                             x="Wellbeing_Score", 
                             y="Attendance_Rate", 
                             size="Sick_Leave_Spikes", 
                             color="Risk_Level",
                             hover_name="Employee_ID",
                             hover_data=["Trend", "Satisfaction_eNPS"],
                             color_discrete_map={
                                 "Severe": "red", "High": "orange", 
                                 "Medium": "yellow", "Low": "green"
                             },
                             title="ProCARE Risk Stratification")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Visualization Error: Missing Data Columns. Please check case_study_data.csv")