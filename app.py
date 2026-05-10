import streamlit as st
import pandas as pd
import plotly.express as px

from ai.medical_ai import (
    medical_response,
    explain_medical_report
)

from parser.document_parser import extract_text

from utils.text_cleaner import (
    clean_text,
    split_text
)

from vectorstore.faiss_store import (
    create_vector_store,
    search_vector_store
)

from rag.rag_pipeline import (
    generate_medical_answer
)

from auth.auth import login_ui

from database.db_manager import (
    save_history,
    load_history
)

from analyzer.report_analyzer import (
    extract_medical_values,
    analyze_medical_values
)

from ml.disease_predictor import (
    predict_diabetes,
    predict_heart_disease,
    calculate_health_score
)

from voice.listen import (
    listen_to_patient
)

from voice.speak import (
    speak_text
)

from memory.patient_memory import (
    build_patient_memory
)

from doctor.appointment_manager import (
    book_appointment,
    load_appointments
)

from doctor.doctor_tools import (
    update_appointment_status,
    save_doctor_notes,
    load_doctor_appointments
)

from admin.admin_tools import (
    load_users,
    delete_user,
    load_all_appointments,
    load_doctors,
    approve_doctor,
    load_pending_doctors
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MedAssist AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PREMIUM UI
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
    linear-gradient(
        135deg,
        #F8FAFC,
        #EEF2FF
    );
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

h1, h2, h3 {
    color: #0F172A;
    font-weight: 700;
}

[data-testid="stSidebar"] {
    background:
    linear-gradient(
        180deg,
        #0F172A,
        #1E293B
    );
}

[data-testid="stSidebar"] * {
    color: white;
}

[data-testid="metric-container"] {

    background:
    rgba(255,255,255,0.75);

    border:
    1px solid rgba(255,255,255,0.3);

    padding: 20px;

    border-radius: 22px;

    backdrop-filter: blur(12px);

    box-shadow:
    0 8px 32px rgba(31,38,135,0.12);

    transition: 0.3s;
}

[data-testid="metric-container"]:hover {

    transform: translateY(-5px);

    box-shadow:
    0 12px 40px rgba(31,38,135,0.2);
}

.stButton > button {

    background:
    linear-gradient(
        135deg,
        #2563EB,
        #7C3AED
    );

    color: white;

    border: none;

    border-radius: 14px;

    padding: 12px 22px;

    font-weight: 600;

    transition: 0.3s;

    width: 100%;
}

.stButton > button:hover {

    transform: scale(1.02);

    box-shadow:
    0 8px 20px rgba(37,99,235,0.35);
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div,
.stNumberInput input {

    border-radius: 14px !important;

    border: 1px solid #CBD5E1 !important;

    background: white !important;
}

[data-testid="stFileUploader"] {

    background: white;

    border-radius: 18px;

    padding: 20px;

    border: 2px dashed #94A3B8;
}

[data-testid="stDataFrame"] {

    border-radius: 18px;

    overflow: hidden;

    border: 1px solid #E2E8F0;
}

.stAlert {
    border-radius: 16px;
}

.hero-card {

    background:
    linear-gradient(
        135deg,
        #2563EB,
        #7C3AED
    );

    padding: 40px;

    border-radius: 28px;

    color: white;

    margin-bottom: 30px;

    box-shadow:
    0 12px 35px rgba(0,0,0,0.15);
}

.chat-card {

    background: white;

    padding: 22px;

    border-radius: 18px;

    margin-bottom: 18px;

    box-shadow:
    0 4px 12px rgba(0,0,0,0.06);
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = "Patient"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "index" not in st.session_state:
    st.session_state.index = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

# =========================================================
# LOGIN
# =========================================================

if not st.session_state.logged_in:

    st.title("🩺 MedAssist AI")

    st.markdown("""
    <div class="hero-card">

    <h1 style="color:white;">
    🏥 Enterprise Healthcare AI Platform
    </h1>

    <p style="font-size:18px; opacity:0.95;">

    AI-powered healthcare intelligence platform with:

    ✔ Medical AI Assistant  
    ✔ OCR + RAG Analysis  
    ✔ Disease Prediction  
    ✔ Doctor Workflows  
    ✔ Admin Analytics  
    ✔ Voice AI  
    ✔ Enterprise Security  

    </p>

    </div>
    """, unsafe_allow_html=True)

    login_ui()

    st.stop()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🩺 MedAssist AI")

st.sidebar.success(
    f"""
👤 User: {st.session_state.username}

🛡️ Role: {st.session_state.role}
"""
)

# =========================================================
# NAVIGATION
# =========================================================

if st.session_state.role == "Patient":

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Upload Reports",
            "Predictions",
            "Appointments",
            "Voice Assistant",
            "Medical Chat"
        ]
    )

elif st.session_state.role == "Doctor":

    page = st.sidebar.radio(
        "Navigation",
        [
            "Doctor Dashboard"
        ]
    )

else:

    page = st.sidebar.radio(
        "Navigation",
        [
            "Admin Dashboard"
        ]
    )

# =========================================================
# LOGOUT
# =========================================================

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False

    st.rerun()

# =========================================================
# TITLE
# =========================================================

st.title("🩺 MedAssist AI")

history = load_history(
    st.session_state.username
)

appointments = load_appointments()

# =========================================================
# PATIENT DASHBOARD
# =========================================================

if st.session_state.role == "Patient":

    if page == "Dashboard":

        st.header("👤 Patient Dashboard")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Consultations",
            len(history)
        )

        c2.metric(
            "Appointments",
            len(appointments)
        )

        c3.metric(
            "Role",
            "Patient"
        )

        st.markdown("---")

        patient_memory = build_patient_memory(
            history
        )

        st.subheader("🧠 Smart Medical Memory")

        st.info(patient_memory)

    elif page == "Medical Chat":

        st.header("🤖 Medical Assistant")

        symptoms = st.text_area(
            "Ask medical questions"
        )

        if st.button("Analyze"):

            patient_memory = build_patient_memory(
                history
            )

            answer = medical_response(
                symptoms,
                patient_memory
            )

            st.markdown(
                f"""
                <div class="chat-card">

                <h4>🧑 Patient</h4>
                <p>{symptoms}</p>

                <hr>

                <h4>🤖 MedAssist AI</h4>
                <p>{answer}</p>

                </div>
                """,
                unsafe_allow_html=True
            )

            save_history(
                st.session_state.username,
                symptoms,
                answer
            )

# =========================================================
# ADMIN DASHBOARD
# =========================================================

elif st.session_state.role == "Admin":

    st.header("🛡️ Enterprise Admin Dashboard")

    users = load_users()

    appointments = load_all_appointments()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Users", len(users))

    c2.metric(
        "Patients",
        len([
            u for u in users
            if u[1] == "Patient"
        ])
    )

    c3.metric(
        "Doctors",
        len([
            u for u in users
            if u[1] == "Doctor"
        ])
    )

    c4.metric(
        "Appointments",
        len(appointments)
    )

    st.markdown("---")

    st.subheader("🩺 Doctor Approval Requests")

    pending_doctors = load_pending_doctors()

    if pending_doctors:

        for doctor in pending_doctors:

            doctor_name = doctor[0]

            c1, c2 = st.columns([4,1])

            c1.write(
                f"👨‍⚕️ {doctor_name}"
            )

            if c2.button(
                f"Approve {doctor_name}"
            ):

                approve_doctor(
                    doctor_name
                )

                st.success(
                    f"{doctor_name} approved!"
                )

                st.rerun()

    else:

        st.info(
            "No pending doctor approvals."
        )

    st.markdown("---")

    st.subheader("👥 User Management")

    users_df = pd.DataFrame(
        users,
        columns=[
            "Username",
            "Role",
            "Approved"
        ]
    )

    st.dataframe(
        users_df,
        use_container_width=True
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<hr>

<div style="
text-align:center;
padding:25px;
color:#64748B;
font-size:14px;
">

Built with ❤️ using
AI + ML + RAG + Streamlit

<br><br>

© 2026 MedAssist AI Enterprise Platform

</div>
""", unsafe_allow_html=True)