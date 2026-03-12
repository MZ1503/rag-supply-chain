import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load API Key
load_dotenv()

# Step 1 — Load CSV
loader = CSVLoader("../al-seer-data-pipeline/data/my_actual_alseer_portfolio.csv")
documents = loader.load()
print(f"Step 1 Done — Loaded {len(documents)} rows")

# Step 2 — Create embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("Step 2 Done — Embeddings ready")

# Step 3 — Store in ChromaDB
vectorstore = Chroma.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 50})
print("Step 3 Done — ChromaDB ready")

# Step 4 — Connect Groq LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)
print("Step 4 Done — LLM connected")

# Step 5 — RAG Chain
prompt = ChatPromptTemplate.from_template("""
Use the following supply chain data to answer the question.
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

# Ask question
question = "Which brand has the most expired products?"
answer = chain.invoke(question)
print(f"\nQ: {question}")
print(f"A: {answer}")