import streamlit as st
import pandas as pd
from llama_index.llms.openai import OpenAI
import os
from dotenv import load_dotenv
from io import StringIO
from llama_index.core.llms import ChatMessage
import subprocess
from prompt import data_cleaning_prompt, feature_selection_prompt, model_training_prompt

load_dotenv()

def load_data(path):
    df = pd.read_csv(path)
    description = StringIO()
    df.info(buf=description)
    data_description = description.getvalue()
    columns_str = ", ".join(df.columns.tolist())
    return data_description, columns_str


def Query(user_input, prompt, context=""):
    behavior = """
    You are an AI assistant for generating Python code for machine learning tasks. You are expected to:
    1. Generate accurate and efficient code based on user prompts.
    2. Handle errors and exceptions by retrying with error messages if necessary.
    3. Ensure the code performs the specified task correctly.
    4. Write python code
    """
    messages = [
        ChatMessage(role="system", content=behavior),
        ChatMessage(
            role="user", content=f"{prompt}\nContext:\n{context}\nTask:\n{user_input}"
        ),
    ]
    llm = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = llm.chat(messages=messages)

    response_text = str(response).split("```python")[1].split("```")[0]
    with open("MLcode.py", "w") as f:
        f.write(response_text)
    command = "python MLcode.py"

    try:
        output = subprocess.run(command, shell=True, check=True, capture_output=True)
        ans = (output.stdout).decode("utf-8")
        return ans, None
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode("utf-8")
        return None, error_message


def run_step(prompt, data_description, columns_str, path, target=""):
    max_retries = 5
    retry_count = 0
    error_message = None

    while retry_count < max_retries:
        query = f"""
        Perform the following step with the provided data context:
        Import all libraries you are using
        Data Description: {data_description}
        Columns: {columns_str}
        Data Path: {path}
        Save Path for Modified Data: {path}
        Target Column: {target}
        Always write entire python code
        """
        if error_message is None:
            _, error_message = Query(query, prompt)
        else:
            query_with_error = f"{query}\nError Message:\n{error_message}"
            error_message = None
            _, error_message = Query(query_with_error, prompt)
            
        if error_message is None:
            with open("./MLcode.py", "r") as f:
                code = f.read()
            st.code(code)
            break
        
        retry_count += 1

def write_code(filename, path):
    with open('./MLcode.py', "r") as f:
        code = f.read()
    path = '/'.join(path.split("/")[:-2]) + f"/code/{filename}.py"
    with open(path, "w") as f:
        f.write(code)

def generate(path, target, classification=True):
    st.title("Automated ML Model Training")

    data_description, columns_str = load_data(path)

    with st.status("Data Cleaning", expanded=True, state="running"):
        run_step(
            prompt=data_cleaning_prompt,
            data_description=data_description,
            columns_str=columns_str,
            path=path,
            target=target,
        )
        st.success("Completed Data Cleaning")
    write_code("data_cleaning", path)
    with st.status("Feature Selection", expanded=True, state="running"):
        run_step(
            prompt=feature_selection_prompt,
            data_description=data_description,
            columns_str=columns_str,
            path=path,
            target=target,
        )
        st.success("Completed Feature Selection")
    write_code("feature_selection", path)
    with st.status("Model Training", expanded=True, state="running"):
        type = "Classification" if classification else "Regression"

        if type:
            models = [
                "Logistic Regression",
                "K-Nearest Neighbors Classification",
                "Support Vector Machine (SVM)",
                "Decision Tree Classification",
                "Random Forest Classification",
                "Gradient Boosting Classification",
                "AdaBoost Classification",
            ]
        else:
            models = [
                "Linear Regression",
                "Polynomial Regression",
                "Support Vector Regression (SVR)",
                "Decision Tree Regression",
                "Random Forest Regression",
                "Gradient Boosting Regression",
                "AdaBoost Regression",
                "K-Nearest Neighbors Regression (KNN)",
            ]
        model_folder = '/'.join(path.split("/")[:-2]) + "/models"
        report_folder = '/'.join(path.split("/")[:-2]) + "/report"
        run_step(
            prompt=model_training_prompt + f"You have to use all {type} models List of models {models}" + f"save_model to folder {model_folder}" + f"save parameters and plot to report folder path : {report_folder}",
            data_description=data_description,
            columns_str=columns_str,
            path=path,
            target=target,
        )
        st.success("Completed Model training")
        write_code("ml_training", path)


