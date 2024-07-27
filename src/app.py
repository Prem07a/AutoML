import streamlit as st
from streamlit_option_menu import option_menu
import os
from explore import explore
import pandas as pd
from automl import generate
from transform import run_transform
import json

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
    df = pd.read_csv(file,encoding='latin1')
    df.to_csv(path)
        

def handle_new_project():
    """Handle the creation of a new project."""
    st.session_state.project_name = st.text_input("Project Name").strip()
    st.session_state.disable = st.session_state.project_name == ""

    train_file = st.file_uploader("Upload your training dataset", type=["csv"], disabled=st.session_state.disable)
    test_file = st.file_uploader("Upload your testing dataset", type=["csv"], disabled=st.session_state.disable)

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
    project.remove(".gitkeep")
    project_name = st.selectbox("Project", project)
    if st.button("Open", disabled= True if project == ["None"] else False):
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
        project_path = f"../project/{st.session_state.project_name}"

        def list_directories(base_dir):
            directories = []
            for root, dirs, files in os.walk(base_dir):
                for dir_name in dirs:
                    directories.append(os.path.relpath(os.path.join(root, dir_name), base_dir))
                break  
            return directories

        def list_files_in_directory(directory):
            file_list = {}
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_file_path = os.path.relpath(file_path, directory)
                    file_list[relative_file_path] = file_path
            return file_list

        directories = list_directories(project_path)

        if directories:
            selected_directory = st.selectbox("Select a folder", directories)
            selected_directory_path = os.path.join(project_path, selected_directory)

            all_files = list_files_in_directory(selected_directory_path)

            if all_files:
                if "models" in selected_directory_path.lower():
                    st.markdown("### Models in the 'models' folder:")
                    for model_file in all_files.keys():
                        st.text(model_file)
                else:
                    selected_files = st.multiselect("Select files to view", list(all_files.keys()))

                    if selected_files:
                        for selected_file in selected_files:
                            file_path = all_files[selected_file]
                            st.markdown(f"### Contents of `{selected_file}`")
                            
                            if selected_file.endswith(".py"):
                                with open(file_path, "r") as f:
                                    code_content = f.read()
                                st.code(code_content, language="python")
                            
                            elif selected_file.endswith(".csv"):
                                df = pd.read_csv(file_path)
                                st.dataframe(df)
                            
                            elif selected_file.endswith(".json"):
                                with open(file_path, "r") as f:
                                    json_content = json.load(f)
                                st.json(json_content)
                            
                            elif selected_file.endswith(".png"):
                                st.image(file_path)
                            
                            elif selected_file.endswith(".joblib"):
                                st.text(f"Model file: {selected_file}")
                    else:
                        st.info("Select files to display their contents.")
            else:
                st.warning("No files found in the selected directory.")
        else:
            st.warning("No directories found in the project.")
        
    elif choice == "Explore Data":
        explore(project_name=st.session_state.project_name)
        
    elif choice == "Transform Data":
        path = f"../project/{st.session_state.project_name}/data/train_dataset.csv"
        temp = f"../project/{st.session_state.project_name}/data/temp.csv"
        df = pd.read_csv(path)
        st.dataframe(df)
        
        if prompt:=st.chat_input("Transform Your Data"):
            msg = {"role": "user", "context": prompt}
            with st.chat_message(msg["role"]):
                st.write(msg["context"])
            run_transform(prompt, path)
            df = pd.read_csv(temp)
            msg = {
                "role": "assistant"
            }
            with st.chat_message(msg["role"]):
                st.dataframe(df)
            
        if st.button("Save changes"):
            df = pd.read_csv(temp)
            df.to_csv(path, index=False)
            st.rerun()
            
        
    else: 
        data_path = f"../project/{st.session_state.project_name}/data/train_dataset.csv"
        df = pd.read_csv(data_path)
        target = st.selectbox("Select Target Columns",list(df.columns))
        if st.button("Start"):
            generate(data_path, target=target)
            st.markdown("### Output")
            st.image(f"../project/{st.session_state.project_name}/report/performance.png")
            with open(f"../project/{st.session_state.project_name}/report/performance.json", "r") as f:
                json_body = json.load(f)
            st.json(json_body)
