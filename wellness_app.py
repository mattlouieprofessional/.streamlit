import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from textblob import TextBlob

# --- CONFIG & PROCARE BRANDING ---
st.set_page_config(page_title="ProCARE CARE Initiative", layout="wide")
MANAGER_PASSWORD = "procareadmin"

# --- MOCK DATA GENERATOR (Longitudinal Trends) ---
# ProCARE requires tracking how wellness changes over time [cite: 69, 70]
def get_procare_data():
    data = {
        'Employee_ID': ['EMP-1', 'EMP-2', 'EMP-3', 'EMP-4', 'EMP-5'],
        'Department': ['Clinical', 'Admin', 'Clinical', 'IT', 'Operations'],
        'Satisfaction_eNPS': [9, 4, 8, 3, 10], # 0-10 scale 
        'Attendance_Score': [95, 60, 85, 40, 98], # % of expected presence
        'Sick_Leave_Spikes': [0, 4, 1, 6, 0], # Recent unexpected leave 
        'PTO_Utilization': [80, 10, 75, 5, 100], # % used 
        'Risk_Level': ['Low', 'High', 'Medium', 'Severe', 'Low'],
        'Trend': ['Stable', 'Declining', 'Stable', 'Severe Drop', 'Stable']
    }
    return pd.DataFrame(data)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("Employee ProCARE Portal")
    st.write("Wellness & Retention Intelligence [cite: 17]")
    role = st.radio("Select View:", ["Employee Check-in", "Manager Dashboard"])
    st.divider()
    st.caption("Confidential & Privacy-First [cite: 59, 76]")

# --- VIEW 1: EMPLOYEE CHECK-IN (Data Collection Layer) ---
if role == "Employee Check-in":
    st.header("🌟 Daily CARE for those who care")
    st.info("Your input helps ProCARE proactively to improve wellbeing in the workplace [cite: 11].")

    # 1. Mental/Emotional (Sentiment Analysis)
    st.subheader("1. Mental & Emotional State")
    reflection = st.text_area("How are you feeling about your workload and impact today?")
    
    # 2. Satisfaction (eNPS) - Professional Fulfillment [cite: 63]
    st.subheader("2. Workplace Satisfaction")
    sat_score = st.select_slider(
        "How satisfied do you feel on your usual workday?",
        options=range(1, 11), value=7
    )

    # 3. Physical/Attendance Context [cite: 61, 63]
    st.subheader("3. Physical & Work-Life Balance")
    col1, col2 = st.columns(2)
    with col1:
        energy = st.slider("Energy Level", 1, 10, 5)
    with col2:
        autonomy = st.slider("Sense of Autonomy over Schedule", 1, 10, 5)

    if st.button("Submit Anonymous Pulse"):
        # Process Sentiment
        sentiment = TextBlob(reflection).sentiment.polarity
        if sentiment < 0 and sat_score < 5:
            st.warning("Detection: High Dissonance. Please consider a 5-minute brain break below.")
        else:
            st.success("Pulse Captured. Thank you for contributing to our CARE Culture[cite: 8].")
        st.balloons()

    # PFC Engagement Section (The Intervention) [cite: 81]
    st.divider()
    st.subheader("🧠 PFC Reset (Grounding Exercise)")
    st.write("Shift from reactive stress to executive focus.")
    st.video("https://www.youtube.com/watch?v=sj8Sg8qnjOg") 

# --- VIEW 2: MANAGER DASHBOARD (Predictive Intelligence Layer) ---
elif role == "Manager Dashboard":
    pwd = st.text_input("Enter Manager Credentials:", type="password")
    if pwd == MANAGER_PASSWORD:
        st.header("📈 Retention Intelligence Engine")
        st.write("Predicting churn risk 60-90 days before disengagement[cite: 36].")
        
        df = get_procare_data()

        # Metrics Overview
        m1, m2, m3 = st.columns(3)
        m1.metric("Avg. Team Satisfaction", f"{df['Satisfaction_eNPS'].mean()}/10", "-5% Trend")
        m2.metric("Attendance Stability", "75.6%", "-12% Trend")
        m3.metric("High-Risk Alerts", "2", "+1 Total")

        # Attendance vs. Satisfaction Correlation
        st.subheader("The Churn Predictor: Satisfaction vs. Attendance")
        fig = px.scatter(df, x="Satisfaction_eNPS", y="Attendance_Score", 
                         size="Sick_Leave_Spikes", color="Risk_Level",
                         hover_name="Employee_ID", title="Risk Stratification Matrix [cite: 54, 55]")
        st.plotly_chart(fig, use_container_width=True)

        # Risk Tier Table
        st.subheader("Employee Risk Tiers & Predictive Signals ")
        
        def color_risk(val):
            if val in ['High', 'Severe']: return 'background-color: #ffcccc'
            if val == 'Medium': return 'background-color: #fff4cc'
            return ''

        st.table(df.style.applymap(color_risk, subset=['Risk_Level']))

        # Intervention Playbooks [cite: 56, 57]
        st.divider()
        st.subheader("Actionable Interventions")
        selected = st.selectbox("Select Employee for Intervention Plan:", df['Employee_ID'])
        emp_data = df[df['Employee_ID'] == selected].iloc[0]

        if emp_data['Risk_Level'] in ['High', 'Severe']:
            st.error(f"ALERT: {selected} shows 'Severe Drop' in attendance and 'Extreme Underuse' of PTO.")
            st.write("**Recommended Intervention:**")
            st.write("- [ ] Immediate Manager 1:1 to address 'Perceived Agency Deficit'.")
            st.write("- [ ] Mandatory 'Wellness Break' / PTO encouragement to prevent burnout.")
            st.write("- [ ] Workload audit to identify after-hours work patterns.")
        else:
            st.success(f"{selected} is currently in the Low-Risk tier. Maintain standard recognition cycles.")

    elif pwd:
        st.error("Access Denied.")