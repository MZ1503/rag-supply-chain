import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from analytics import Inventory
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load inventory data on startup, clean up on shutdown."""
    global inventory
    try:
        inventory = Inventory("data/inventory_data.csv")
        logger.info("Inventory loaded successfully")
    except FileNotFoundError:
        logger.error("Data file not found: data/inventory_data.csv")
        raise
    yield
    logger.info("Application shutting down")

    app = FastAPI(
    title="Supply Chain AI Assistant",
    description="Natural language inventory analytics for logistics managers",
    version="1.0.0",
    lifespan=lifespan
    )

    client = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",
    temperature=0

    class QueryRequest(BaseModel):
    question: str

    class QueryResponse(BaseModel):
    answer: str

def classify_intent(question: str) -> str:
    """
    Classifies user question into a predefined metric key.

    Args:
        question: Natural language question from user

    Returns:
        One of the 10 predefined metric keys

    Raises:
        Exception: If OpenAI API call fails
    """
    prompt = f"""You are a supply chain analytics assistant.

Given this question: "{question}"

Reply with ONLY one metric name from this list, nothing else:
expired_count, expiring_7_days, top_expired_brand,
top_revenue_brand, total_inv_val, highest_stock_category,
products_zero_stock, expiry_rate_brand, urgent_brands, top_10_products"""

    response = client.invoke(prompt)
    return response.content.strip()

    def format_answer(metric_key: str, metrics: dict) -> str:
    """
    Formats a pre-calculated metric into a human readable answer.

    Args:
        metric_key: One of the 10 predefined metric keys
        metrics: Dictionary of pre-calculated inventory metrics

    Returns:
        Human readable answer string
    """
    answers = {
        "expired_count": f"There are {metrics['expired_count']} expired products.",
        "expiring_7_days": f"{len(metrics['expiring_7_days'])} products are expiring in the next 7 days.",
        "top_expired_brand": f"The brand with most expired products is {metrics['top_expired_brand']}.",
        "top_revenue_brand": f"The top revenue brand is {metrics['top_revenue_brand']}.",
        "total_inv_val": f"The total inventory value is {metrics['total_inv_val']}.",
        "highest_stock_category": f"The {metrics['highest_stock_category']} category has the highest stock.",
        "products_zero_stock": f"There are {len(metrics['products_zero_stock'])} products with zero stock.",
        "expiry_rate_brand": f"Expiry rates by brand: {metrics['expiry_rate_brand']}.",
        "urgent_brands": f"Brands needing urgent attention: {', '.join(metrics['urgent_brands'])}.",
        "top_10_products": ", ".join([
            f"{p['BRAND']} ({p['CATEGORY']}): AED {p['REVENUE']:,.0f}"
            for p in metrics['top_10_products']
        ])
    }

    return answers.get(metric_key, "I didn't quite understand that. Could you rephrase?")


    @app.get("/health")
def health() -> dict:
    """Health check endpoint for load balancers and monitoring."""
    return {"status": "healthy"}


@app.post("/query")
def query(request: QueryRequest) -> QueryResponse:
    """
    Main query endpoint. Accepts natural language question,
    returns pre-calculated inventory metric as answer.

    Args:
        request: QueryRequest with question field

    Returns:
        QueryResponse with answer field

    Raises:
        HTTPException 400: If question is empty
        HTTPException 500: If internal processing fails
    """
    try:
        # Edge case 1 — empty question
        if not request.question.strip():
            raise ValueError("Question cannot be empty")

        logger.info(f"Query received: {request.question}")

        metric_key = classify_intent(request.question)
        logger.info(f"Intent classified as: {metric_key}")

        answer = format_answer(metric_key, inventory.metrics)
        return QueryResponse(answer=answer)

    except ValueError as e:
        # Edge case 2 — bad input from user
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Edge case 3 — anything unexpected
        logger.error(f"Query endpoint failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong")
