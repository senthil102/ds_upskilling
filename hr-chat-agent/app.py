import streamlit as st

from auth import authenticate_employee
from agent import run_hr_agent


st.set_page_config(
    page_title="HR Chat Agent",
    page_icon="👨‍💼",
    layout="wide"
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "employee" not in st.session_state:
    st.session_state.employee = None

if "employee_id" not in st.session_state:
    st.session_state.employee_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# Login
# --------------------------------------------------

if not st.session_state.authenticated:

    st.title("👨‍💼 HR Chat Agent")
    st.caption("AI-powered HR assistant")

    st.subheader("Employee Login")

    employee_id = st.text_input(
        "Employee ID",
        placeholder="Example: EMP1001"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        employee = authenticate_employee(
            employee_id,
            password
        )

        if employee:

            st.session_state.authenticated = True
            st.session_state.employee = employee
            st.session_state.employee_id = employee_id

            # Start a fresh conversation after login
            st.session_state.messages = []

            st.rerun()

        else:

            st.error(
                "Invalid Employee ID or password."
            )

    st.stop()


# --------------------------------------------------
# Authenticated Employee
# --------------------------------------------------

employee = st.session_state.employee
employee_id = st.session_state.employee_id


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("👨‍💼 HR Assistant")

    st.write(
        f"**Employee:** {employee['name']}"
    )

    st.write(
        f"**Employee ID:** {employee_id}"
    )

    st.write(
        f"**Department:** {employee['department']}"
    )

    st.divider()

    if st.button("Logout"):

        st.session_state.authenticated = False
        st.session_state.employee = None
        st.session_state.employee_id = None
        st.session_state.messages = []

        st.rerun()


# --------------------------------------------------
# Main Chat
# --------------------------------------------------

st.title("👨‍💼 HR Chat Agent")

st.caption(
    "Ask questions about HR policies, leave and employee information."
)


# --------------------------------------------------
# Display Previous Messages
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

user_question = st.chat_input(
    "Ask your HR question..."
)


# --------------------------------------------------
# Process Question
# --------------------------------------------------

if user_question:

    # Save current user question
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    # Display user question
    with st.chat_message("user"):

        st.write(user_question)

    # Previous conversation
    # Remove current question because it is
    # already passed separately.
    chat_history = st.session_state.messages[:-1]

    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 HR Agent is thinking..."
        ):

            answer = run_hr_agent(
                question=user_question,
                employee_id=employee_id,
                chat_history=chat_history
            )

        st.write(answer)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )