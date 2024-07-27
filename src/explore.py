import streamlit as st
from dotenv import load_dotenv
from pandasai.llm.openai import OpenAI
from pandasai import SmartDataframe


load_dotenv()

def explore(project_name):
    if "messages" not in st.session_state.keys():
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "context": "Feel free to inquire the Uploaded Data",
                }
            ]
            
            st.session_state.query_engine = None
    if prompt := st.chat_input("Your question?"):
        st.session_state.messages.append({"role": "user", "context": prompt})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["context"])
            
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                llm = OpenAI()
                prompt += "Use Month Nnames in final output response"
                df = SmartDataframe(f'../project/{project_name}/data/train_dataset.csv  ', config={"llm":llm, "conversational":True})
                response = df.chat(prompt)
                st.image(response)
                st.session_state.messages.append(
                    {"role": "assistant", "context": response}
                )
    
