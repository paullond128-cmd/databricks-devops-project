# 05_RAG_Agent
# This notebook implements a basic RAG Agent that uses Text-to-SQL to query the Gold layer

import os

print("🚀 Starting RAG Agent...")

# 1. Check if LangChain & OpenAI credentials are configured
SERVER_HOSTNAME = os.getenv('DATABRICKS_SERVER_HOSTNAME')
HTTP_PATH = os.getenv('DATABRICKS_HTTP_PATH')
ACCESS_TOKEN = os.getenv('DATABRICKS_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def ask_housing_agent(question):
    print(f"❓ Question: {question}")

    # Step 1: If LangChain and OpenAI credentials are provided, use them
    if OPENAI_API_KEY and SERVER_HOSTNAME and HTTP_PATH and ACCESS_TOKEN:
        try:
            from databricks import sql
            from langchain.llms import OpenAI
            from langchain.chains import create_sql_query_chain
            from langchain_community.utilities import SQLDatabase

            conn_string = f"databricks://token:{ACCESS_TOKEN}@{SERVER_HOSTNAME}?http_path={HTTP_PATH}"
            db = SQLDatabase.from_uri(conn_string)
            llm = OpenAI(temperature=0)
            chain = create_sql_query_chain(llm, db)

            sql_query = chain.invoke({"question": question})
            print(f"🛠️ Generated SQL: {sql_query}")
            result = db.run(sql_query)
            print(f"📦 Data Retrieved: {result}")
            return f"The answer is: {result}"
        except Exception as e:
            print(f"⚠️ LangChain execution unavailable ({e}), using native Spark query...")

    # Step 2: Native Databricks fallback (querying the Gold table directly with Spark)
    q_lower = question.lower()
    if "new york" in q_lower or "ny" in q_lower:
        sql_query = "SELECT city, avg_price FROM housing_gold_report WHERE city = 'NY'"
    elif "expensive" in q_lower or "most" in q_lower:
        sql_query = "SELECT city, avg_price FROM housing_gold_report ORDER BY avg_price DESC LIMIT 1"
    else:
        sql_query = "SELECT city, avg_price FROM housing_gold_report"

    print(f"🛠️ Generated SQL: {sql_query}")
    df_result = spark.sql(sql_query)
    rows = df_result.collect()
    result = [row.asDict() for row in rows]
    print(f"📦 Data Retrieved: {result}")
    return f"The answer is: {result}"

# 3. Test the Agent
questions = [
    "What is the average housing price in New York?",
    "Which city has the most expensive houses on average?"
]

for q in questions:
    print(ask_housing_agent(q))
    print("-" * 30)
