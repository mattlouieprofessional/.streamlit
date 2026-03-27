import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="ProCARE CARE Portal", layout="wide")
HR_PASSWORD = "procare_admin" 

# --- 2. SESSION STATE (The Live Multi-Dimension Database) ---
if 'app_data' not in st.session_state:
    initial_data = {
        'Employee_ID': ['EMP-101', 'EMP-102', 'EMP-103', 'EMP-104', 'EMP-105'],
        'Mood_Score': [8, 3, 7, 2, 9],
        'Attendance_Rate': [95, 60, 88, 45, 100], 
        'Status': ["On-site", "Sick Leave", "Remote", "Sick Leave", "On-site"],
        'Overtime': ["No", "Yes", "No", "Yes", "No"],
        'Performance_Score': [9, 4, 8, 3, 10],
        'Blockers': ["None", "Heavy Workload", "None", "System Latency", "None"],
        'Risk_Level': ['Low', 'High', 'Medium', 'Severe', 'Low'],
        'Checkin_Time': ["Baseline", "Baseline", "Baseline", "Baseline", "Baseline"]
    }
    st.session_state.app_data = pd.DataFrame(initial_data)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🛡️ ProCARE Portal")
    role = st.radio("Portal Access:", ["Employee View", "HR Admin View"])
    st.divider()
    st.info("CARE Initiative: Holistic Wellness & Retention Intelligence")

# --- 4. EMPLOYEE VIEW (Tabs for Action & Reset) ---
if role == "Employee View":
    st.header("🌟 Daily Wellness & Performance Pulse")
    emp_tabs = st.tabs(["📝 Daily Check-in", "🌊 PFC Reset (Breathing)"])

    with emp_tabs[0]:
        st.subheader("Professional & Physical Status")
        with st.form("pulse_form", clear_on_submit=True):
            mood = st.slider("Mental Energy/Mood (1-10):", 1, 10, 7)
            
            col1, col2 = st.columns(2)
            with col1:
                att_status = st.selectbox("Current Work Status:", ["On-site", "Remote", "Late/Partial", "Sick Leave"])
            with col2:
                overtime = st.toggle("Worked >9 hours yesterday?")
            
            perf = st.select_slider("Productivity/Focus Level:", options=range(1, 11), value=8)
            blockers = st.text_input("Resource Blockers / Agency Deficits (Optional):")
            
            submit = st.form_submit_button("Submit Pulse to HR")

        if submit:
            att_val = 100 if att_status in ["On-site", "Remote"] else (50 if att_status == "Late/Partial" else 0)
            risk = "Low"
            if mood <= 4 or att_val <= 50: risk = "High"
            if mood <= 2 and att_val <= 20: risk = "Severe"

            new_entry = {
                'Employee_ID': f"LIVE-{time.strftime('%M%S')}",
                'Mood_Score': mood,
                'Attendance_Rate': att_val,
                'Status': att_status,
                'Overtime': "Yes" if overtime else "No",
                'Performance_Score': perf,
                'Blockers': blockers if blockers else "None",
                'Risk_Level': risk,
                'Checkin_Time': time.strftime("%H:%M:%S")
            }
            st.session_state.app_data = pd.concat([st.session_state.app_data, pd.DataFrame([new_entry])], ignore_index=True)
            st.success("Pulse Captured. Thank you for helping us maintain a CARE culture.")
            st.balloons()

    with emp_tabs[1]:
        st.subheader("Navy SEAL Box Breathing")
        st.write("Reset your nervous system with a 16-second cycle.")
        if st.button("🚀 Start 4-Round Reset"):
            phases = [("Inhale 🌬️", "blue"), ("Hold ✋", "green"), ("Exhale 💨", "orange"), ("Hold 🛑", "red")]
            progress_bar = st.progress(0)
            status_text = st.empty()
            for r in range(1, 5):
                for phase, color in phases:
                    status_text.markdown(f"### :{color}[{phase}] (Round {r}/4)")
                    for p in range(101):
                        time.sleep(0.035) 
                        progress_bar.progress(p)
            st.success("PFC Reset Complete.")

# --- 5. HR ADMIN VIEW (Analytical Dashboard with Tabs) ---
elif role == "HR Admin View":
    pwd = st.text_input("Admin Password:", type="password")
    if pwd == HR_PASSWORD:
        st.header("📈 Retention Intelligence Center")
        df = st.session_state.app_data
        
        hr_tabs = st.tabs(["📊 Executive Dashboard", "🎯 Risk Matrix", "📋 Master Data Tracker"])

        with hr_tabs[0]: # Executive Dashboard
            st.subheader("Workforce Health KPIs")
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Org Mood Index", f"{round(df['Mood_Score'].mean(), 1)}/10")
            k2.metric("Avg Attendance", f"{round(df['Attendance_Rate'].mean(), 1)}%")
            k3.metric("High-Risk Flags", len(df[df['Risk_Level'].isin(['High', 'Severe'])]))
            k4.metric("Focus Score", f"{round(df['Performance_Score'].mean(), 1)}/10")
            
            st.divider()
            st.subheader("Risk Distribution")
            fig_pie = px.pie(df, names='Risk_Level', color='Risk_Level',
                             color_discrete_map={"Severe": "red", "High": "orange", "Medium": "yellow", "Low": "green"})
            st.plotly_chart(fig_pie, use_container_width=True)

        with hr_tabs[1]: # Interactive Graphs
            st.subheader("Predictive Signal Architecture")
            fig_scatter = px.scatter(df, x="Mood_Score", y="Attendance_Rate", 
                                     size="Performance_Score", color="Risk_Level",
                                     hover_data=["Status", "Overtime", "Blockers"],
                                     title="Correlation: Mood vs. Attendance (Bubble Size = Performance)",
                                     color_discrete_map={"Severe": "red", "High": "orange", "Medium": "yellow", "Low": "green"})
            st.plotly_chart(fig_scatter, use_container_width=True)
            st.info("💡 Identifying 'Longitudinal Trends' (60-90 day lead time) by analyzing low mood + low attendance coordinates.")

        with hr_tabs[2]: # Master Data Tracker
            st.subheader("Full Wellness Signal Log")
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Full Analytical Report", data=csv, 
                               file_name="ProCARE_Retention_Report.csv", mime='text/csv')

    elif pwd:
        st.error("Invalid Admin Credentials.")