import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="ProCARE CARE Portal", layout="wide")
HR_PASSWORD = "procareadmin" 

# --- 2. SESSION STATE (The Live Database) ---
if 'app_data' not in st.session_state:
    initial_data = {
        'Employee_ID': ['EMP-101', 'EMP-102', 'EMP-103', 'EMP-104', 'EMP-105'],
        'Mood_Score': [8, 3, 7, 2, 9],
        'Attendance_Rate': [95, 60, 88, 45, 100], 
        'Performance_Score': [9, 4, 8, 3, 10],
        'Sick_Days': [0, 4, 1, 6, 0],
        'Risk_Level': ['Low', 'High', 'Medium', 'Severe', 'Low'],
        'Checkin_Time': ["Baseline", "Baseline", "Baseline", "Baseline", "Baseline"]
    }
    st.session_state.app_data = pd.DataFrame(initial_data)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🛡️ ProCARE Portal")
    role = st.radio("Portal Access:", "Employee View", "HR Admin View")
    st.divider()
    st.info("CARE Initiative: Employee Wellness Monitoring")

# --- 4. EMPLOYEE VIEW (Tabs for Check-in & Breathing) ---
if role == "Employee View":
    st.header("🌟 Daily Wellness & Performance Pulse")
    
    tab1, tab2 = st.tabs(["📝 Daily Check-in", "Brain Reset (Breathing)"])

    with tab1:
        st.subheader("Professional & Physical Status")
        with st.form("pulse_form", clear_on_submit=True):
            mood = st.slider("How is your mental energy/mood today?", 1, 10, 7)
            
            col1, col2 = st.columns(2)
            with col1:
                att_status = st.selectbox("Current Work Status:", ["On-site", "Remote", "Late/Partial", "Sick Leave"])
            with col2:
                overtime = st.toggle("Worked >9 hours yesterday?")
            
            perf = st.select_slider("Rate your current productivity/focus:", options=range(1, 11), value=8)
            blockers = st.text_input("Any resource 'Blockers' or pay issues?")
            
            submit = st.form_submit_button("Submit Pulse to HR")

        if submit:
            # Logic to calculate values for the predictive model
            att_val = 100 if att_status in ["On-site", "Remote"] else (50 if att_status == "Late/Partial" else 0)
            risk = "Low"
            if mood <= 4 or att_val <= 50: risk = "High"
            if mood <= 2 and att_val <= 20: risk = "Severe"

            new_entry = {
                'Employee_ID': f"LIVE-{time.strftime('%H%M')}",
                'Mood_Score': mood,
                'Attendance_Rate': att_val,
                'Performance_Score': perf,
                'Sick_Days': 1 if att_status == "Sick Leave" else 0,
                'Risk_Level': risk,
                'Checkin_Time': time.strftime("%H:%M:%S")
            }
            st.session_state.app_data = pd.concat([st.session_state.app_data, pd.DataFrame([new_entry])], ignore_index=True)
            st.success("Pulse Captured. Your feedback helps ProCARE proactively manage wellbeing.")
            st.balloons()

    with tab2:
        st.subheader("Navy SEAL Box Breathing")
        st.write("Click below to start a 16-second cycle designed to reset your nervous system.")
        
        if st.button("Start 4-Round Reset"):
            phases = [
                ("Inhale 🌬️", "blue", "Deep breath in..."),
                ("Hold ✋", "green", "Keep the lungs full..."),
                ("Exhale 💨", "orange", "Release the breath..."),
                ("Hold 🛑", "red", "Wait for the next cycle...")
            ]
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for round_num in range(1, 5):
                st.write(f"Round {round_num} of 4")
                for phase, color, text in phases:
                    status_text.markdown(f"### :{color}[{phase}]")
                    st.caption(text)
                    for p in range(101):
                        time.sleep(0.035) 
                        progress_bar.progress(p)
            st.success("Brain Reset Complete. Great job taking a moment for yourself!")

# --- 5. HR VIEW (Admin Dashboard & Data Export) ---
elif role == "HR Admin View":
    pwd = st.text_input("Admin Password:", type="password")
    if pwd == HR_PASSWORD:
        st.header("📈 HR Burnout Statistics")
        df = st.session_state.app_data

        # --- DATA EXPORT FEATURE ---
        st.subheader("💾 Export Data")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Wellness Report (CSV)",
            data=csv,
            file_name=f"ProCARE_Wellness_Report_{time.strftime('%Y%m%d')}.csv",
            mime='text/csv',
        )
        st.divider()

        # Priority List
        st.subheader("🚨 Priority Outreach List")
        at_risk = df[df['Risk_Level'].isin(['High', 'Severe'])]
        if not at_risk.empty:
            st.dataframe(at_risk, use_container_width=True)
        else:
            st.success("All systems green. No critical burnout signals detected.")

        # Correlation Graph
        st.subheader("The Churn Predictor: Mood vs. Attendance")
        fig = px.scatter(df, x="Mood_Score", y="Attendance_Rate", 
                         size="Performance_Score", color="Risk_Level",
                         hover_name="Employee_ID",
                         color_discrete_map={"Severe": "red", "High": "orange", "Medium": "yellow", "Low": "green"})
        st.plotly_chart(fig, use_container_width=True)
    elif pwd:
        st.error("Invalid Credentials.")