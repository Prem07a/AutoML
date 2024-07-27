import streamlit as st
from dotenv import load_dotenv
from pandasai.llm.openai import OpenAI
from pandasai import Agent
import pandas as pd


load_dotenv()

def explore(project_name):
    if "messages" not in st.session_state.keys():
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "context": "Feel free to inquire the Uploaded Data",
                }
            ]
            
    if prompt := st.chat_input("Explore your Data"):
        st.session_state.messages.append({"role": "user", "context": prompt})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["context"].split('.')[-1] == 'png':
                    st.image(message["context"])
            else:
                st.write(message["context"])

            
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                llm = OpenAI()
                prompt += "Use Month Nnames in final output response"
                df = pd.read_csv(f'../project/{project_name}/data/train_dataset.csv')
                agent = Agent(df, config={"verbose": True, "llm": llm, "save_charts": True, "enable_cache": True, "open_charts": False})
                prompt += "If user is asking for plot dont forget to save plot"
                response = agent.chat(prompt)
                if response.split('.')[-1] == 'png':
                    st.image(response)
                else:
                    st.write(response)
                st.session_state.messages.append(
                    {"role": "assistant", "context": response}
                )
    
