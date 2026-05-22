Q1)What was wrong with my RAG and why?
Ans) My RAG was only answering on unstructured data and not calculated ones, so I used Pandas Agent. I created it by using LangChain function called create_csv_agent.
RAG uses semantic similarity search which cannot perform aggregations, counts, or date comparisons. It finds rows that look similar to the question — not rows that answer it mathematically.

Q2)What is the ReAct pattern?
Ans) Think- Act- Response loop

Q3)Why does the Pandas agent write Python code?
It writes the python code to make calculations, LLM cannot do calculations it can give semantic search output

Q4)What is the difference between a chain and an agent?
chain is like an assembly line, it follows the same steps everytime, no decision making of its own. agent is like a human analyst who chooses the approach based on the question, it thinks and understands the situation, which tool to use, reads the result.

Q5)Why removed verbose from api.py file now?
verbose=os.getenv("VERBOSE","FALSE")=="True" #  Verbose was for CSV Agent to show the thinking step in the terminal. ChatOpenAI doesn't use that parameter 

Order in the file:

1. Imports
2. load_dotenv()
3. app = FastAPI()
4. inventory = Inventory(...)
5. client = ChatOpenAI(...)
6. QueryRequest class
7. QueryResponse class
8. classify_intent function ← before endpoint
9. format_answer function ← before endpoint
10. @app.post("/query") endpoint ← calls both functions

Define the helper functions before the code that uses them. It makes the file's readibility easier.


runs-on: ubuntu-latest
GitHub Actions runs your pipeline on a fresh virtual machine in the cloud. You choose which operating system that machine uses.

Why Linux and not Windows? Because:

Most production servers run Linux
Docker works best on Linux
It is free on GitHub Actions
Faster than Windows

Every time you push code GitHub creates a fresh Ubuntu machine, runs your 4 steps, and destroys it. Clean slate every time.