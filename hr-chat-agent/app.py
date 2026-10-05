import streamlit as st

from auth import authenticate_employee
from agent import run_hr_agent

from document_manager import (
    DOCUMENTS_DIR,
    save_document_metadata,
    get_documents,
    delete_document
)

from ui import (
    COMPANY_NAME,
    inject_css,
    login_brand,
    sidebar_logo,
    profile_card,
    chat_topbar,
    welcome_hero,
    page_header,
    stat_card,
)


# Page Configuration

st.set_page_config(
    page_title=f"{COMPANY_NAME} | HR Chat Agent",
    page_icon="💬",
    layout="wide"
)


# Starter questions shown on an empty chat (edit freely)
SUGGESTED_QUESTIONS = [
    "How many leave days do I have left?",
    "What is the company leave policy?",
    "What is the work from home policy?",
    "Show my employee details.",
]


# Session State

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "employee" not in st.session_state:
    st.session_state.employee = None

if "employee_id" not in st.session_state:
    st.session_state.employee_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# Login
if not st.session_state.authenticated:

    inject_css()

    st.write("")
    st.write("")

    _, center, _ = st.columns([1, 1.1, 1])

    with center:

        with st.container(border=True):

            st.markdown(
                login_brand(),
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="login-title">Welcome back 👋</div>'
                '<div class="login-sub">Sign in to your employee '
                'account to chat with the HR assistant.</div>',
                unsafe_allow_html=True
            )

            # st.form lets the user press Enter to submit
            with st.form("login_form", border=False):

                employee_id_input = st.text_input(
                    "Employee ID",
                    placeholder="Example: I20102"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password"
                )

                submitted = st.form_submit_button(
                    "Sign in",
                    use_container_width=True
                )

            if submitted:

                employee = authenticate_employee(
                    employee_id_input,
                    password
                )

                if employee:

                    st.session_state.authenticated = True
                    st.session_state.employee = employee
                    st.session_state.employee_id = employee_id_input
                    st.session_state.messages = []
                    st.session_state.pending_question = None

                    st.rerun()

                else:

                    st.error(
                        "Invalid Employee ID or password."
                    )

        st.markdown(
            f'<div class="login-foot">© {COMPANY_NAME} · '
            'Secure employee access</div>',
            unsafe_allow_html=True
        )

    st.stop()


 # Authenticated Employee

inject_css()

employee = st.session_state.employee

employee_id = st.session_state.employee_id

role = employee["role"]

first_name = str(employee["name"]).split()[0]


# Sidebar (brand, profile, menu, actions)

with st.sidebar:

    st.markdown(
        sidebar_logo(),
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown(
        profile_card(
            employee["name"],
            employee_id,
            employee["department"],
            role
        ),
        unsafe_allow_html=True
    )

    st.write("")

    # Navigation (HR / ADMIN only)
    if role in ["HR", "ADMIN"]:

        st.markdown(
            '<div class="menu-label">MENU</div>',
            unsafe_allow_html=True
        )

        selected_page = st.radio(
            "Navigation",
            [
                "HR Chat",
                "Document Management"
            ],
            label_visibility="collapsed"
        )

    else:

        selected_page = "HR Chat"

    st.divider()

    if st.button(
        "New chat",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.pending_question = None

        st.rerun()

    if st.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.authenticated = False
        st.session_state.employee = None
        st.session_state.employee_id = None
        st.session_state.messages = []
        st.session_state.pending_question = None

        st.rerun()


 # HR CHAT

if selected_page == "HR Chat":

    st.markdown(
        chat_topbar(),
        unsafe_allow_html=True
    )

    # The question comes from the chat box or a clicked suggestion card
    user_question = st.chat_input(
        "Ask your HR question..."
    )

    if not user_question and st.session_state.pending_question:

        user_question = st.session_state.pending_question

        st.session_state.pending_question = None


    # Empty state: welcome + suggested questions

    if not st.session_state.messages and not user_question:

        st.markdown(
            welcome_hero(first_name),
            unsafe_allow_html=True
        )

        try:
            suggestions_box = st.container(key="suggestions")
        except TypeError:
            # Older Streamlit without container keys
            suggestions_box = st.container()

        with suggestions_box:

            columns = st.columns(2)

            for index, suggestion in enumerate(SUGGESTED_QUESTIONS):

                with columns[index % 2]:

                    if st.button(
                        suggestion,
                        key=f"suggestion_{index}",
                        use_container_width=True
                    ):

                        st.session_state.pending_question = suggestion

                        st.rerun()


    # Previous messages

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )


   # Process question

    if user_question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        with st.chat_message("user"):

            st.write(
                user_question
            )

        chat_history = (
            st.session_state.messages[:-1]
        )

        with st.chat_message("assistant"):

            with st.spinner(
                "HR Agent is thinking..."
            ):

                answer = run_hr_agent(
                    question=user_question,
                    employee_id=employee_id,
                    chat_history=chat_history
                )

            st.write(
                answer
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


# DOCUMENT MANAGEMENT

elif selected_page == "Document Management":

    page_header(
        "HR Document Management",
        "Upload and manage HR policy documents used by the RAG system."
    )

    documents = get_documents()

  
    # ---------------- Upload ----------------

    st.subheader("Upload HR Policy Document")

    upload_col1, upload_col2 = st.columns([4, 1])

    with upload_col1:

        uploaded_file = st.file_uploader(
            "Choose a document",
            type=["pdf", "docx", "txt"],
            label_visibility="collapsed"
        )

    with upload_col2:

        upload_button = st.button(
            "Upload",
            use_container_width=True
        )

    if upload_button:

        if uploaded_file is None:

            st.warning(
                "Please select a document first."
            )

        else:

            file_path = (
                DOCUMENTS_DIR
                / uploaded_file.name
            )

            existing_documents = get_documents()

            duplicate = any(
                document[1] == uploaded_file.name
                for document in existing_documents
            )

            if duplicate:

                st.warning(
                    "This document already exists."
                )

            else:

                with open(file_path, "wb") as file:

                    file.write(
                        uploaded_file.getbuffer()
                    )

                save_document_metadata(
                    file_name=uploaded_file.name,
                    file_path=str(file_path),
                    uploaded_by=employee_id
                )

                st.success(
                    "Document uploaded successfully."
                )

                st.rerun()

    st.divider()

    # ---------------- Document Table ----------------

    st.subheader("Uploaded Documents")

    if not documents:

        st.info(
            "No HR documents available."
        )

    else:

        widths = [3, 1.5, 2, 1, 1]

        h1, h2, h3, h4, h5 = st.columns(widths)

        h1.markdown("**File Name**")
        h2.markdown("**Uploaded By**")
        h3.markdown("**Uploaded Date**")
        h4.markdown("**Status**")
        h5.markdown("**Action**")

        st.divider()

        for document in documents:

            document_id = document[0]
            file_name = document[1]
            uploaded_by = document[2]
            uploaded_at = document[3]
            status = document[4]

            col1, col2, col3, col4, col5 = st.columns(widths)

            with col1:
                st.write(f"📄 {file_name}")

            with col2:
                st.write(uploaded_by)

            with col3:
                st.write(uploaded_at)

            with col4:
                if status == "ACTIVE":
                    st.success("ACTIVE")
                else:
                    st.warning(status)

            with col5:

                if st.button(
                    "Delete",
                    key=f"delete_{document_id}",
                    help=f"Delete {file_name}"
                ):

                    deleted = delete_document(
                        document_id
                    )

                    if deleted:

                        st.success("Document deleted.")
                        st.rerun()

                    else:

                        st.error("Unable to delete document.")