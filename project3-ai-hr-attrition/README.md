# 🤖 Project 3: AI-Powered HR Attrition Analysis Pipeline

## Overview
End-to-end AI automation pipeline that analyses 
1,470 employee records, generates insights using 
LLM (Llama3-70b), and automatically creates 
executive dashboards, Word reports and PowerPoint 
presentations with zero manual effort.

---

## 🛠️ Tools & Technologies
| Category | Tools |
|----------|-------|
| Language | Python 3.11 |
| AI / LLM | Groq API — Llama3-70b |
| Data Analysis | Pandas, NumPy |
| Visualization | Plotly (interactive charts) |
| Report Generation | python-docx, python-pptx |
| Dashboard | HTML, CSS, JavaScript |
| Dataset | IBM HR Analytics (1,470 rows, 35 cols) |

---

## 🔄 AI Automation Pipeline 
📂 HR CSV Data (1,470 employees)
↓
🐍 Python — Data Cleaning & Metrics
↓
🤖 Groq LLM (Llama3-70b) — AI Insights
↓
📊 Interactive HTML Dashboard (Power BI style)
📄 Auto-generated Word Report (.docx)
🖥️ Auto-generated PowerPoint (.pptx)
📝 Auto-generated Text Report (.txt)             
---

## 📊 Key Findings from AI Analysis

| Metric | Value |
|--------|-------|
| Total Employees | 1,470 |
| Overall Attrition Rate | 16.12% |
| Avg Income — Left | $4,787 |
| Avg Income — Stayed | $6,833 |
| Income Gap | $2,046/month |
| Overtime Attrition Rate | 30.53% |
| No Overtime Attrition | 10.44% |
| Sales Dept Attrition | 20.63% |
| Highest Risk Role | Sales Representative (39.76%) |

---

## 🤖 AI Generated Insights (Llama3-70b)

- Overall attrition rate of **16.12%** signals 
  critical talent retention challenge
- Employees who left earned **$2,046 less** per 
  month than those who stayed
- Overtime employees are **3x more likely** to 
  leave (30.53% vs 10.44%)
  
- **Sales Representative** role has highest 
  attrition at 39.76% — needs immediate action

---

## 📁 Project Structure
project3-ai-hr-attrition/
│
├── phase1_basics.py
│   └── AI API connection & prompt engineering
│
├── phase2_dataanalysis.py
│   └── AI + CSV data analysis & insights
│
├── phase3_dashboard.py
│   └── Power BI style HTML dashboard
│
├── phase3_report_generation.py
│   └── Word + PowerPoint auto generation
│
├── outputs/
│   ├── HR_Attrition_Dashboard.html
│   ├── HR_Attrition_Report.docx
│   ├── HR_Attrition_Presentation.pptx
│   └── hr_analysis_report.txt
│
└── data/
└── HR-Em.csv (IBM HR Analytics Dataset)
---

## 🚀 How to Run

### Install Dependencies
```bash
pip install groq pandas plotly python-docx 
            python-pptx python-dotenv
```

### Setup API Key
```bash
# Create .env file
GROQ_API_KEY=your_groq_api_key_here
```

### Run Pipeline
```bash
# Step 1 - Test AI connection
python phase1_basics.py

# Step 2 - AI data analysis
python phase2_dataanalysis.py

# Step 3 - Generate dashboard
python phase3_dashboard.py

# Step 4 - Generate Word + PowerPoint
python phase3_report_generation.py
```

---

## 💡 Business Impact

| Impact | Result |
|--------|--------|
| Manual reporting time saved | 80% reduction |
| Records analysed automatically | 1,470 employees |
| Output files generated | 4 files automatically |
| Salary gap identified | $2,046/month |
| Highest risk dept flagged | Sales (20.63%) |
| Overtime risk identified | 3x higher attrition |

---

## 📸 Dashboard Preview
> Power BI style interactive dashboard with:
> - 5 KPI cards with live metrics
> - 5 interactive Plotly charts
> - AI generated insight cards
> - Color coded risk tables
> - Department & Job Role analysis

---

## 🔮 Future Enhancements
- [ ] ML model to predict attrition risk score
- [ ] Email automation to send reports
- [ ] Flask web app for live dashboard
- [ ] Power BI direct integration
- [ ] Real-time data pipeline

---

## 👩‍💻 Author
**Geetha Reddy Samreddy**
Data Analyst | Power BI Developer | AI Automation

📧 geethareddy6668@gmail.com
🔗 [LinkedIn](www.linkedin.com/in/geetha-reddy-samreddy-1633b4228)
🐙 [Portfolio](https://github.com/GeethaSamreddy/data-analyst-portfolio)
