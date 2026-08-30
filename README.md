
# MZ Supply Chain Q&A
Natural language inventory analytics platform enables logistics managers to query 10,000+ SKU inventory data in English for instant and accurate answers about expired products, inventory value , brands that needs attention, etc.

# Live Links
AWS EC2: http://3.67.3.254:8000/docs

# Why I built this tool?
I spent around 4 years in logistics and supply chain and in one of the previous companies as a Supply Chain Analyst, I handled around 1000+ SKU's demand and supply. I had to manually check the inventory data in Excel. Create expiry and inventory analysis reports. This tool is based out of that frustation of doing manual job especially being an Engineer and in the world of AI. 

# Architecture Decision
Initially when I started building this tool, I chose RAG, LangChain, ChromaDB and GroqLLM. I faced significant issues in data retrieval. The 10000 rows was too much for GroqLLaMA-3 as I was using free tier, therefore the LLM was only able to capture 50 rows which was not giving the desired output. Secondly, RAG is meant for semantic similarity search and it wasn't the right tool for calculation based searches. Therefore I refactored from RAG to Pandas Agent where I wrote python code in pandas for calculations such as total expired products, top 10 products with stock value, highest revenue brand and many more. No more hallucinated answers. 
The Agentic pattern used in this project is intent classification with routing where the LLM(GPT-4o-mini) classifies the user's question into predefined metrics,then routes to the precalculated answers. This decision taught me to choose the right retrieval strategy - RAG for unstructured documents and Pandas for structured tabular data.
 
# The Working
- Streamlit sends request to FastAPI backend
- Redis cache checked first — instant response if cached
- If not cached, GPT-4o-mini classifies the intent
- Pre-calculated metrics are looked up
- Response cached and returned

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
- FastAPI — REST API backend
- PostgreSQL — persistent data storage
- Redis — response caching layer
- SQLAlchemy — ORM
- Alembic — database migrations
- LangChain — intent classification routing
- OpenAI GPT-4o-mini — natural language understanding
- Pandas — pre-calculated analytics engine
- Docker — containerization
- GitHub Actions — CI/CD pipeline
- Deployed on AWS EC2 with Amazon ECR
- Streamlit — interactive frontend

## Architecture
analytics.py          — Pandas class, 10 pre-calculated metrics
api.py                — FastAPI with intent classifier and routing
app.py                — Streamlit frontend
Dockerfile            — containerized application
docker-compose.yml    — local development setup
.github/workflows/    — automated CI/CD pipeline
experiments/          — earlier approaches tried and abandoned
tests/                — automated test suite
app/database.py       — PostgreSQL connection (SQLAlchemy)
app/models.py         — Database schema (Product, Query, User)
app/cache.py          — Redis caching functions
migrations/           — Alembic migration files

## How To Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/MZ1503/supply-chain-ai-assistant
cd supply-chain-ai-assistant
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Add your OpenAI API key to .env
```

### 5. Add your data
```bash
# Add your inventory CSV to data/inventory_data.csv
# See data/sample_inventory.csv for required column structure
```

### 6. Run the API
```bash
uvicorn api:app --reload
```

### 7. Run the frontend
```bash
streamlit run app.py
```

## Data
Inventory data is synthetic, generated to represent a realistic 
supply chain structure based on my logistics experience. 
Does not represent real company data.

Required CSV columns: BRAND, CATEGORY, ACTUAL_QTY, 
UNIT_PRICE_AED, DAYS_TO_EXPIRY

## What I Learned
- RAG is the wrong tool for structured tabular data
- Pre-calculating metrics gives reliable, exact, fast answers
- Separating intent classification from data retrieval
- Docker + CI/CD makes deployment repeatable and automatic
- Importance of choosing the right tool for the data type

## Experiments
See `experiments/pandas_agent_v1.py` for the earlier Pandas Agent 
approach that was abandoned due to context window limitations 
with 10,000+ rows.

Enterprise Upgrade Sprints

### Sprint 1 — Bug Fixes
- Fixed KeyError from dead deployment URL
- Migrated to live AWS EC2 endpoint

### Sprint 2 — Database Layer
- Migrated from CSV to PostgreSQL
- Designed normalized schema (Product, Query, User)
- Implemented Alembic migrations

### Sprint 3 — Caching Layer
- Implemented Redis caching
- Reduced response time from ~2s to under 100ms
- Debugged production Docker/disk space issue on AWS EC2

### Sprint 4 — Authentication (In Progress)
- JWT authentication
- Rate limiting