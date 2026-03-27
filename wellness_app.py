import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- 1. CONFIG & BRANDING ---
st.set_page_config(page_title="ProCARE CARE Portal", layout="wide")
HR_PASSWORD = "procareadmin" 

# --- 2. DATA ENGINE ---
def get_procare_data():
    data = {
        'Employee_ID': ['EMP-101', 'EMP-102', 'EMP-103', 'EMP-104', 'EMP-105'],
        'Mood_Score': [8, 3, 7, 2, 9],
        'Attendance_Rate': [95, 60, 88, 45, 100], 
        'Risk_Level': ['Low', 'High', 'Medium', 'Severe', 'Low'],
        'Trend': ['Stable', 'Declining', 'Stable', 'Severe Drop', 'Stable']
    }
    return pd.DataFrame(data)

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
        st.toast("Pulse captured. Thank you for your honesty.")
        if mood <= 4:
            st.warning("It looks like you're carrying a lot today. Try the PFC reset below.")

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
        st.success("PFC Reset Complete. Great job taking care of yourself!")

# --- 5. HR VIEW ---
elif role == "HR Representative (Admin)":
    pwd = st.text_input("Enter Admin Password:", type="password")
    if pwd == HR_PASSWORD:
        st.header("📈 HR Retention Intelligence")
        df = get_procare_data()

        # Outreach Flags
        at_risk = df[(df['Mood_Score'] <= 4) | (df['Attendance_Rate'] < 70)]
        st.subheader("🚨 Priority Outreach List")
        
        if not at_risk.empty:
            st.write(at_risk[['Employee_ID', 'Mood_Score', 'Attendance_Rate', 'Risk_Level']])
            st.info("💡 Reach out to these individuals to offer flexible scheduling or wellness resources.")
        else:
            st.success("All systems green. No critical burnout signals detected.")

        # Risk Matrix
        fig = px.scatter(df, x="Mood_Score", y="Attendance_Rate", color="Risk_Level", 
                         size=[20, 20, 20, 20, 20], title="Mood vs Attendance Correlation")
        st.plotly_chart(fig)

    elif pwd:
        st.error("Access Denied.")