import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

st.title("🏭 MZ Supply Chain Q&A")
st.write("Ask questions about inventory, expiry, and brand performance!")

@st.cache_resource
def load_rag():
    loader = CSVLoader("../al-seer-data-pipeline/data/my_actual_alseer_portfolio.csv")
    documents = loader.load()
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 50})
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile"
    )
    prompt = ChatPromptTemplate.from_template("""
    Use the supply chain data to answer:
    Context: {context}
    Question: {question}
    Answer:
    """)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

chain = load_rag()

question = st.text_input("Ask a question about your supply chain data:")

if question:
    with st.spinner("Analyzing..."):
        answer = chain.invoke(question)
        st.write("**Answer:**", answer)