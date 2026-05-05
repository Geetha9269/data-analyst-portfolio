from groq import Groq
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Create Groq client
client = Groq(api_key=api_key)

# ---- Test 1: Simple Question ----
print("=" * 50)
print("TEST 1: Simple Question")
print("=" * 50)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful data analyst"
        },
        {
            "role": "user",
            "content": "What are top 5 KPIs for sales analysis?"
        }
    ],
    max_tokens=500
)

print(response.choices[0].message.content)
# ---- Test 2: SQL Generation ----
print("\n" + "=" * 50)
print("TEST 2: SQL Generation")
print("=" * 50)

response2 = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": """You are a SQL expert. 
            Return only SQL code with comments."""
        },
        {
            "role": "user",
            "content": """
            I have a table called 'sales' with columns:
            date, region, product, revenue, units, cost
            
            Write SQL queries to find:
            1. Total revenue by region
            2. Top 3 products by profit margin
            3. Monthly revenue trend
            """
        }
    ],
    max_tokens=800
)
print(response2.choices[0].message.content)

# ---- Test 3: Power BI DAX ----
print("\n" + "=" * 50)
print("TEST 3: DAX Measures")
print("=" * 50)

response3 = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": """You are a Power BI DAX expert.
            Return only DAX code with comments."""
        },
        {
            "role": "user",
            "content": """
            Table: Sales
            Columns: Date, Region, Product, 
                     Revenue, Units, Cost
            
            Generate DAX measures for:
            1. Total Revenue
            2. Profit Margin %
            3. Month over Month Growth %
            """
        }
    ],
    max_tokens=800
)
print(response3.choices[0].message.content)

# ---- Test 4: Data Analyst Insight ----
print("\n" + "=" * 50)
print("TEST 4: AI Insight Generation")
print("=" * 50)

response4 = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "You are a senior data analyst"
        },
        {
            "role": "user",
            "content": """
            Our sales data shows:
            - Revenue dropped 20% in Q3
            - North region performing 40% below target
            - Product A has 60% return rate
            - Sales cycle increased from 20 to 45 days
            
            Give me:
            1. Top 3 root causes
            2. Immediate actions to take
            3. KPIs to monitor going forward
            
            Be specific and concise.
            """
        }
    ],
    max_tokens=800
)
print(response4.choices[0].message.content)