# Research Cohort Management System

A web-based dashboard built with Streamlit for managing graduate research cohorts, tracking funding status, monitoring academic performance, and generating cohort-level analytics.

## Live Demo

**Application:** https://research-cohort-management-system-wm6std8baczbwecufnzi8p.streamlit.app/

## Overview

Research laboratories, graduate programs, and academic departments often manage student information across multiple spreadsheets and reports. This project provides a centralized dashboard for cohort management, allowing administrators to upload datasets, monitor student progress, analyze funding status, and generate insights through an interactive interface.

The application supports both mock datasets and user-uploaded CSV/Excel files, making it useful for demonstrations, testing, and real-world administrative workflows.

## Key Features

### Data Management

* Upload CSV datasets
* Upload Excel datasets (.xlsx)
* Automatic data validation
* Mock dataset generation for testing

### Student Monitoring

* Student profile cards
* Funding status tracking
* GPA monitoring
* Department categorization

### Filtering & Search

* Department-based filtering
* GPA range filtering
* Alphabetical sorting
* Dynamic cohort views

### Analytics Dashboard

* Funding status distribution
* Department distribution analysis
* GPA distribution charts
* Cohort summary statistics

### Reporting

* Export filtered datasets to CSV
* Detailed statistical summaries
* Department performance breakdowns

## Technology Stack

| Category            | Technology                |
| ------------------- | ------------------------- |
| Language            | Python                    |
| Framework           | Streamlit                 |
| Data Processing     | Pandas                    |
| Numerical Computing | NumPy                     |
| Excel Support       | OpenPyXL                  |
| Visualization       | Streamlit Charts / Plotly |

## Project Structure

```text
research-cohort-management-system/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/arunsamy4444/research-cohort-management-system.git
cd research-cohort-management-system
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run locally:

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

## Expected Dataset Format

Required columns:

| Column         | Description               |
| -------------- | ------------------------- |
| Student ID     | Unique student identifier |
| Name           | Student full name         |
| Department     | Academic department       |
| GPA            | Student GPA               |
| Funding Status | Funding information       |

Example:

```csv
Student ID,Name,Department,GPA,Funding Status
STU001,Emma Wilson,Agriculture,3.82,Fully Funded
STU002,Liam Chen,Forestry,3.45,Pending
STU003,Sophia Patel,Biology,2.91,Missing Report
```

## Potential Use Cases

* Graduate Research Assistant (GRA) tracking
* Academic cohort management
* Research administration support
* Funding oversight and monitoring
* Student performance analytics
* Department-level reporting

## Future Improvements

* Risk assessment engine
* Funding expiry alerts
* Research milestone tracking
* Faculty supervisor assignment
* PDF report generation
* Authentication and role-based access
* Database integration

## Author

**Arun Samy V**

Portfolio: https://arunsamyportfolio.vercel.app/

GitHub: https://github.com/arunsamy4444

## License

This project is provided for educational, research, and portfolio purposes.
