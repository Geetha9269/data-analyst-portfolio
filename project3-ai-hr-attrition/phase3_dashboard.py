from groq import Groq
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv
from datetime import datetime

# ---- Setup ----
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---- Load Data ----
df = pd.read_csv('data/HR-Em.csv')

print("=" * 50)
print("GENERATING POWER BI STYLE DASHBOARD...")
print("=" * 50)

# ---- Calculate Metrics ----
attrition_rate = round(
    df['Attrition'].value_counts()['Yes'] / len(df) * 100, 2
)
total_left   = df['Attrition'].value_counts()['Yes']
total_stayed = df['Attrition'].value_counts()['No']

avg_income_left = round(
    df[df['Attrition'] == 'Yes']['MonthlyIncome'].mean(), 0
)
avg_income_stayed = round(
    df[df['Attrition'] == 'No']['MonthlyIncome'].mean(), 0
)
income_gap = int(avg_income_stayed - avg_income_left)
retention  = round(100 - attrition_rate, 2)

overtime_attrition = df.groupby('OverTime')['Attrition'].apply(
    lambda x: round((x == 'Yes').sum() / len(x) * 100, 2)
)

dept_attrition = df.groupby('Department')['Attrition'].apply(
    lambda x: round((x == 'Yes').sum() / len(x) * 100, 2)
).reset_index()
dept_attrition.columns = ['Department', 'Attrition_Rate']

top_roles = df.groupby('JobRole')['Attrition'].apply(
    lambda x: round((x == 'Yes').sum() / len(x) * 100, 2)
).sort_values(ascending=False).head(5).reset_index()
top_roles.columns = ['JobRole', 'Attrition_Rate']

age_bins   = [20, 30, 40, 50, 100]
age_labels = ['20-30', '31-40', '41-50', '50+']
df['AgeGroup'] = pd.cut(
    df['Age'], bins=age_bins,
    labels=age_labels, right=False
)
age_attrition = df.groupby(
    'AgeGroup', observed=True
)['Attrition'].apply(
    lambda x: round((x == 'Yes').sum() / len(x) * 100, 2)
).reset_index()
age_attrition.columns = ['AgeGroup', 'Attrition_Rate']

gender_attrition = df.groupby('Gender')['Attrition'].apply(
    lambda x: round((x == 'Yes').sum() / len(x) * 100, 2)
).reset_index()
gender_attrition.columns = ['Gender', 'Attrition_Rate']

print("✅ Metrics calculated")

# ---- Get AI Insights ----
print("🤖 Getting AI insights...")
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "You are a senior HR Data Analyst."
        },
        {
            "role": "user",
            "content": (
                "Based on this HR data provide exactly "
                "4 short insights (max 20 words each):\n"
                f"- Attrition Rate: {attrition_rate}%\n"
                f"- Income Gap: ${income_gap:,}\n"
                f"- Overtime Attrition: "
                f"{overtime_attrition['Yes']}%\n"
                f"- Top Risk Role: "
                f"{top_roles['JobRole'].iloc[0]}\n\n"
                "Format exactly like this:\n"
                "1. [insight]\n"
                "2. [insight]\n"
                "3. [insight]\n"
                "4. [insight]"
            )
        }
    ],
    max_tokens=300
)
ai_insights = response.choices[0].message.content
print("✅ AI insights generated")

# ---- Pre-build HTML Snippets ----

# AI insight cards
insight_items = ""
for line in ai_insights.strip().split('\n'):
    line = line.strip()
    if line:
        insight_items += (
            '<div class="insight-item">'
            + line +
            '</div>\n'
        )

# Department table rows
dept_rows = ""
for _, drow in dept_attrition.iterrows():
    dept = drow['Department']
    rate = drow['Attrition_Rate']
    total = len(df[df['Department'] == dept])
    left  = len(df[
        (df['Department'] == dept) &
        (df['Attrition'] == 'Yes')
    ])
    if rate > 18:
        rc = 'risk-high'
        rl = '🔴 HIGH'
    elif rate > 13:
        rc = 'risk-medium'
        rl = '🟡 MEDIUM'
    else:
        rc = 'risk-low'
        rl = '🟢 LOW'
    width = min(rate * 3, 100)
    dept_rows += (
        "<tr>"
        f"<td>{dept}</td>"
        f"<td>{total}</td>"
        f"<td>{left}</td>"
        f'<td class="{rc}">{rate}%</td>'
        f'<td class="{rc}">{rl}</td>'
        "<td>"
        '<div class="progress-bar">'
        f'<div class="progress-fill" style="width:{width}%">'
        "</div></div></td>"
        "</tr>\n"
    )

# Job role table rows
role_rows = ""
for rank, rrow in enumerate(top_roles.itertuples(), 1):
    role  = rrow.JobRole
    rate  = rrow.Attrition_Rate
    left  = len(df[
        (df['JobRole'] == role) &
        (df['Attrition'] == 'Yes')
    ])
    total = len(df[df['JobRole'] == role])
    if rate > 25:
        rc = 'risk-high'
        rl = '🔴 CRITICAL'
    elif rate > 15:
        rc = 'risk-medium'
        rl = '🟡 HIGH'
    else:
        rc = 'risk-low'
        rl = '🟢 MEDIUM'
    role_rows += (
        "<tr>"
        f"<td>#{rank}</td>"
        f"<td>{role}</td>"
        f"<td>{left}</td>"
        f"<td>{total}</td>"
        f'<td class="{rc}">{rate}%</td>'
        f'<td class="{rc}">{rl}</td>'
        "</tr>\n"
    )

print("✅ Table rows built")

# ---- Generate Charts ----
print("📊 Generating charts...")

# Chart 1 — Department Bar
fig_dept = px.bar(
    dept_attrition,
    x='Department', y='Attrition_Rate',
    color='Attrition_Rate',
    color_continuous_scale=['#00B4D8','#0077B6','#03045E'],
    title='Attrition Rate by Department (%)',
    text='Attrition_Rate'
)
fig_dept.update_traces(
    texttemplate='%{text}%', textposition='outside'
)
fig_dept.update_layout(
    plot_bgcolor='#1e2130', paper_bgcolor='#1e2130',
    font_color='white', title_font_size=16,
    showlegend=False, height=350
)
dept_chart = fig_dept.to_html(
    full_html=False, include_plotlyjs=False
)

# Chart 2 — Top Roles Horizontal Bar
fig_roles = px.bar(
    top_roles,
    x='Attrition_Rate', y='JobRole',
    orientation='h',
    color='Attrition_Rate',
    color_continuous_scale=['#F72585','#B5179E','#7209B7'],
    title='Top 5 High-Risk Job Roles (%)',
    text='Attrition_Rate'
)
fig_roles.update_traces(
    texttemplate='%{text}%', textposition='outside'
)
fig_roles.update_layout(
    plot_bgcolor='#1e2130', paper_bgcolor='#1e2130',
    font_color='white', title_font_size=16,
    showlegend=False, height=350,
    yaxis={'categoryorder': 'total ascending'}
)
roles_chart = fig_roles.to_html(
    full_html=False, include_plotlyjs=False
)

# Chart 3 — Overtime Donut
fig_ot = go.Figure(data=[go.Pie(
    labels=['With Overtime', 'Without Overtime'],
    values=[
        overtime_attrition['Yes'],
        overtime_attrition['No']
    ],
    hole=0.6,
    marker_colors=['#F72585', '#4CC9F0']
)])
fig_ot.update_layout(
    title='Overtime Impact on Attrition (%)',
    plot_bgcolor='#1e2130', paper_bgcolor='#1e2130',
    font_color='white', title_font_size=16, height=350,
    annotations=[dict(
        text=str(overtime_attrition['Yes']) + '%',
        x=0.5, y=0.5, font_size=28,
        font_color='#F72585', showarrow=False
    )]
)
ot_chart = fig_ot.to_html(
    full_html=False, include_plotlyjs=False
)

# Chart 4 — Age Group Bar
fig_age = px.bar(
    age_attrition,
    x='AgeGroup', y='Attrition_Rate',
    color='Attrition_Rate',
    color_continuous_scale=['#06D6A0','#118AB2','#073B4C'],
    title='Attrition Rate by Age Group (%)',
    text='Attrition_Rate'
)
fig_age.update_traces(
    texttemplate='%{text}%', textposition='outside'
)
fig_age.update_layout(
    plot_bgcolor='#1e2130', paper_bgcolor='#1e2130',
    font_color='white', title_font_size=16,
    showlegend=False, height=350
)
age_chart = fig_age.to_html(
    full_html=False, include_plotlyjs=False
)

# Chart 5 — Income Comparison
fig_income = go.Figure(data=[
    go.Bar(
        name='Left',
        x=['Employees Left'],
        y=[avg_income_left],
        marker_color='#F72585',
        text=[f'${int(avg_income_left):,}'],
        textposition='outside'
    ),
    go.Bar(
        name='Stayed',
        x=['Employees Stayed'],
        y=[avg_income_stayed],
        marker_color='#4CC9F0',
        text=[f'${int(avg_income_stayed):,}'],
        textposition='outside'
    )
])
fig_income.update_layout(
    title='Avg Monthly Income: Left vs Stayed ($)',
    plot_bgcolor='#1e2130', paper_bgcolor='#1e2130',
    font_color='white', title_font_size=16,
    showlegend=True, height=350
)
income_chart = fig_income.to_html(
    full_html=False, include_plotlyjs=False
)

# Chart 6 — Gender Pie
fig_gender = px.pie(
    gender_attrition,
    values='Attrition_Rate', names='Gender',
    title='Attrition Rate by Gender (%)',
    color_discrete_sequence=['#4CC9F0', '#F72585'],
    hole=0.5
)
fig_gender.update_layout(
    plot_bgcolor='#1e2130', paper_bgcolor='#1e2130',
    font_color='white', title_font_size=16, height=350
)
gender_chart = fig_gender.to_html(
    full_html=False, include_plotlyjs=False
)

print("✅ All charts generated")

# ---- Build Final HTML ----
print("🎨 Building dashboard...")

report_date  = datetime.now().strftime('%B %d, %Y %H:%M')
report_year  = datetime.now().strftime('%Y')
ot_yes       = str(overtime_attrition['Yes'])
ot_no        = str(overtime_attrition['No'])
total_emp    = f"{len(df):,}"
income_gap_f = f"${income_gap:,}"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HR Attrition Dashboard</title>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
    background-color: #0d1117;
    color: #e6edf3;
    font-family: 'Inter', sans-serif;
}
.header {
    background: linear-gradient(135deg,#1e2130,#161b27);
    border-bottom: 1px solid #30363d;
    padding: 20px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.header-left h1 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: #4CC9F0;
    letter-spacing: 1px;
}
.header-left p {
    color: #8b949e;
    font-size: 12px;
    margin-top: 4px;
}
.header-right {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}
.badge {
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 12px;
    color: #8b949e;
}
.badge span { color: #4CC9F0; font-weight: 600; }
.container {
    padding: 25px 30px;
    max-width: 1600px;
    margin: 0 auto;
}
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5,1fr);
    gap: 16px;
    margin-bottom: 25px;
}
.kpi-card {
    background: linear-gradient(145deg,#1e2130,#161b27);
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 20px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
    cursor: default;
}
.kpi-card:hover {
    transform: translateY(-3px);
    border-color: #4CC9F0;
}
.kpi-card::before {
    content:'';
    position:absolute;
    top:0; left:0; right:0;
    height:3px;
    background: var(--accent);
}
.kpi-card .icon { font-size:24px; margin-bottom:10px; }
.kpi-card .label {
    font-size:11px;
    color:#8b949e;
    text-transform:uppercase;
    letter-spacing:1px;
    margin-bottom:8px;
}
.kpi-card .value {
    font-family:'Rajdhani',sans-serif;
    font-size:32px;
    font-weight:700;
    color: var(--accent);
    line-height:1;
}
.kpi-card .sub {
    font-size:11px;
    color:#8b949e;
    margin-top:6px;
}
.insights-bar {
    background: linear-gradient(135deg,#161b27,#1e2130);
    border: 1px solid #30363d;
    border-left: 4px solid #4CC9F0;
    border-radius: 12px;
    padding: 20px 25px;
    margin-bottom: 25px;
}
.insights-bar h3 {
    font-family:'Rajdhani',sans-serif;
    color:#4CC9F0;
    font-size:14px;
    letter-spacing:2px;
    text-transform:uppercase;
    margin-bottom:12px;
}
.insights-grid {
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:15px;
}
.insight-item {
    background:#21262d;
    border-radius:8px;
    padding:12px 15px;
    font-size:12px;
    color:#c9d1d9;
    line-height:1.5;
    border:1px solid #30363d;
}
.insight-item::before { content:'🤖 '; }
.charts-grid-3 {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:16px;
    margin-bottom:16px;
}
.charts-grid-2 {
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:16px;
    margin-bottom:25px;
}
.chart-card {
    background:linear-gradient(145deg,#1e2130,#161b27);
    border:1px solid #30363d;
    border-radius:12px;
    padding:5px;
    transition:border-color 0.2s;
}
.chart-card:hover { border-color:#4CC9F0; }
.table-section {
    background:linear-gradient(145deg,#1e2130,#161b27);
    border:1px solid #30363d;
    border-radius:12px;
    padding:20px;
    margin-bottom:20px;
}
.table-section h3 {
    font-family:'Rajdhani',sans-serif;
    color:#4CC9F0;
    font-size:16px;
    letter-spacing:1px;
    margin-bottom:15px;
    text-transform:uppercase;
}
table { width:100%; border-collapse:collapse; font-size:13px; }
th {
    background:#21262d;
    color:#8b949e;
    padding:10px 15px;
    text-align:left;
    font-weight:500;
    text-transform:uppercase;
    font-size:11px;
    letter-spacing:1px;
}
td {
    padding:10px 15px;
    border-bottom:1px solid #21262d;
    color:#c9d1d9;
}
tr:hover td { background:#21262d; }
.risk-high   { color:#F72585; font-weight:600; }
.risk-medium { color:#FFB703; font-weight:600; }
.risk-low    { color:#06D6A0; font-weight:600; }
.progress-bar {
    background:#21262d;
    border-radius:10px;
    height:6px; width:100%;
    margin-top:4px;
}
.progress-fill {
    height:6px;
    border-radius:10px;
    background:linear-gradient(90deg,#4CC9F0,#F72585);
}
.footer {
    text-align:center;
    padding:20px;
    color:#8b949e;
    font-size:12px;
    border-top:1px solid #30363d;
    margin-top:10px;
}
.footer span { color:#4CC9F0; }
</style>
</head>
<body>

<div class="header">
  <div class="header-left">
    <h1>⚡ HR ATTRITION INTELLIGENCE DASHBOARD</h1>
    <p>AI-Powered Analytics &bull; Generated: """ + report_date + """ &bull; IBM HR Dataset</p>
  </div>
  <div class="header-right">
    <div class="badge">Dataset: <span>IBM HR Analytics</span></div>
    <div class="badge">Records: <span>""" + total_emp + """</span></div>
    <div class="badge">AI Model: <span>Llama3-70b</span></div>
    <div class="badge">Columns: <span>35</span></div>
  </div>
</div>

<div class="container">

  <div class="kpi-grid">
    <div class="kpi-card" style="--accent:#4CC9F0">
      <div class="icon">👥</div>
      <div class="label">Total Employees</div>
      <div class="value">""" + total_emp + """</div>
      <div class="sub">Across 3 departments</div>
    </div>
    <div class="kpi-card" style="--accent:#F72585">
      <div class="icon">📉</div>
      <div class="label">Attrition Rate</div>
      <div class="value">""" + str(attrition_rate) + """%</div>
      <div class="sub">""" + str(total_left) + """ employees left</div>
    </div>
    <div class="kpi-card" style="--accent:#FFB703">
      <div class="icon">💰</div>
      <div class="label">Income Gap</div>
      <div class="value">""" + income_gap_f + """</div>
      <div class="sub">Left vs Stayed monthly</div>
    </div>
    <div class="kpi-card" style="--accent:#F72585">
      <div class="icon">⏰</div>
      <div class="label">Overtime Attrition</div>
      <div class="value">""" + ot_yes + """%</div>
      <div class="sub">vs """ + ot_no + """% no overtime</div>
    </div>
    <div class="kpi-card" style="--accent:#06D6A0">
      <div class="icon">✅</div>
      <div class="label">Retention Rate</div>
      <div class="value">""" + str(retention) + """%</div>
      <div class="sub">""" + str(total_stayed) + """ employees retained</div>
    </div>
  </div>

  <div class="insights-bar">
    <h3>🤖 AI Generated Insights &mdash; Llama3-70b</h3>
    <div class="insights-grid">
      """ + insight_items + """
    </div>
  </div>

  <div class="charts-grid-3">
    <div class="chart-card">""" + dept_chart + """</div>
    <div class="chart-card">""" + roles_chart + """</div>
    <div class="chart-card">""" + ot_chart + """</div>
  </div>

  <div class="charts-grid-2">
    <div class="chart-card">""" + age_chart + """</div>
    <div class="chart-card">""" + income_chart + """</div>
  </div>

  <div class="table-section">
    <h3>📊 Department Risk Summary</h3>
    <table>
      <thead>
        <tr>
          <th>Department</th>
          <th>Total Employees</th>
          <th>Employees Left</th>
          <th>Attrition Rate</th>
          <th>Risk Level</th>
          <th>Visual</th>
        </tr>
      </thead>
      <tbody>
        """ + dept_rows + """
      </tbody>
    </table>
  </div>

  <div class="table-section">
    <h3>⚠️ High Risk Job Roles</h3>
    <table>
      <thead>
        <tr>
          <th>Rank</th>
          <th>Job Role</th>
          <th>Employees Left</th>
          <th>Total in Role</th>
          <th>Attrition Rate</th>
          <th>Risk</th>
        </tr>
      </thead>
      <tbody>
        """ + role_rows + """
      </tbody>
    </table>
  </div>

</div>

<div class="footer">
  Generated by <span>AI Automation Pipeline</span> &bull;
  Python + Groq API (Llama3-70b) + Plotly &bull;
  <span>Geetha Reddy Samreddy</span> &bull;
  """ + report_year + """
</div>

</body>
</html>"""

with open('HR_Attrition_Dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Dashboard saved: HR_Attrition_Dashboard.html")
print("\n" + "=" * 50)
print("🎉 DASHBOARD COMPLETE!")
print("=" * 50)
print("➡ Open HR_Attrition_Dashboard.html in Chrome")
print("➡ It looks exactly like Power BI!")