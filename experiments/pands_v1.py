import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_csv_agent

# Connect Groq LLM and load env file
load_dotenv()
client=ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"),
                model_name="gpt-4o-mini",
                temperature=0)
verbose=os.getenv("VERBOSE","FALSE")=="True"
print("LLM Connected")
BASE_DIR= os.path.dirname(os.path.abspath(__file__))
CSV_PATH=os.path.join(BASE_DIR, "data", "inventory_data.csv")
df = pd.read_csv(CSV_PATH)
print(f"CSV loaded: {len(df)} rows")

# Create the agent this is LangChain function
agent=create_csv_agent(client,
                       CSV_PATH,
                       verbose=True,
                       allow_dangerous_code=True,
                        handle_parsing_errors=True,
                         max_iterations=10,
                         max_execution_time=180,
                         agent_type="openai-tools",
                       prefix="""You are a Supply Chain analyst. Always answer questions in 
                       plain English. Do not ask to access "code" or "dataframe". Always respond
                       in a structured format."""
                       
                       )

      




