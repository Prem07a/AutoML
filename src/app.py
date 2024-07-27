import streamlit as st
from streamlit_option_menu import option_menu
import os
# from explore import explore

st.set_page_config(page_title="AutoML", page_icon="../images/favicon.ico")


if "disable" not in st.session_state:
    st.session_state.disable = True

if "start" not in st.session_state:
    st.session_state.start = False

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "project_name" not in st.session_state:
    st.session_state.project_name = ""

if "choice_type" not in st.session_state:
    st.session_state.choice_type = ""

if "files_ready" not in st.session_state:
    st.session_state.files_ready = False

def create_project_folders(base_path):
    """Create project folders if they don't exist."""
    folders = [f"{base_path}/data", f"{base_path}/report", f"{base_path}/code", f"{base_path}/models"]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

def save_uploaded_file(file, path):
    """Save uploaded file to the specified path."""
    if file is not None:
        with open(path, "wb") as f:
            f.write(file.getbuffer())

def handle_new_project():
    """Handle the creation of a new project."""
    st.session_state.project_name = st.text_input("Project Name").strip()
    st.session_state.disable = st.session_state.project_name == ""

    train_file = st.file_uploader("Upload your training dataset", type=["csv", "xlsx"], disabled=st.session_state.disable)
    test_file = st.file_uploader("Upload your testing dataset", type=["csv", "xlsx"], disabled=st.session_state.disable)

    st.session_state.files_ready = train_file is not None and test_file is not None

    if st.button("CREATE", disabled=st.session_state.disable or not st.session_state.files_ready):
        base_path = f"../project/{st.session_state.project_name}"
        if os.path.exists(base_path):
            st.warning("A project with this name already exists.")
        else:
            create_project_folders(base_path)
            save_uploaded_file(train_file, os.path.join(base_path, 'data', 'train_dataset.csv'))
            save_uploaded_file(test_file, os.path.join(base_path, 'data', 'test_dataset.csv'))
            st.success(f"Project '{st.session_state.project_name}' created successfully.")
            st.session_state.uploaded = True
            st.session_state.start = True
            st.rerun()

def handle_previous_project():
    """Handle opening a previous project."""
    project = os.listdir("../project")
    project_name = st.selectbox("Project", project)
    if st.button("Open"):
        st.session_state.project_name = project_name
        st.session_state.start = True
        st.rerun()

with st.sidebar:
    if not st.session_state.start:
        st.session_state.choice_type = option_menu(None, options=["New Project", "Previous Project"], icons=["1-square", "2-square"])

    if not st.session_state.uploaded and st.session_state.choice_type == "New Project":
        handle_new_project()
    elif st.session_state.choice_type == "Previous Project" and not st.session_state.project_name:
        handle_previous_project()

    if st.session_state.start:
        st.image("../images/logo.png")
        choice = option_menu(
            menu_title=None,
            options=["Auto Pilot", "Explore Data", "Transform Data", "Open Project"],
            icons=["code-slash", "clipboard-data", "file-earmark-arrow-up", "folder"]
        )

        
        if st.button("Close Project"):
            st.session_state.project_name = ""
            st.session_state.start = False
            st.session_state.uploaded = False
            st.rerun()

if not st.session_state.start:
    with st.container():
        col1, col2, col3 = st.columns([0.07, 1, 0.05])
        with col2:
            st.image("../images/logo.png")

else:
    if choice == "Open Project":
        
            st.markdown("""        
                        ```python
                        print("Hello World")
                        ```
                        """)
    elif choice == "Explore Data":
        # explore(project_name=st.session_state.project_name)
        st.chat_input("Explore Your Data")
        
    elif choice == "Transform Data":
        st.chat_input("Transform Your Data")
    else: 
        msg = "Starting Data Preprocessing"
        if st.button("Start"):
            with st.status(msg, expanded=False, state="running"):
                st.success(f"Created ML model")