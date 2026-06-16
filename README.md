# Research Cohort Management System

A Streamlit-based research administration dashboard designed to help universities, research labs, graduate coordinators, and principal investigators manage student cohorts, funding status, academic progress, and research milestones through an interactive visual interface.

## Overview

Managing graduate research cohorts often involves multiple spreadsheets, manual reporting, funding tracking, and progress monitoring. This project provides a centralized dashboard that simplifies cohort management through real-time filtering, analytics, risk assessment, and reporting features.

The system allows administrators to upload student datasets, monitor funding status, track academic performance, identify at-risk students, and generate cohort-level insights through an intuitive web interface.

## Features

### Cohort Management

* View and manage graduate research student records
* Student profile cards with key information
* Department-based organization
* Sort and filter student data dynamically

### Data Import

* CSV file upload support
* Excel (.xlsx) file upload support
* Automatic dataset validation
* Required column verification
* Error handling for invalid files

### Student Analytics

* Funding status distribution
* Department-wise statistics
* GPA distribution analysis
* Cohort summary metrics
* Interactive visual dashboards

### Risk Assessment

* Student risk classification
* Identification of students requiring attention
* Funding and academic performance monitoring
* Administrative oversight support

### Research Milestone Tracking

* Proposal progress monitoring
* Literature review tracking
* Midterm evaluation tracking
* Final defense progress monitoring
* Cohort completion visibility

### Funding Management

* Funding status monitoring
* Funding expiry tracking
* Remaining funding duration calculations
* Early warning indicators

### Search & Filtering

* Student search functionality
* Department filters
* GPA range filtering
* Sorting options
* Multi-criteria filtering

### Reporting

* Export filtered datasets to CSV
* Cohort-level statistics
* Administrative reporting support
* Data-driven decision making

## Technology Stack

### Frontend

* Streamlit

### Data Processing

* Pandas
* NumPy

### File Handling

* OpenPyXL

### Visualization

* Streamlit Charts

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

Run the application:

```bash
streamlit run app.py
```

## Required Dataset Format

The application expects the following columns:

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
STU002,Liam Chen,Forestry,3.41,Pending
STU003,Sophia Patel,Biology,2.94,Missing Report
```

## Use Cases

### Research Laboratories

* Monitor graduate research assistants
* Track funding allocations
* Identify students requiring intervention
* Generate administrative reports

### Graduate Programs

* Cohort management
* Progress tracking
* Academic monitoring
* Student analytics

### University Departments

* Funding oversight
* Student reporting
* Department statistics
* Administrative decision support

## Future Improvements

* Faculty supervisor assignment
* Authentication and role-based access
* Database integration
* Automated email notifications
* PDF report generation
* Research publication tracking
* Cloud deployment support
* Multi-cohort management

## Author

**Arun Samy V**

* Portfolio: https://arunsamy.vercel.app
* GitHub: https://github.com/arunsamy4444

## License

This project is provided for educational, research, and portfolio purposes.
