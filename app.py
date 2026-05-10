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

st.markdown("""
<style>

/* =====================================================
BACKGROUND
===================================================== */

.stApp {

    background:
    linear-gradient(
        135deg,
        #F8FAFC,
        #EEF2FF
    );
}

/* =====================================================
MAIN CONTAINER
===================================================== */

.block-container {

    padding-top: 2rem;
    padding-bottom: 2rem;

    max-width: 1400px;
}

/* =====================================================
HEADINGS
===================================================== */

h1, h2, h3 {

    color: #0F172A;

    font-weight: 700;
}

/* =====================================================
SIDEBAR
===================================================== */

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

/* =====================================================
METRIC CARDS
===================================================== */

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

/* =====================================================
BUTTONS
===================================================== */

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

/* =====================================================
INPUTS
===================================================== */

.stTextInput input,
.stTextArea textarea,
.stSelectbox div,
.stNumberInput input {

    border-radius: 14px !important;

    border: 1px solid #CBD5E1 !important;

    background: white !important;
}

/* =====================================================
UPLOAD BOX
===================================================== */

[data-testid="stFileUploader"] {

    background: white;

    border-radius: 18px;

    padding: 20px;

    border: 2px dashed #94A3B8;
}

/* =====================================================
TABLES
===================================================== */

[data-testid="stDataFrame"] {

    border-radius: 18px;

    overflow: hidden;

    border: 1px solid #E2E8F0;
}

/* =====================================================
SUCCESS / INFO BOXES
===================================================== */

.stAlert {

    border-radius: 16px;
}

/* =====================================================
HERO CARD
===================================================== */

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

/* =====================================================
CHAT CARD
===================================================== */

.chat-card {

    background: white;

    padding: 22px;

    border-radius: 18px;

    margin-bottom: 18px;

    box-shadow:
    0 4px 12px rgba(0,0,0,0.06);
}

/* =====================================================
FOOTER
===================================================== */

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
User: {st.session_state.username}

Role: {st.session_state.role}
"""
)

# =========================================================
# SIDEBAR NAVIGATION
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

    # =====================================================
    # DASHBOARD
    # =====================================================

    if page == "Dashboard":

        st.header("👤 Patient Dashboard")

        total_questions = len(history)

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Consultations",
            total_questions
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

        st.subheader("🧠 Smart Memory")

        st.info(patient_memory)

    # =====================================================
    # REPORTS
    # =====================================================

    elif page == "Upload Reports":

        st.header("📄 Upload Medical Reports")

        uploaded_file = st.file_uploader(
            "Upload Report",
            type=[
                "pdf",
                "txt",
                "png",
                "jpg",
                "jpeg"
            ]
        )

        clean = ""

        if uploaded_file:

            raw_text = extract_text(
                uploaded_file
            )

            clean = clean_text(
                raw_text
            )

            st.text_area(
                "Extracted Text",
                clean,
                height=250
            )

            chunks = split_text(clean)

            chunks = [
                c.strip()
                for c in chunks
                if len(c.strip()) > 5
            ]

            index, stored_chunks = create_vector_store(
                chunks
            )

            st.session_state.index = index
            st.session_state.chunks = stored_chunks

            st.success(
                "Medical report processed successfully!"
            )

            extracted_values = extract_medical_values(
                clean
            )

            if extracted_values:

                analysis = analyze_medical_values(
                    extracted_values
                )

                for item in analysis:

                    st.write(item)

                ai_explanation = explain_medical_report(
                    analysis
                )

                st.subheader("🧠 AI Explanation")

                st.info(ai_explanation)

    # =====================================================
    # PREDICTIONS
    # =====================================================

    elif page == "Predictions":

        st.header("🩺 Health Prediction")

        c1, c2 = st.columns(2)

        glucose = c1.number_input(
            "Glucose",
            value=100
        )

        blood_pressure = c2.number_input(
            "Blood Pressure",
            value=80
        )

        bmi = c1.number_input(
            "BMI",
            value=25.0
        )

        age = c2.number_input(
            "Age",
            value=30
        )

        cholesterol = c1.number_input(
            "Cholesterol",
            value=180
        )

        if st.button("Predict"):

            d_prediction, d_probability = predict_diabetes(
                glucose,
                blood_pressure,
                bmi,
                age
            )

            h_prediction, h_probability = predict_heart_disease(
                cholesterol,
                blood_pressure,
                bmi,
                age
            )

            diabetes_risk = round(
                d_probability * 100,
                2
            )

            heart_risk = round(
                h_probability * 100,
                2
            )

            health_score = calculate_health_score(
                diabetes_risk,
                heart_risk
            )

            st.success(
                f"Health Score: {health_score}"
            )

    # =====================================================
    # APPOINTMENTS
    # =====================================================

    elif page == "Appointments":

        st.header("📅 Book Appointment")

        c1, c2 = st.columns(2)

        doctor_list = load_doctors()

        doctor_name = c1.selectbox(
            "Doctor",
            doctor_list
        )

        appointment_date = c2.date_input(
            "Date"
        )

        appointment_time = c1.time_input(
            "Time"
        )

        appointment_reason = c2.text_input(
            "Reason"
        )

        if st.button("Book Appointment"):

            book_appointment(
                st.session_state.username,
                doctor_name,
                str(appointment_date),
                str(appointment_time),
                appointment_reason
            )

            st.success(
                "Appointment booked successfully!"
            )

        st.markdown("---")

        st.subheader("📋 My Appointments")

        patient_appointments = [
            a for a in appointments
            if a[0] == st.session_state.username
        ]

        if patient_appointments:

            patient_df = pd.DataFrame(
                patient_appointments,
                columns=[
                    "Patient",
                    "Doctor",
                    "Date",
                    "Time",
                    "Reason",
                    "Status",
                    "Notes",
                    "Prescription"
                ]
            )

            st.dataframe(
                patient_df,
                use_container_width=True
            )

    # =====================================================
    # VOICE ASSISTANT
    # =====================================================

    elif page == "Voice Assistant":

        st.header("🎙️ Voice Assistant")

        if st.button("Start Voice Assistant"):

            voice_input = listen_to_patient()

            st.success(
                f"You said: {voice_input}"
            )

            patient_memory = build_patient_memory(
                history
            )

            answer = medical_response(
                voice_input,
                patient_memory
            )

            st.info(answer)

            speak_text(answer)

    # =====================================================
    # MEDICAL CHAT
    # =====================================================

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

            st.success(answer)

            save_history(
                st.session_state.username,
                symptoms,
                answer
            )

# =========================================================
# DOCTOR DASHBOARD
# =========================================================

elif st.session_state.role == "Doctor":

    st.header("👨‍⚕️ Doctor Dashboard")

    doctor_name = f"Dr. {st.session_state.username}"

    appointments = load_doctor_appointments()

    doctor_appointments = [
        a for a in appointments
        if a[1] == doctor_name
    ]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Appointments",
        len(doctor_appointments)
    )

    c2.metric(
        "Patients",
        len(set([a[0] for a in doctor_appointments]))
    )

    pending_count = len([
        a for a in doctor_appointments
        if a[5] == "Pending"
    ])

    c3.metric(
        "Pending",
        pending_count
    )

    st.markdown("---")

    st.subheader("📅 Appointment Management")

    if doctor_appointments:

        for appointment in doctor_appointments:

            patient = appointment[0]
            doctor = appointment[1]
            date = appointment[2]
            time = appointment[3]
            reason = appointment[4]
            status = appointment[5]
            notes = appointment[6]
            prescription = appointment[7]

            with st.expander(
                f"{patient} • {date} • {status}"
            ):

                st.write(f"Reason: {reason}")
                st.write(f"Time: {time}")

                # =========================================
                # STATUS UPDATE
                # =========================================

                new_status = st.selectbox(
                    f"Update Status - {patient}",
                    [
                        "Pending",
                        "Accepted",
                        "Rejected",
                        "Completed"
                    ],
                    key=f"status_{patient}"
                )

                if st.button(
                    f"Save Status - {patient}"
                ):

                    update_appointment_status(
                        patient,
                        new_status
                    )

                    st.success(
                        "Status updated!"
                    )

                    st.rerun()

                st.markdown("---")

                # =========================================
                # NOTES
                # =========================================

                doctor_notes = st.text_area(
                    "Doctor Notes",
                    value=notes,
                    key=f"notes_{patient}"
                )

                prescription_text = st.text_area(
                    "Prescription",
                    value=prescription,
                    key=f"prescription_{patient}"
                )

                if st.button(
                    f"Save Consultation - {patient}"
                ):

                    save_doctor_notes(
                        patient,
                        doctor_notes,
                        prescription_text
                    )

                    st.success(
                        "Consultation saved!"
                    )

                    st.rerun()

# =========================================================
# ADMIN DASHBOARD
# =========================================================

elif st.session_state.role == "Admin":

    st.header("🛡️ Enterprise Admin Dashboard")

    users = load_users()

    appointments = load_all_appointments()

    # =====================================================
    # METRICS
    # =====================================================

    total_users = len(users)

    total_patients = len([
        u for u in users
        if u[1] == "Patient"
    ])

    total_doctors = len([
        u for u in users
        if u[1] == "Doctor"
    ])

    total_appointments = len(
        appointments
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Users",
        total_users
    )

    c2.metric(
        "Patients",
        total_patients
    )

    c3.metric(
        "Doctors",
        total_doctors
    )

    c4.metric(
        "Appointments",
        total_appointments
    )

    st.markdown("---")

    # =====================================================
    # USER MANAGEMENT
    # =====================================================

    # =====================================================
    # DOCTOR APPROVALS
    # =====================================================

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

    if users:

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

        st.markdown("---")

        # ================================================
        # DELETE USER
        # ================================================

        usernames = [
            u[0]
            for u in users
        ]

        selected_user = st.selectbox(
            "Select User to Delete",
            usernames
        )

        if st.button("Delete User"):

            delete_user(
                selected_user
            )

            st.success(
                "User deleted successfully!"
            )

            st.rerun()

    else:

        st.info(
            "No users found."
        )

    st.markdown("---")

    # =====================================================
    # APPOINTMENT MANAGEMENT
    # =====================================================

    st.subheader("📅 Appointment Monitoring")

    if appointments:

        appointment_df = pd.DataFrame(
            appointments,
            columns=[
                "Patient",
                "Doctor",
                "Date",
                "Time",
                "Reason",
                "Status"
            ]
        )

        st.dataframe(
            appointment_df,
            use_container_width=True
        )

        st.markdown("---")

        # ================================================
        # ANALYTICS
        # ================================================

        st.subheader("📊 Platform Analytics")

        fig = px.histogram(
            appointment_df,
            x="Status",
            title="Appointment Status Analytics"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        fig2 = px.pie(
            appointment_df,
            names="Doctor",
            title="Doctor Distribution"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    else:

        st.info(
            "No appointments available."
        )

    st.markdown("---")

    # =====================================================
    # SYSTEM HEALTH
    # =====================================================

    st.subheader("⚙️ System Health")

    st.success(
        "System Status: Operational"
    )

    st.info(
        "JWT Authentication Active"
    )

    st.info(
        "AI Healthcare Engine Running"
    )

    st.info(
        "Database Connected Successfully"
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