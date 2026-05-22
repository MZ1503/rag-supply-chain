
# MZ Supply Chain Q&A
Natural language inventory analytics platform enables logistics managers to query 10,000+ SKU inventory data in English for instant and accurate answers about expired products, inventory value , brands that needs attention, etc.

# Live Links
Streamlit Demo: https://huggingface.co/spaces/MZ1503/supply-chain-ai-assistant
AWS EC2: http://3.123.36.250:8000/docs

# Why I built this tool?
I spent around 4 years in logistics and supply chain and in one of the previous companies as a Supply Chain Analyst, I handled around 1000+ SKU's demand and supply. I had to manually check the inventory data in Excel. Create expiry and inventory analysis reports. This tool is based out of that frustation of doing manual job especially being an Engineer and in the world of AI. 

# Architecture Decision
Initially when I started building this tool, I chose RAG, LangChain, ChromaDB and GroqLLM. I faced significant issues in data retrieval. The 10000 rows was too much for GroqLLaMA-3 as I was using free tier, therefore the LLM was only able to capture 50 rows which was not giving the desired output. Secondly, RAG is meant for semantic similarity search and it wasn't the right tool for calculation based searches. Therefore I refactored from RAG to Pandas Agent where I wrote python code in pandas for calculations such as total expired products, top 10 products with stock value, highest revenue brand and many more. No more hallucinated answers. 
The Agentic pattern used in this project is intent classification with routing where the LLM(GPT-4o-mini) classifies the user's question into predefined metrics,then routes to the precalculated answers. This decision taught me to choose the right retrieval strategy - RAG for unstructured documents and Pandas for structured tabular data.
 
# The Working
- User enters a question in plain English
- Streamlit sends to Fast API on Railway
- GPT-4o-mini classifies the intent
- Pre-calculated metrics are looked up
- Clean answer returned

# Questions this AI assistant can answer
     
#1. How many products are expired?
#2. Which products are expiring in the next 7 days?
#3. Which brand has the most expired products?
#4. Which brand has the highest revenue?
#5. What is the total inventory value?
#6. Which category has the most stock?
#7. Which products have zero stock?
#8. What is the expiry rate by brand?
#9. Which brands need urgent attention?
#10. Show me the top 10 products by stock value?


# Tech Stack
- FastAPI — backend
- LangChain — intent classification routing
- OpenAI GPT-4o-mini — natural language understanding
- Pandas — pre-calculated analytics engine
- Docker — containerization
- GitHub Actions — CI/CD pipeline
- Railway — production deployment
- Deployed on AWS EC2 with Amazon ECR
- Streamlit — interactive frontend

## Architecture
analytics.py — Pandas class, 10 pre-calculated metrics
api.py — FastAPI with intent classifier
app.py — Streamlit frontend calling Railway API
Dockerfile — containerized application
.github/workflows/ci.yml — automated testing and deployment

## How To Run Locally
1. Clone the repo
2. pip install -r requirements.txt
3. Add API keys to .env (see .env.example)
4. uvicorn api:app --reload
5. streamlit run app.py

## What I Learned
- RAG is the wrong tool for structured tabular data.
- Pre-calculating metrics gives reliable, fast, exact answers.
- Separating intent classification from data retrieval.
- Docker + CI/CD makes deployment repeatable and automatic.

## Note
Inventory data is synthetic, generated to represent a realistic supply chain structure based on my logistics experience. Does not represent real company data.
