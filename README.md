#Supply Chain RAG Q&A System (Need to Fine-Tune)

## What it does
Natural language Q&A system on 10,000 rows of FMCG supply chain data.

Ask questions like:
- "Which brand has most expired products?"
- "What is the total revenue by category?"
- "Which products are expiring soon?"

## Tech Stack
- Python
- LangChain
- Groq LLM (Llama 3)
- ChromaDB
- HuggingFace Embeddings
- Streamlit

## Architecture

CSV Data → CSVLoader → HuggingFace Embeddings → ChromaDB
                                                     ↓
User Question → Retriever → Prompt → Groq LLM → Answer


## How to run
pip install -r requirements.txt
streamlit run app.py

