# 05_RAG_Agent
# This notebook implements a basic RAG Agent that uses Text-to-SQL to query the Gold layer

import os
from databricks import sql
from langchain.llms import OpenAI # Example LLM
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase

# 1. Setup Databricks SQL Connection (The "Data Tool")
SERVER_HOSTNAME = os.getenv('DATABRICKS_SERVER_HOSTNAME')
HTTP_PATH = os.getenv('DATABRICKS_HTTP_PATH')
ACCESS_TOKEN = os.getenv('DATABRICKS_TOKEN')

# Create a SQLAlchemy connection for LangChain
# Format: databricks://token:<token>@<host>?http_path=<path>
conn_string = f"databricks://token:{ACCESS_TOKEN}@{SERVER_HOSTNAME}?http_path={HTTP_PATH}"
db = SQLDatabase.from_uri(conn_string)

# 2. Define the RAG Logic (Text-to-SQL)
# This agent converts natural language -> SQL -> Result -> Natural Language
llm = OpenAI(temperature=0)
chain = create_sql_query_chain(llm, db)

def ask_housing_agent(question):
    print(f"❓ Question: {question}")

    # Step 1: Generate SQL (The 'Retrieval' part of RAG)
    sql_query = chain.invoke({"question": question})
    print(f"🛠️ Generated SQL: {sql_query}")

    # Step 2: Execute SQL on Gold Table
    result = db.run(sql_query)
    print(f"📦 Data Retrieved: {result}")

    # Step 3: Final Answer (The 'Generation' part of RAG)
    # In a full RAG, we'd pass the result back to the LLM for a natural response
    return f"The answer is: {result}"

# 3. Test the Agent
questions = [
    "What is the average housing price in New York?",
    "Which city has the most expensive houses on average?"
]

for q in questions:
    print(ask_housing_agent(q))
    print("-" * 30)
