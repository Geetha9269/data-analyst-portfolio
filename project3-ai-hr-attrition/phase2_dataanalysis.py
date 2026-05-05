from groq import Groq
import pandas as pd
import os
from dotenv import load_dotenv

# ---- Setup ----
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---- Load Your HR Dataset ----
df = pd.read_csv('data/HR-Em.csv')

print("=" * 50)
print("DATASET OVERVIEW")
print("=" * 50)
print(f"Total Employees  : {len(df)}")
print(f"Total Columns    : {len(df.columns)}")
print(f"Attrition - Yes  : {df['Attrition'].value_counts()['Yes']}")
print(f"Attrition - No   : {df['Attrition'].value_counts()['No']}")
print(f"Departments      : {df['Department'].unique()}")

# ---- Prepare Data Summary for AI ----
attrition_rate = round(
    df['Attrition'].value_counts()['Yes'] / len(df) * 100, 2
)

dept_attrition = df.groupby('Department')['Attrition'].apply(
    lambda x: round((x == 'Yes').sum() / len(x) * 100, 2)
).to_string()

avg_age_left    = round(df[df['Attrition'] == 'Yes']['Age'].mean(), 1)
avg_age_stayed  = round(df[df['Attrition'] == 'No']['Age'].mean(), 1)

avg_income_left   = round(
    df[df['Attrition'] == 'Yes']['MonthlyIncome'].mean(), 0
)
avg_income_stayed = round(
    df[df['Attrition'] == 'No']['MonthlyIncome'].mean(), 0
)

overtime_attrition = df.groupby('OverTime')['Attrition'].apply(
    lambda x: round((x == 'Yes').sum() / len(x) * 100, 2)
).to_string()

job_role_attrition = df.groupby('JobRole')['Attrition'].apply(
    lambda x: round((x == 'Yes').sum() / len(x) * 100, 2)
).sort_values(ascending=False).head(5).to_string()

# ---- Send to AI for Insights ----
print("\n" + "=" * 50)
print("AI ANALYSIS - ATTRITION INSIGHTS")
print("=" * 50)

response1 = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": """You are a senior HR Data Analyst. 
            Analyze HR data and give specific, 
            actionable insights."""
        },
        {
            "role": "user",
            "content": f"""
            Analyze this HR Attrition data and give insights:

            COMPANY OVERVIEW:
            - Total Employees: {len(df)}
            - Overall Attrition Rate: {attrition_rate}%

            ATTRITION BY DEPARTMENT:
            {dept_attrition}

            AGE ANALYSIS:
            - Average age of employees who LEFT: {avg_age_left}
            - Average age of employees who STAYED: {avg_age_stayed}

            INCOME ANALYSIS:
            - Average monthly income who LEFT: ${avg_income_left}
            - Average monthly income who STAYED: ${avg_income_stayed}

            OVERTIME IMPACT:
            {overtime_attrition}

            TOP 5 JOB ROLES WITH HIGHEST ATTRITION:
            {job_role_attrition}

            Please provide:
            1. Top 3 key findings from this data
            2. Root causes of attrition
            3. 3 specific recommendations for HR team
            4. Which department needs immediate attention
            
            Be specific with numbers from the data.
            """
        }
    ],
    max_tokens=1000
)
print(response1.choices[0].message.content)

# ---- AI generates SQL queries ----
print("\n" + "=" * 50)
print("AI GENERATED SQL QUERIES")
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
            I have an HR table called 'employees' with columns:
            Age, Attrition, Department, MonthlyIncome,
            JobRole, OverTime, YearsAtCompany,
            JobSatisfaction, WorkLifeBalance, Gender

            Write SQL queries to find:
            1. Attrition rate by department
            2. Average salary of employees who left vs stayed
            3. Overtime impact on attrition
            4. Top 5 job roles with highest attrition
            5. Attrition by age group (20-30, 31-40, 41-50, 50+)
            """
        }
    ],
    max_tokens=1000
)
print(response2.choices[0].message.content)

# ---- Save Report to File ----
print("\n" + "=" * 50)
print("SAVING REPORT...")
print("=" * 50)

with open('hr_analysis_report.txt', 'w') as f:
    f.write("HR ATTRITION ANALYSIS REPORT\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Total Employees: {len(df)}\n")
    f.write(f"Attrition Rate: {attrition_rate}%\n\n")
    f.write("AI INSIGHTS:\n")
    f.write(response1.choices[0].message.content)
    f.write("\n\nSQL QUERIES:\n")
    f.write(response2.choices[0].message.content)

print("✅ Report saved as hr_analysis_report.txt")
print("✅ Phase 2 Complete!")