# Research Cohort Management System

A Streamlit-based dashboard for managing graduate research cohorts, funding status, academic performance, and student progress.

## Overview

Research labs and graduate programs often manage student records across multiple spreadsheets and reports. This project provides a centralized dashboard for viewing, filtering, analyzing, and exporting cohort information through a simple web interface.

The application supports data uploads, student analytics, funding monitoring, cohort statistics, and administrative reporting.

## Features

* Student cohort dashboard
* CSV and Excel file upload
* Student profile cards
* Department filtering
* GPA range filtering
* Student sorting
* Funding status tracking
* Cohort analytics dashboard
* GPA distribution analysis
* Department statistics
* CSV export functionality
* Interactive visualizations

## Technology Stack

* Python
* Streamlit
* Pandas
* NumPy
* OpenPyXL

## Running Locally

Install dependencies:

```bash
pip install streamlit pandas numpy openpyxl
```

Run the application:

```bash
streamlit run app.py
```

## Supported Dataset Format

Required columns:

| Column         | Description               |
| -------------- | ------------------------- |
| Student ID     | Unique student identifier |
| Name           | Student name              |
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

## Use Cases

* Graduate research assistant management
* Academic progress monitoring
* Funding oversight
* Cohort reporting
* Research administration

## Author

Arun Samy V

GitHub: https://github.com/arunsamy4444
Portfolio: https://arunsamyportfolio.vercel.app/
