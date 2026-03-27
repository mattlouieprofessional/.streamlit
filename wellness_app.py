import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- 1. CONFIG & BRANDING ---
st.set_page_config(page_title="ProCARE CARE Portal", layout="wide")
HR_PASSWORD = "procareadmin" 

# --- 2. DATA ENGINE (Updated for Live Submissions) ---
def get_initial_data():
    data = {
        'Employee_ID': ['EMP-101', 'EMP-102', 'EMP-103', 'EMP-104', 'EMP-105'],
        'Mood_Score': [8, 3, 7, 2, 9],
        'Attendance_Rate': [95, 60, 88, 45, 100], 
        'Sick_Days_Recent': [0, 4, 1, 6, 0],
        'Risk_Level': ['Low', 'High', 'Medium', 'Severe', 'Low'],
        'Trend': ['Stable', 'Declining', 'Stable', 'Severe Drop', 'Stable'],
        'Satisfaction_eNPS': [9, 3, 8, 2, 10]
    }
    return pd.DataFrame(data)

# This block ensures the data persists while you switch between views
if 'app_data' not in st.session_state:
    st.session_state.app_data = get_initial_data()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("⚕️ ProCARE Portal")
    role = st.radio("Portal Access:", ["Employee (Check-in)", "HR Representative (Admin)"])
    st.divider()
    st.caption("Privacy-First & HIPAA Compliant")

# --- 4. EMPLOYEE VIEW ---
if role == "Employee (Check-in)":
    st.header("🌟 Daily CARE Pulse")
    
    # Positive Reinforcement
    st.success("😊 Your work today at ProCARE helps physicians focus on patients. You make an impact!")

    # Check-in Inputs
    col1, col2 = st.columns(2)
    with col1:
        mood = st.slider("How is your mood/stress today?", 1, 10, 7)
    with col2:
        attendance = st.selectbox("Work Status:", ["On-site", "Remote", "Sick/Personal Leave"])

    if st.button("Submit Pulse"):
        # Create the new entry based on user input
        new_entry = {
            'Employee_ID': "LIVE-SUBMISSION",
            'Mood_Score': mood,
            'Attendance_Rate': 100 if attendance == "On-site" else (80 if attendance == "Remote" else 20),
            'Sick_Days_Recent': 1 if attendance == "Sick/Personal Leave" else 0,
            'Risk_Level': "Low" if mood > 5 else "High",
            'Trend': "Recent Change",
            'Satisfaction_eNPS': 5 # Default value
        }
        
        # Add the new row to our 'Live' session database
        st.session_state.app_data = pd.concat([st.session_state.app_data, pd.DataFrame([new_entry])], ignore_index=True)
        
        st.success("Pulse Captured! Thank you for providing your honest feedback. Take a minute to take a breath break.")
        st.balloons()
    # --- INTERACTIVE NAVY SEAL BREATHING ---
    st.divider()
    st.subheader("Navy SEAL Box Breathing (Interactive)")
    st.write("Click 'Start' and follow the visual cues to reset your nervous system.")

    if st.button(" Start Breathing Exercise"):
        phases = [
            ("Inhale", "blue", "Fill your lungs slowly..."),
            ("Hold", "green", "Keep the air in..."),
            ("Exhale", "orange", "Release all tension..."),
            ("Hold", "red", "Wait for the next breath...")
        ]
        
        # Progress Bar for Visual Feedback
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(4): # 4 Rounds
            for phase, color, instruction in phases:
                status_text.markdown(f"### :{color}[{phase}]")
                st.write(instruction)
                # 4 seconds per phase
                for percent in range(101):
                    time.sleep(0.035) # Approx 4 seconds total
                    progress_bar.progress(percent)
        
        st.balloons()
        st.success("Brain Break Complete. Great job taking care of yourself!")

# --- 5. HR VIEW ---
# --- 5. HR VIEW: INTERVENTION & OUTREACH ---
elif role == "HR Representative (Admin)":
    # Define the variable by taking the input immediately
    pwd = st.text_input("Enter Admin Password:", type="password")
    
    if pwd == HR_PASSWORD:
        st.header("📈 HR Wellness & Outreach Dashboard")
        st.write("Target: Identifying churn risk 60-90 days in advance.") 
        
        # Use the session data for live updates
        display_df = st.session_state.app_data

        # 1. Identify At-Risk Employees (The Predictive Layer) [cite: 41]
        # Filtering for low mood or low attendance as burnout precursors [cite: 66]
        at_risk = display_df[(display_df['Mood_Score'] <= 4) | (display_df['Attendance_Rate'] < 70)]

        st.subheader("🚨 Priority Outreach List")
        if not at_risk.empty:
            st.write(at_risk)
            st.info("💡 ProCARE CARE Tip: Reach out to offer workload adjustments or 1:1 check-ins.") 
        else:
            st.success("No high-risk signals detected at this time.")

        # 2. Visualization (The Retention Intelligence Layer) [cite: 15, 17]
        fig = px.scatter(display_df, 
                         x="Mood_Score", 
                         y="Attendance_Rate", 
                         size="Sick_Days_Recent", 
                         color="Risk_Level",
                         hover_name="Employee_ID",
                         title="Retention Intelligence: Mood vs. Attendance Correlation") 
        st.plotly_chart(fig, use_container_width=True)

    elif pwd != "":  # Only show error if they actually typed something wrong
        st.error("Unauthorized Access. Please check your credentials.")