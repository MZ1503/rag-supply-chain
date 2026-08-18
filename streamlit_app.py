import streamlit as st
import requests


st.title("🏭 MZ Supply Chain AI Assistant")

# Ask questions
question=st.text_input("Ask questions about inventory data:")

if question:
    with st.spinner("Analyzing..."):
       response=requests.post(
           "http://localhost:8000/query",
            json={"question": question}
       )
       result = response.json()
       st.success(result["answer"])

