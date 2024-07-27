from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI
import os
import subprocess
from automl import load_data
import streamlit as st


def Transform(prompt, path):
    behavior = """
    You are an AI assistant for generating Python code for Data science:
    1. Generate accurate and efficient code based on user prompts.
    2. Handle errors and exceptions by retrying with error messages if necessary.
    3. Ensure the code performs the specified task correctly.
    4. Write python code
    """
    data_description, _ = load_data(path)
    save_path = '/'.join(path.split('/')[:-1])
    messages = [
        ChatMessage(role="system", content=behavior),
        ChatMessage(
            role="user", content=f"Prompt: {prompt},Data Path: {path} Data Description: {data_description}, Save Modified data to : {save_path}/temp.csv"
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
    
def run_transform(prompt, path):
    max_retries = 5
    retry_count = 0
    error_message = None

    while retry_count < max_retries:
        if error_message is None:
            _, error_message = Transform(prompt, path)
        else:
            prompt_with_error = f"{prompt}\nError Message:\n{error_message}"
            error_message = None
            _, error_message = Transform(prompt_with_error, path)
            
        if error_message is None:
            with open("./MLcode.py", "r") as f:
                code = f.read()
            st.code(code)
            break
        
        retry_count += 1