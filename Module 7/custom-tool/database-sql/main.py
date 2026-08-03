import ollama
import pyodbc
import json
from decimal import Decimal

MODEL = "llama3.1"

DB_CONFIG = {
    "server": "I20102",     
    "database": "my_database",
    "username": "sa",
    "password": "123",
    "driver": "{ODBC Driver 18 for SQL Server}",
}

def get_connection():
    conn_str = (
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']};"
        f"TrustServerCertificate=yes;" 
    )
    return pyodbc.connect(conn_str)



def search_orders(customer_email: str = None, limit: int = 10):
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = 10
    limit = min(limit, 20)

    conn = get_connection()
    cur = conn.cursor()

    if customer_email:
        cur.execute(
            f"SELECT TOP {limit} id, customer_email, total, created_at "
            f"FROM orders WHERE customer_email = ?",
            (customer_email,),
        )
    else:
        cur.execute(f"SELECT TOP {limit} id, customer_email, total, created_at FROM orders")

    columns = [col[0] for col in cur.description]
    rows = []
    for row in cur.fetchall():
        record = dict(zip(columns, row))
        for key, value in record.items():
            if isinstance(value, Decimal):
                record[key] = float(value)
        rows.append(record)

    conn.close()
    return rows


tools = [
    {
        "type": "function",
        "function": {
            "name": "search_orders",
            "description": "Search orders in the SQL Server database, optionally filtered by customer email. Read-only.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_email": {
                        "type": "string",
                        "description": "Filter by customer email (optional)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max rows to return (default 10, max 20)",
                    },
                },
                "required": [],
            },
        },
    }
]

available_functions = {"search_orders": search_orders}

# --- 4. Run the conversation ---
messages = [{"role": "user", "content": "What orders has senthild@test.com placed?"}]

response = ollama.chat(model=MODEL, messages=messages, tools=tools)
msg = response["message"]
messages.append(msg)

if msg.get("tool_calls"):
    for call in msg["tool_calls"]:
        func_name = call["function"]["name"]
        args = call["function"]["arguments"]
        result = available_functions[func_name](**args)
        messages.append({"role": "tool", "content": json.dumps(result)})

    final = ollama.chat(model=MODEL, messages=messages)
    print(final["message"]["content"])
else:
    print(msg["content"])