
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from datetime import datetime, timedelta
import base64
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(
    page_title="Research Cohort Management System",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'data_source' not in st.session_state:
    st.session_state.data_source = "Mock Data"
if 'uploaded_file_name' not in st.session_state:
    st.session_state.uploaded_file_name = ""

# Custom CSS
st.markdown("""
    <style>
    .student-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 5px solid #4CAF50;
        transition: transform 0.2s;
    }
    .student-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .student-name {
        font-size: 18px;
        font-weight: 600;
        color: #1a1a1a;
    }
    .student-id {
        font-size: 14px;
        color: #666;
        background: #f0f0f0;
        padding: 4px 12px;
        border-radius: 20px;
    }
    .card-details {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-top: 10px;
    }
    .detail-item {
        display: flex;
        flex-direction: column;
    }
    .detail-label {
        font-size: 11px;
        text-transform: uppercase;
        color: #888;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .detail-value {
        font-size: 16px;
        font-weight: 500;
        color: #333;
        margin-top: 2px;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
    }
    .status-fully-funded {
        background: #e8f5e9;
        color: #2e7d32;
    }
    .status-pending {
        background: #fff3e0;
        color: #e65100;
    }
    .status-missing {
        background: #ffebee;
        color: #c62828;
    }
    .risk-low {
        background: #e8f5e9;
        color: #2e7d32;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
    }
    .risk-medium {
        background: #fff3e0;
        color: #e65100;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
    }
    .risk-high {
        background: #ffebee;
        color: #c62828;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
    }
    .gpa-circle {
        display: inline-block;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        text-align: center;
        line-height: 40px;
        font-weight: 700;
        font-size: 16px;
        color: white;
    }
    .gpa-high {
        background: #4CAF50;
    }
    .gpa-medium {
        background: #FFA726;
    }
    .gpa-low {
        background: #EF5350;
    }
    .progress-bar {
        width: 100%;
        height: 8px;
        background: #e0e0e0;
        border-radius: 4px;
        overflow: hidden;
        margin-top: 4px;
    }
    .progress-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s;
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 16px;
        margin: 20px 0;
    }
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .stat-number {
        font-size: 28px;
        font-weight: 700;
        color: #1a1a1a;
    }
    .stat-label {
        font-size: 13px;
        color: #666;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .alert-box {
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 0;
        border-left: 4px solid;
    }
    .alert-danger {
        background: #ffebee;
        border-color: #c62828;
        color: #c62828;
    }
    .alert-warning {
        background: #fff3e0;
        border-color: #e65100;
        color: #e65100;
    }
    .alert-info {
        background: #e3f2fd;
        border-color: #0d47a1;
        color: #0d47a1;
    }
    .deadline-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin: 10px 0;
    }
    .deadline-card {
        background: white;
        padding: 16px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Generate mock dataset
def generate_mock_data():
    np.random.seed(42)
    student_ids = [f"STU{i:03d}" for i in range(1, 31)]
    names = [
        "Emma Wilson", "Liam Chen", "Sophia Patel", "Noah Rodriguez", "Olivia Kim",
        "Mason Davis", "Ava Thompson", "Ethan Martinez", "Isabella Garcia", "Lucas Brown",
        "Mia Johnson", "Alexander Lee", "Charlotte White", "James Anderson", "Amelia Taylor",
        "Benjamin Moore", "Harper Jackson", "Elijah Martin", "Abigail Thompson", "William Garcia",
        "Evelyn Martinez", "James Robinson", "Ella Clark", "Oliver Lewis", "Grace Walker",
        "Daniel Hall", "Chloe Allen", "Matthew Young", "Victoria King", "Joseph Wright"
    ]
    departments = np.random.choice(["Ag", "Forestry", "Bio"], size=30, p=[0.3, 0.3, 0.4])
    gpas = np.round(np.random.uniform(2.5, 4.0, size=30), 2)
    funding_statuses = np.random.choice(
        ["Fully Funded", "Missing Report", "Pending"],
        size=30,
        p=[0.5, 0.2, 0.3]
    )
    
    # Add new fields
    funding_end_dates = []
    for _ in range(30):
        days = np.random.randint(1, 365)
        funding_end_dates.append((datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d'))
    
    milestones = []
    for _ in range(30):
        proposal = np.random.choice([True, False], p=[0.7, 0.3])
        lit_review = np.random.choice([True, False], p=[0.6, 0.4])
        midterm = np.random.choice([True, False], p=[0.4, 0.6])
        defense = np.random.choice([True, False], p=[0.2, 0.8])
        milestones.append({
            'Proposal Submitted': proposal,
            'Literature Review Complete': lit_review,
            'Midterm Review Complete': midterm,
            'Final Defense Complete': defense
        })
    
    data = {
        "Student ID": student_ids,
        "Name": names,
        "Department": departments,
        "GPA": gpas,
        "Funding Status": funding_statuses,
        "Funding End Date": funding_end_dates,
        "Proposal Submitted": [m['Proposal Submitted'] for m in milestones],
        "Literature Review Complete": [m['Literature Review Complete'] for m in milestones],
        "Midterm Review Complete": [m['Midterm Review Complete'] for m in milestones],
        "Final Defense Complete": [m['Final Defense Complete'] for m in milestones]
    }
    return pd.DataFrame(data)

# Load data from file
def load_data(uploaded_file, file_type):
    try:
        if file_type == "CSV":
            df = pd.read_csv(uploaded_file)
        elif file_type == "Excel":
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        else:
            return None
        
        required_cols = ["Student ID", "Name", "Department", "GPA", "Funding Status"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
            st.info("📋 Required columns: Student ID, Name, Department, GPA, Funding Status")
            return None
        
        # Add missing optional columns with defaults
        if "Funding End Date" not in df.columns:
            df["Funding End Date"] = (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')
        
        milestone_cols = ['Proposal Submitted', 'Literature Review Complete', 'Midterm Review Complete', 'Final Defense Complete']
        for col in milestone_cols:
            if col not in df.columns:
                df[col] = np.random.choice([True, False], size=len(df), p=[0.5, 0.5])
        
        return df
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        return None

# Calculate risk score
def calculate_risk_score(row):
    risk_score = 0
    
    # GPA factor
    if row['GPA'] < 3.0:
        risk_score += 3
    elif row['GPA'] < 3.5:
        risk_score += 1
    
    # Funding status factor
    if row['Funding Status'] == 'Missing Report':
        risk_score += 3
    elif row['Funding Status'] == 'Pending':
        risk_score += 2
    
    # Milestone progress factor
    milestones = ['Proposal Submitted', 'Literature Review Complete', 'Midterm Review Complete', 'Final Defense Complete']
    completed = sum([1 for m in milestones if row.get(m, False)])
    if completed <= 1:
        risk_score += 2
    elif completed == 2:
        risk_score += 1
    
    # Funding expiry factor
    try:
        end_date = pd.to_datetime(row['Funding End Date'])
        days_remaining = (end_date - datetime.now()).days
        if days_remaining < 30:
            risk_score += 3
        elif days_remaining < 90:
            risk_score += 1
    except:
        pass
    
    # Classify risk
    if risk_score >= 7:
        return 'High Risk'
    elif risk_score >= 4:
        return 'Medium Risk'
    else:
        return 'Low Risk'

# Calculate days remaining
def calculate_days_remaining(end_date_str):
    try:
        end_date = pd.to_datetime(end_date_str)
        days = (end_date - datetime.now()).days
        return days
    except:
        return None

# Get funding status alert
def get_funding_alert(days_remaining):
    if days_remaining is None:
        return None, None
    if days_remaining < 0:
        return 'Expired', 'danger'
    elif days_remaining < 30:
        return 'Expiring Soon (30 days)', 'danger'
    elif days_remaining < 60:
        return 'Expiring Soon (60 days)', 'warning'
    elif days_remaining < 90:
        return 'Expiring Soon (90 days)', 'info'
    else:
        return 'Active', None

# Calculate milestone completion
def calculate_completion(row):
    milestones = ['Proposal Submitted', 'Literature Review Complete', 'Midterm Review Complete', 'Final Defense Complete']
    completed = sum([1 for m in milestones if row.get(m, False)])
    return (completed / len(milestones)) * 100

# Initialize with mock data
if st.session_state.df is None:
    st.session_state.df = generate_mock_data()
    st.session_state.data_source = "Mock Data"

# Sidebar - Data Source
st.sidebar.title("📁 Data Source")

data_option = st.sidebar.radio(
    "Choose Data Source",
    ["📊 Mock Data", "📤 Upload CSV", "📤 Upload Excel"],
    index=0 if st.session_state.data_source == "Mock Data" else 1
)

if data_option == "📊 Mock Data":
    if st.session_state.data_source != "Mock Data":
        st.session_state.df = generate_mock_data()
        st.session_state.data_source = "Mock Data"
        st.session_state.uploaded_file_name = ""
        st.rerun()

elif data_option == "📤 Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Drop your CSV file here", type=['csv'], key="csv_upload")
    if uploaded_file is not None:
        st.session_state.uploaded_file_name = uploaded_file.name
        df = load_data(uploaded_file, "CSV")
        if df is not None:
            st.session_state.df = df
            st.session_state.data_source = "CSV"
            st.sidebar.success(f"✅ Loaded {len(df)} students from {uploaded_file.name}")
    elif st.session_state.data_source == "Mock Data":
        st.sidebar.info("📤 Upload a CSV file to get started")
    else:
        st.sidebar.warning("⚠️ Please upload a CSV file")

elif data_option == "📤 Upload Excel":
    uploaded_file = st.sidebar.file_uploader("Drop your Excel file here", type=['xlsx', 'xls'], key="excel_upload")
    if uploaded_file is not None:
        st.session_state.uploaded_file_name = uploaded_file.name
        df = load_data(uploaded_file, "Excel")
        if df is not None:
            st.session_state.df = df
            st.session_state.data_source = "Excel"
            st.sidebar.success(f"✅ Loaded {len(df)} students from {uploaded_file.name}")
    elif st.session_state.data_source == "Mock Data":
        st.sidebar.info("📤 Upload an Excel file to get started")
    else:
        st.sidebar.warning("⚠️ Please upload an Excel file")

df = st.session_state.df

# Calculate risk scores and days remaining
df['Risk Score'] = df.apply(calculate_risk_score, axis=1)
df['Days Remaining'] = df['Funding End Date'].apply(calculate_days_remaining)
df['Completion %'] = df.apply(calculate_completion, axis=1)

# Sidebar - Filters
st.sidebar.markdown("---")
st.sidebar.title("🔍 Filters")

# Search bar
search_query = st.sidebar.text_input("🔎 Search by Name or ID", placeholder="Type to search...")

sort_order = st.sidebar.radio("Sort by Name", options=["A-Z", "Z-A"], index=0)

all_depts = sorted(df["Department"].unique().tolist())
selected_depts = st.sidebar.multiselect("Department", options=all_depts, default=all_depts)

gpa_min_val = float(df["GPA"].min())
gpa_max_val = float(df["GPA"].max())
gpa_min, gpa_max = st.sidebar.slider("GPA Range", min_value=gpa_min_val, max_value=gpa_max_val, value=(gpa_min_val, gpa_max_val), step=0.1)

# Risk filter
risk_filter = st.sidebar.multiselect("Risk Level", options=['Low Risk', 'Medium Risk', 'High Risk'], default=['Low Risk', 'Medium Risk', 'High Risk'])

# Apply filters
filtered_df = df[
    (df["Department"].isin(selected_depts)) &
    (df["GPA"] >= gpa_min) &
    (df["GPA"] <= gpa_max) &
    (df["Risk Score"].isin(risk_filter))
].copy()

# Apply search
if search_query:
    filtered_df = filtered_df[
        filtered_df["Name"].str.contains(search_query, case=False, na=False) |
        filtered_df["Student ID"].str.contains(search_query, case=False, na=False)
    ]

# Apply sorting
if sort_order == "A-Z":
    filtered_df = filtered_df.sort_values("Name", ascending=True)
else:
    filtered_df = filtered_df.sort_values("Name", ascending=False)

# Main Dashboard
st.title("🎓 Research Cohort Management System")

# Data source indicator
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    if st.session_state.data_source in ["CSV", "Excel"]:
        st.info(f"📂 Data Source: **{st.session_state.uploaded_file_name}** ({len(df)} records)")
    else:
        st.info(f"📊 Data Source: **{st.session_state.data_source}** ({len(df)} records)")

with col3:
    if st.button("🔄 Reset to Mock Data", use_container_width=True):
        st.session_state.df = generate_mock_data()
        st.session_state.data_source = "Mock Data"
        st.session_state.uploaded_file_name = ""
        st.rerun()

st.markdown("---")

# Stats Grid
total = len(filtered_df)
fully_funded = len(filtered_df[filtered_df["Funding Status"] == "Fully Funded"])
pending = len(filtered_df[filtered_df["Funding Status"] == "Pending"])
missing = len(filtered_df[filtered_df["Funding Status"] == "Missing Report"])
low_risk = len(filtered_df[filtered_df["Risk Score"] == "Low Risk"])
medium_risk = len(filtered_df[filtered_df["Risk Score"] == "Medium Risk"])
high_risk = len(filtered_df[filtered_df["Risk Score"] == "High Risk"])

st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">{total}</div>
            <div class="stat-label">👥 Total Students</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{fully_funded}</div>
            <div class="stat-label">✅ Fully Funded</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{pending}</div>
            <div class="stat-label">⏳ Pending</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{missing}</div>
            <div class="stat-label">⚠️ Missing Report</div>
        </div>
        <div class="stat-card" style="border-top: 3px solid {'#4CAF50' if low_risk > max(medium_risk, high_risk) else '#FFA726' if medium_risk > high_risk else '#EF5350'}">
            <div class="stat-number" style="color: {'#4CAF50' if low_risk > max(medium_risk, high_risk) else '#FFA726' if medium_risk > high_risk else '#EF5350'}">
                {low_risk} / {medium_risk} / {high_risk}
            </div>
            <div class="stat-label">🟢 Risk: Low / Medium / High</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Alerts Section
st.subheader("🚨 Alerts & Deadlines")

# Funding expiry alerts
expiring_30 = filtered_df[filtered_df['Days Remaining'].between(0, 30)]
expiring_60 = filtered_df[filtered_df['Days Remaining'].between(31, 60)]
expiring_90 = filtered_df[filtered_df['Days Remaining'].between(61, 90)]

alert_col1, alert_col2, alert_col3 = st.columns(3)

with alert_col1:
    st.markdown("### ⚠️ Funding Expiring")
    if len(expiring_30) > 0:
        st.markdown(f"""
            <div class="alert-box alert-danger">
                <strong>{len(expiring_30)} students</strong> - Expiring within 30 days
            </div>
        """, unsafe_allow_html=True)
    if len(expiring_60) > 0:
        st.markdown(f"""
            <div class="alert-box alert-warning">
                <strong>{len(expiring_60)} students</strong> - Expiring within 60 days
            </div>
        """, unsafe_allow_html=True)
    if len(expiring_90) > 0:
        st.markdown(f"""
            <div class="alert-box alert-info">
                <strong>{len(expiring_90)} students</strong> - Expiring within 90 days
            </div>
        """, unsafe_allow_html=True)
    if len(expiring_30) == 0 and len(expiring_60) == 0 and len(expiring_90) == 0:
        st.success("✅ No funding expiring soon")

with alert_col2:
    st.markdown("### 📋 Missing Reports")
    missing_reports = filtered_df[filtered_df['Funding Status'] == 'Missing Report']
    if len(missing_reports) > 0:
        st.markdown(f"""
            <div class="alert-box alert-danger">
                <strong>{len(missing_reports)} students</strong> have missing reports
            </div>
        """, unsafe_allow_html=True)
        for _, row in missing_reports.head(5).iterrows():
            st.write(f"• {row['Name']} ({row['Student ID']})")
        if len(missing_reports) > 5:
            st.write(f"... and {len(missing_reports) - 5} more")
    else:
        st.success("✅ No missing reports")

with alert_col3:
    st.markdown("### 🎯 At-Risk Students")
    at_risk = filtered_df[filtered_df['Risk Score'] == 'High Risk']
    if len(at_risk) > 0:
        st.markdown(f"""
            <div class="alert-box alert-danger">
                <strong>{len(at_risk)} students</strong> classified as High Risk
            </div>
        """, unsafe_allow_html=True)
        for _, row in at_risk.head(5).iterrows():
            st.write(f"• {row['Name']} ({row['Student ID']}) - GPA: {row['GPA']:.2f}")
        if len(at_risk) > 5:
            st.write(f"... and {len(at_risk) - 5} more")
    else:
        st.success("✅ No high-risk students")

st.markdown("---")

# Student Profiles
st.subheader("👨‍🎓 Student Profiles")

# Grid view - 2 columns
cols = st.columns(2)

for idx, (_, row) in enumerate(filtered_df.iterrows()):
    with cols[idx % 2]:
        # GPA color coding
        gpa = row["GPA"]
        if gpa >= 3.5:
            gpa_class = "gpa-high"
        elif gpa >= 3.0:
            gpa_class = "gpa-medium"
        else:
            gpa_class = "gpa-low"
        
        # Status badge class
        status = row["Funding Status"]
        if status == "Fully Funded":
            status_class = "status-fully-funded"
        elif status == "Pending":
            status_class = "status-pending"
        else:
            status_class = "status-missing"
        
        # Risk badge class
        risk = row["Risk Score"]
        if risk == "Low Risk":
            risk_class = "risk-low"
        elif risk == "Medium Risk":
            risk_class = "risk-medium"
        else:
            risk_class = "risk-high"
        
        # Progress bar
        completion = row['Completion %']
        bar_color = '#4CAF50' if completion >= 75 else '#FFA726' if completion >= 50 else '#EF5350'
        
        # Days remaining
        days = row['Days Remaining']
        days_text = f"{days} days" if days and days > 0 else "Expired" if days and days <= 0 else "N/A"
        days_color = '#c62828' if days and days < 30 else '#e65100' if days and days < 60 else '#0d47a1' if days and days < 90 else '#2e7d32'
        
        st.markdown(f"""
            <div class="student-card">
                <div class="card-header">
                    <span class="student-name">{row['Name']}</span>
                    <span class="student-id">{row['Student ID']}</span>
                </div>
                <div class="card-details">
                    <div class="detail-item">
                        <span class="detail-label">Department</span>
                        <span class="detail-value">🏛️ {row['Department']}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">GPA</span>
                        <span class="detail-value">
                            <span class="gpa-circle {gpa_class}">{gpa:.2f}</span>
                        </span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Funding Status</span>
                        <span class="detail-value">
                            <span class="status-badge {status_class}">{status}</span>
                        </span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Risk Level</span>
                        <span class="detail-value">
                            <span class="{risk_class}">{risk}</span>
                        </span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Funding End</span>
                        <span class="detail-value" style="color: {days_color}; font-weight: 600;">
                            {row['Funding End Date']}<br>
                            <span style="font-size: 12px;">{days_text}</span>
                        </span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Milestone Progress</span>
                        <span class="detail-value" style="font-size: 14px;">
                            {completion:.0f}%
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: {completion}%; background: {bar_color};"></div>
                            </div>
                        </span>
                    </div>
                    <div class="detail-item" style="grid-column: span 2;">
                        <span class="detail-label">Milestones</span>
                        <span class="detail-value" style="font-size: 13px;">
                            {'✅' if row['Proposal Submitted'] else '❌'} Proposal
                            {'✅' if row['Literature Review Complete'] else '❌'} Lit Review
                            {'✅' if row['Midterm Review Complete'] else '❌'} Midterm
                            {'✅' if row['Final Defense Complete'] else '❌'} Defense
                        </span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Analytics Dashboard
st.subheader("📊 Analytics Dashboard")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("#### Funding Status Distribution")
    funding_counts = filtered_df["Funding Status"].value_counts().reset_index()
    funding_counts.columns = ["Funding Status", "Count"]
    if len(funding_counts) > 0:
        st.bar_chart(funding_counts.set_index("Funding Status"), use_container_width=True, height=300)

    st.markdown("#### Risk Distribution")
    risk_counts = filtered_df["Risk Score"].value_counts().reset_index()
    risk_counts.columns = ["Risk Level", "Count"]
    if len(risk_counts) > 0:
        st.bar_chart(risk_counts.set_index("Risk Level"), use_container_width=True, height=300)

with chart_col2:
    st.markdown("#### Department Distribution")
    dept_counts = filtered_df["Department"].value_counts().reset_index()
    dept_counts.columns = ["Department", "Count"]
    if len(dept_counts) > 0:
        st.bar_chart(dept_counts.set_index("Department"), use_container_width=True, height=300)

    st.markdown("#### Milestone Completion")
    milestone_data = []
    milestones = ['Proposal Submitted', 'Literature Review Complete', 'Midterm Review Complete', 'Final Defense Complete']
    for m in milestones:
        count = len(filtered_df[filtered_df[m] == True])
        milestone_data.append({'Milestone': m.replace(' Complete', ''), 'Completed': count})
    milestone_df = pd.DataFrame(milestone_data)
    if len(milestone_df) > 0:
        st.bar_chart(milestone_df.set_index('Milestone'), use_container_width=True, height=300)

# GPA Distribution
st.markdown("#### GPA Distribution")
bins = [2.5, 2.8, 3.1, 3.4, 3.7, 4.0]
labels = ['2.5-2.8', '2.8-3.1', '3.1-3.4', '3.4-3.7', '3.7-4.0']
filtered_df['GPA Range'] = pd.cut(filtered_df['GPA'], bins=bins, labels=labels, include_lowest=True)
gpa_counts = filtered_df['GPA Range'].value_counts().sort_index().reset_index()
gpa_counts.columns = ['GPA Range', 'Count']
if len(gpa_counts) > 0:
    st.bar_chart(gpa_counts.set_index('GPA Range'), use_container_width=True, height=250)

st.markdown("---")

# Export Section
st.subheader("📄 Export Reports")

col_export1, col_export2 = st.columns(2)

with col_export1:
    if st.button("📥 Export Filtered Data (CSV)", use_container_width=True):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"cohort_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key="download_csv"
        )

with col_export2:
    if st.button("📄 Generate Cohort Summary Report", use_container_width=True):
        # Create summary report
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("RESEARCH COHORT MANAGEMENT SYSTEM - SUMMARY REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        report_lines.append("1. COHORT OVERVIEW")
        report_lines.append("-" * 40)
        report_lines.append(f"Total Students: {len(filtered_df)}")
        report_lines.append(f"Fully Funded: {fully_funded}")
        report_lines.append(f"Pending: {pending}")
        report_lines.append(f"Missing Report: {missing}")
        report_lines.append("")
        report_lines.append("2. RISK ANALYSIS")
        report_lines.append("-" * 40)
        report_lines.append(f"Low Risk: {low_risk}")
        report_lines.append(f"Medium Risk: {medium_risk}")
        report_lines.append(f"High Risk: {high_risk}")
        report_lines.append("")
        report_lines.append("3. DEPARTMENT STATISTICS")
        report_lines.append("-" * 40)
        for dept in filtered_df['Department'].unique():
            dept_data = filtered_df[filtered_df['Department'] == dept]
            report_lines.append(f"{dept}: {len(dept_data)} students, Avg GPA: {dept_data['GPA'].mean():.2f}")
        report_lines.append("")
        report_lines.append("4. GPA STATISTICS")
        report_lines.append("-" * 40)
        report_lines.append(f"Mean GPA: {filtered_df['GPA'].mean():.2f}")
        report_lines.append(f"Median GPA: {filtered_df['GPA'].median():.2f}")
        report_lines.append(f"Min GPA: {filtered_df['GPA'].min():.2f}")
        report_lines.append(f"Max GPA: {filtered_df['GPA'].max():.2f}")
        report_lines.append("")
        report_lines.append("5. MILESTONE PROGRESS")
        report_lines.append("-" * 40)
        for m in milestones:
            count = len(filtered_df[filtered_df[m] == True])
            pct = (count / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
            report_lines.append(f"{m}: {count}/{len(filtered_df)} ({pct:.1f}%)")
        report_lines.append("")
        report_lines.append("6. FUNDING EXPIRY ALERTS")
        report_lines.append("-" * 40)
        report_lines.append(f"Expiring within 30 days: {len(expiring_30)}")
        report_lines.append(f"Expiring within 60 days: {len(expiring_60)}")
        report_lines.append(f"Expiring within 90 days: {len(expiring_90)}")
        report_lines.append("")
        report_lines.append("=" * 60)
        report_lines.append("END OF REPORT")
        report_lines.append("=" * 60)
        
        report_text = "\n".join(report_lines)
        
        st.download_button(
            label="Download Summary Report (TXT)",
            data=report_text,
            file_name=f"cohort_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            key="download_report"
        )

st.markdown("---")
st.caption(f"🔄 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Research Cohort Management System v4.0")













# import streamlit as st
# import pandas as pd
# import numpy as np
# from io import BytesIO

# # Set page config
# st.set_page_config(
#     page_title="GRA Cohort Tracker",
#     page_icon="🎓",
#     layout="wide"
# )

# # Initialize session state
# if 'df' not in st.session_state:
#     st.session_state.df = None
# if 'data_source' not in st.session_state:
#     st.session_state.data_source = "Mock Data"
# if 'uploaded_file_name' not in st.session_state:
#     st.session_state.uploaded_file_name = ""

# # Generate mock dataset
# def generate_mock_data():
#     np.random.seed(42)
#     student_ids = [f"STU{i:03d}" for i in range(1, 31)]
#     names = [
#         "Emma Wilson", "Liam Chen", "Sophia Patel", "Noah Rodriguez", "Olivia Kim",
#         "Mason Davis", "Ava Thompson", "Ethan Martinez", "Isabella Garcia", "Lucas Brown",
#         "Mia Johnson", "Alexander Lee", "Charlotte White", "James Anderson", "Amelia Taylor",
#         "Benjamin Moore", "Harper Jackson", "Elijah Martin", "Abigail Thompson", "William Garcia",
#         "Evelyn Martinez", "James Robinson", "Ella Clark", "Oliver Lewis", "Grace Walker",
#         "Daniel Hall", "Chloe Allen", "Matthew Young", "Victoria King", "Joseph Wright"
#     ]
#     departments = np.random.choice(["Ag", "Forestry", "Bio"], size=30, p=[0.3, 0.3, 0.4])
#     gpas = np.round(np.random.uniform(2.5, 4.0, size=30), 2)
#     funding_statuses = np.random.choice(
#         ["Fully Funded", "Missing Report", "Pending"],
#         size=30,
#         p=[0.5, 0.2, 0.3]
#     )
    
#     data = {
#         "Student ID": student_ids,
#         "Name": names,
#         "Department": departments,
#         "GPA": gpas,
#         "Funding Status": funding_statuses
#     }
#     return pd.DataFrame(data)

# # Load data from file
# def load_data(uploaded_file, file_type):
#     try:
#         if file_type == "CSV":
#             df = pd.read_csv(uploaded_file)
#         elif file_type == "Excel":
#             df = pd.read_excel(uploaded_file, engine='openpyxl')
#         else:
#             return None
        
#         required_cols = ["Student ID", "Name", "Department", "GPA", "Funding Status"]
#         missing_cols = [col for col in required_cols if col not in df.columns]
        
#         if missing_cols:
#             st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
#             st.info("📋 Required columns: Student ID, Name, Department, GPA, Funding Status")
#             return None
            
#         return df
#     except Exception as e:
#         st.error(f"❌ Error loading file: {str(e)}")
#         return None

# # Initialize with mock data
# if st.session_state.df is None:
#     st.session_state.df = generate_mock_data()
#     st.session_state.data_source = "Mock Data"

# # Custom CSS for visual cards
# st.markdown("""
#     <style>
#     .student-card {
#         background: white;
#         border-radius: 12px;
#         padding: 20px;
#         margin: 10px 0;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.1);
#         border-left: 5px solid #4CAF50;
#         transition: transform 0.2s;
#     }
#     .student-card:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 4px 12px rgba(0,0,0,0.15);
#     }
#     .card-header {
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         margin-bottom: 12px;
#     }
#     .student-name {
#         font-size: 18px;
#         font-weight: 600;
#         color: #1a1a1a;
#     }
#     .student-id {
#         font-size: 14px;
#         color: #666;
#         background: #f0f0f0;
#         padding: 4px 12px;
#         border-radius: 20px;
#     }
#     .card-details {
#         display: grid;
#         grid-template-columns: repeat(3, 1fr);
#         gap: 12px;
#         margin-top: 10px;
#     }
#     .detail-item {
#         display: flex;
#         flex-direction: column;
#     }
#     .detail-label {
#         font-size: 11px;
#         text-transform: uppercase;
#         color: #888;
#         font-weight: 600;
#         letter-spacing: 0.5px;
#     }
#     .detail-value {
#         font-size: 16px;
#         font-weight: 500;
#         color: #333;
#         margin-top: 2px;
#     }
#     .status-badge {
#         display: inline-block;
#         padding: 4px 14px;
#         border-radius: 20px;
#         font-size: 13px;
#         font-weight: 500;
#     }
#     .status-fully-funded {
#         background: #e8f5e9;
#         color: #2e7d32;
#     }
#     .status-pending {
#         background: #fff3e0;
#         color: #e65100;
#     }
#     .status-missing {
#         background: #ffebee;
#         color: #c62828;
#     }
#     .gpa-circle {
#         display: inline-block;
#         width: 40px;
#         height: 40px;
#         border-radius: 50%;
#         text-align: center;
#         line-height: 40px;
#         font-weight: 700;
#         font-size: 16px;
#         color: white;
#     }
#     .gpa-high {
#         background: #4CAF50;
#     }
#     .gpa-medium {
#         background: #FFA726;
#     }
#     .gpa-low {
#         background: #EF5350;
#     }
#     .upload-section {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 30px;
#         border-radius: 15px;
#         color: white;
#         margin-bottom: 20px;
#     }
#     .stats-grid {
#         display: grid;
#         grid-template-columns: repeat(4, 1fr);
#         gap: 16px;
#         margin: 20px 0;
#     }
#     .stat-card {
#         background: white;
#         padding: 20px;
#         border-radius: 12px;
#         text-align: center;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.08);
#     }
#     .stat-number {
#         font-size: 28px;
#         font-weight: 700;
#         color: #1a1a1a;
#     }
#     .stat-label {
#         font-size: 13px;
#         color: #666;
#         margin-top: 4px;
#         text-transform: uppercase;
#         letter-spacing: 0.5px;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Sidebar - Data Source
# st.sidebar.title("📁 Data Source")

# data_option = st.sidebar.radio(
#     "Choose Data Source",
#     ["📊 Mock Data", "📤 Upload CSV", "📤 Upload Excel"],
#     index=0 if st.session_state.data_source == "Mock Data" else 1
# )

# # Handle data source
# if data_option == "📊 Mock Data":
#     if st.session_state.data_source != "Mock Data":
#         st.session_state.df = generate_mock_data()
#         st.session_state.data_source = "Mock Data"
#         st.session_state.uploaded_file_name = ""
#         st.rerun()

# elif data_option == "📤 Upload CSV":
#     uploaded_file = st.sidebar.file_uploader(
#         "Drop your CSV file here",
#         type=['csv'],
#         key="csv_upload"
#     )
#     if uploaded_file is not None:
#         st.session_state.uploaded_file_name = uploaded_file.name
#         df = load_data(uploaded_file, "CSV")
#         if df is not None:
#             st.session_state.df = df
#             st.session_state.data_source = "CSV"
#             st.sidebar.success(f"✅ Loaded {len(df)} students from {uploaded_file.name}")
#     elif st.session_state.data_source == "Mock Data":
#         st.sidebar.info("📤 Upload a CSV file to get started")
#     else:
#         st.sidebar.warning("⚠️ Please upload a CSV file")

# elif data_option == "📤 Upload Excel":
#     uploaded_file = st.sidebar.file_uploader(
#         "Drop your Excel file here",
#         type=['xlsx', 'xls'],
#         key="excel_upload"
#     )
#     if uploaded_file is not None:
#         st.session_state.uploaded_file_name = uploaded_file.name
#         df = load_data(uploaded_file, "Excel")
#         if df is not None:
#             st.session_state.df = df
#             st.session_state.data_source = "Excel"
#             st.sidebar.success(f"✅ Loaded {len(df)} students from {uploaded_file.name}")
#     elif st.session_state.data_source == "Mock Data":
#         st.sidebar.info("📤 Upload an Excel file to get started")
#     else:
#         st.sidebar.warning("⚠️ Please upload an Excel file")

# df = st.session_state.df

# # Sidebar - Filters
# st.sidebar.markdown("---")
# st.sidebar.title("🔍 Filters")

# sort_order = st.sidebar.radio(
#     "Sort by Name",
#     options=["A-Z", "Z-A"],
#     index=0
# )

# all_depts = sorted(df["Department"].unique().tolist())
# selected_depts = st.sidebar.multiselect(
#     "Department",
#     options=all_depts,
#     default=all_depts
# )

# gpa_min_val = float(df["GPA"].min())
# gpa_max_val = float(df["GPA"].max())
# gpa_min, gpa_max = st.sidebar.slider(
#     "GPA Range",
#     min_value=gpa_min_val,
#     max_value=gpa_max_val,
#     value=(gpa_min_val, gpa_max_val),
#     step=0.1
# )

# # Apply filters
# filtered_df = df[
#     (df["Department"].isin(selected_depts)) &
#     (df["GPA"] >= gpa_min) &
#     (df["GPA"] <= gpa_max)
# ].copy()

# # Apply sorting
# if sort_order == "A-Z":
#     filtered_df = filtered_df.sort_values("Name", ascending=True)
# else:
#     filtered_df = filtered_df.sort_values("Name", ascending=False)

# # Main Dashboard
# st.title("🎓 Graduate Research Assistant (GRA) Cohort Tracker")

# # Data source indicator
# col1, col2, col3 = st.columns([2, 2, 1])
# with col1:
#     if st.session_state.data_source in ["CSV", "Excel"]:
#         st.info(f"📂 Data Source: **{st.session_state.uploaded_file_name}** ({len(df)} records)")
#     else:
#         st.info(f"📊 Data Source: **{st.session_state.data_source}** ({len(df)} records)")

# with col3:
#     if st.button("🔄 Reset to Mock Data", use_container_width=True):
#         st.session_state.df = generate_mock_data()
#         st.session_state.data_source = "Mock Data"
#         st.session_state.uploaded_file_name = ""
#         st.rerun()

# st.markdown("---")

# # Stats Grid
# total = len(filtered_df)
# fully_funded = len(filtered_df[filtered_df["Funding Status"] == "Fully Funded"])
# pending = len(filtered_df[filtered_df["Funding Status"] == "Pending"])
# missing = len(filtered_df[filtered_df["Funding Status"] == "Missing Report"])

# st.markdown(f"""
#     <div class="stats-grid">
#         <div class="stat-card">
#             <div class="stat-number">{total}</div>
#             <div class="stat-label">👥 Total Students</div>
#         </div>
#         <div class="stat-card">
#             <div class="stat-number">{fully_funded}</div>
#             <div class="stat-label">✅ Fully Funded</div>
#         </div>
#         <div class="stat-card">
#             <div class="stat-number">{pending}</div>
#             <div class="stat-label">⏳ Pending</div>
#         </div>
#         <div class="stat-card">
#             <div class="stat-number">{missing}</div>
#             <div class="stat-label">⚠️ Missing Report</div>
#         </div>
#     </div>
# """, unsafe_allow_html=True)

# st.markdown("---")

# # Student Cards - Visual Display
# st.subheader("👨‍🎓 Student Profiles")

# # Grid view - 2 columns
# cols = st.columns(2)

# for idx, (_, row) in enumerate(filtered_df.iterrows()):
#     with cols[idx % 2]:
#         # GPA color coding
#         gpa = row["GPA"]
#         if gpa >= 3.5:
#             gpa_class = "gpa-high"
#         elif gpa >= 3.0:
#             gpa_class = "gpa-medium"
#         else:
#             gpa_class = "gpa-low"
        
#         # Status badge class
#         status = row["Funding Status"]
#         if status == "Fully Funded":
#             status_class = "status-fully-funded"
#         elif status == "Pending":
#             status_class = "status-pending"
#         else:
#             status_class = "status-missing"
        
#         st.markdown(f"""
#             <div class="student-card">
#                 <div class="card-header">
#                     <span class="student-name">{row['Name']}</span>
#                     <span class="student-id">{row['Student ID']}</span>
#                 </div>
#                 <div class="card-details">
#                     <div class="detail-item">
#                         <span class="detail-label">Department</span>
#                         <span class="detail-value">🏛️ {row['Department']}</span>
#                     </div>
#                     <div class="detail-item">
#                         <span class="detail-label">GPA</span>
#                         <span class="detail-value">
#                             <span class="gpa-circle {gpa_class}">{gpa:.2f}</span>
#                         </span>
#                     </div>
#                     <div class="detail-item">
#                         <span class="detail-label">Funding Status</span>
#                         <span class="detail-value">
#                             <span class="status-badge {status_class}">{status}</span>
#                         </span>
#                     </div>
#                 </div>
#             </div>
#         """, unsafe_allow_html=True)

# # Charts section
# st.markdown("---")
# st.subheader("📊 Analytics Dashboard")

# col_chart1, col_chart2 = st.columns(2)

# with col_chart1:
#     st.markdown("#### Funding Status Distribution")
#     funding_counts = filtered_df["Funding Status"].value_counts().reset_index()
#     funding_counts.columns = ["Funding Status", "Count"]
#     if len(funding_counts) > 0:
#         st.bar_chart(
#             funding_counts.set_index("Funding Status"),
#             use_container_width=True,
#             height=300
#         )
#     else:
#         st.info("No data to display")

# with col_chart2:
#     st.markdown("#### Department Distribution")
#     dept_counts = filtered_df["Department"].value_counts().reset_index()
#     dept_counts.columns = ["Department", "Count"]
#     if len(dept_counts) > 0:
#         st.bar_chart(
#             dept_counts.set_index("Department"),
#             use_container_width=True,
#             height=300
#         )
#     else:
#         st.info("No data to display")

# # GPA Distribution
# # GPA Distribution
# st.markdown("#### GPA Distribution")
# # Create GPA bins with cleaner labels
# bins = [2.5, 2.8, 3.1, 3.4, 3.7, 4.0]
# labels = ['2.5-2.8', '2.8-3.1', '3.1-3.4', '3.4-3.7', '3.7-4.0']
# filtered_df['GPA Range'] = pd.cut(filtered_df['GPA'], bins=bins, labels=labels, include_lowest=True)
# gpa_counts = filtered_df['GPA Range'].value_counts().sort_index().reset_index()
# gpa_counts.columns = ['GPA Range', 'Count']
# if len(gpa_counts) > 0:
#     st.bar_chart(
#         gpa_counts.set_index('GPA Range'),
#         use_container_width=True,
#         height=250
#     )

# # Export and Summary
# st.markdown("---")
# col_exp1, col_exp2 = st.columns([1, 3])

# with col_exp1:
#     if st.button("📥 Export Filtered CSV", use_container_width=True):
#         csv = filtered_df.to_csv(index=False)
#         st.download_button(
#             label="Download",
#             data=csv,
#             file_name=f"gra_cohort_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
#             mime="text/csv",
#             key="download_btn"
#         )

# with st.expander("📊 Detailed Statistics", expanded=False):
#     col1, col2 = st.columns(2)
#     with col1:
#         st.write("**GPA Statistics**")
#         stats_df = pd.DataFrame({
#             "Statistic": ["Mean", "Median", "Min", "Max", "Std Dev"],
#             "Value": [
#                 f"{filtered_df['GPA'].mean():.2f}",
#                 f"{filtered_df['GPA'].median():.2f}",
#                 f"{filtered_df['GPA'].min():.2f}",
#                 f"{filtered_df['GPA'].max():.2f}",
#                 f"{filtered_df['GPA'].std():.2f}"
#             ]
#         })
#         st.dataframe(stats_df, hide_index=True, use_container_width=True)
#     with col2:
#         st.write("**Department Breakdown**")
#         dept_breakdown = filtered_df.groupby("Department").agg({
#             "Student ID": "count",
#             "GPA": "mean"
#         }).round(2)
#         dept_breakdown.columns = ["Count", "Avg GPA"]
#         st.dataframe(dept_breakdown, use_container_width=True)

# st.markdown("---")
# st.caption(f"🔄 Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')} | GRA Cohort Tracker v3.0")