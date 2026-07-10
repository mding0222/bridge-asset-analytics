# Bridge Asset Analytics

## Project Overview

This project demonstrates an end-to-end bridge asset analytics solution using **MySQL** and **Power BI**.

The project simulates how a transport authority can analyse bridge assets, inspection records, defect information and maintenance plans to support infrastructure planning, maintenance prioritisation and business reporting.

The workflow covers the complete analytics process from relational database design and SQL analysis to interactive dashboard development and business reporting.

---

## Business Scenario

A transport authority is responsible for managing bridge assets across multiple provinces.

Bridge inspection data, defect records and maintenance plans are collected from different operational systems. Decision makers require reliable reporting to identify high-risk bridges, monitor asset condition, analyse maintenance activities and support infrastructure investment decisions.

This project demonstrates how these datasets can be integrated into a relational database and transformed into meaningful business insights using SQL and Power BI.

---

## Project Objectives

- Design a relational database using a Star Schema model
- Analyse bridge inspection, defect and maintenance data using SQL
- Develop an interactive Power BI dashboard for infrastructure reporting
- Identify high-risk bridges requiring maintenance attention
- Support data-driven maintenance planning and budget allocation
- Demonstrate practical SQL techniques commonly used in Data Analytics

---

## Data Model

![Data Model](images/data_model.png)

The database follows a dimensional modelling approach.

### Dimension Tables

- **dim_bridge** – Bridge asset information
- **dim_province** – Province information
- **dim_road** – Road network information

### Fact Tables

- **fact_inspection** – Bridge inspection records
- **fact_defect** – Recorded bridge defects
- **fact_maintenance** – Planned maintenance activities

The bridge table acts as the central dimension connecting inspection, defect and maintenance information.

---

# Database & SQL

The project database was built in MySQL.

The SQL analysis progresses from fundamental querying techniques to more advanced analytical SQL used in real business reporting scenarios.

## SQL Topics Covered

### Basic SQL

- SELECT
- WHERE
- ORDER BY
- Aggregate Functions
- GROUP BY
- HAVING

### Join Analysis

- INNER JOIN
- LEFT JOIN
- RIGHT JOIN
- Understanding row multiplication after joins
- Fact-to-fact aggregation using multiple CTEs

### Business Logic

- CASE WHEN classification
- Risk bridge identification
- Risk bridge ranking

### Advanced SQL

- Common Table Expressions (CTE)
- Multiple CTEs
- Non-correlated Subqueries
- Aggregate comparison using subqueries
- COALESCE()
- Query Block design
- Window Functions (ROW_NUMBER, COUNT OVER, RANK) *(ongoing learning)*

---

## Example Business Analysis

The project includes SQL solutions for common infrastructure reporting tasks such as:

- Total bridge assets
- Bridge distribution by province
- Bridge condition analysis
- Defect statistics
- Maintenance cost summary
- High-risk bridge identification
- Bridge defect and maintenance summaries
- Bridges with above-average defect counts
- Bridges with above-average maintenance activity
- Latest inspection record retrieval
- Bridge ranking based on inspection condition

---

## Power BI Dashboard

The dashboard provides an overview of bridge asset performance through interactive visualisations.

### Dashboard 1 – Executive Summary

![Dashboard 1](images/dashboard_page1.png)

Includes:

- Total Bridges
- High Risk Bridges
- Total Maintenance Cost
- Total Defects
- Total Bridge Length
- Maintenance Count
- Bridge distribution by province
- Bridge condition distribution by province
- Bridge maintenance cost distribution by province

### Dashboard 2 – Inspection & Defect Analysis

![Dashboard 2](images/dashboard_page2.png)

Includes:

- Province slicer
- Top 10 high-risk bridges
- Defect distribution by bridge component
- Most common defect types

---

## Key Business Insights

Example insights generated from the dashboard include:

- Provinces with the highest maintenance investment
- Distribution of bridge condition ratings
- Most common bridge defect types
- Bridges requiring priority maintenance
- Relationships between inspection results and maintenance planning
- Bridges with above-average defect frequency
- Bridges with intensive maintenance activity
- Latest inspection status for infrastructure assets

---

## Repository Structure

```text
bridge-asset-analytics
│
├── data
│   ├── dim_bridge.csv
│   ├── dim_province.csv
│   ├── dim_road.csv
│   ├── fact_defect.csv
│   ├── fact_inspection.csv
│   ├── fact_maintenance.csv
│   └── data_dictionary.csv
│
├── images
│   ├── dashboard_page1.png
│   ├── dashboard_page2.png
│   └── data_model.png
│
├── powerbi
│   └── Bridge Asset Dashboard.pbix
│
├── python
│   └── generate_bridge_data.py
│
├── sql
│   ├── 01_database_setup.sql
│   ├── 02_basic_queries.sql
│   ├── 03_join_queries.sql
│   ├── 04_case_when.sql
│   └── 05_advanced_sql_analysis.sql
│
└── README.md
```

---

## Tools Used

- MySQL
- MySQL Workbench
- Power BI
- Python
- GitHub

---

## Skills Demonstrated

### SQL

- Data querying
- Relational joins
- Aggregate analysis
- Conditional logic
- Common Table Expressions (CTE)
- Subqueries
- Window Functions
- Query optimisation concepts

### Data Analytics

- Star Schema modelling
- Business reporting
- KPI development
- Data transformation
- Infrastructure asset analytics

### Visualisation

- Power BI
- Interactive dashboard design
- Business KPI reporting

---

## Future Improvements

Planned enhancements include:

- Additional Window Function examples
- Advanced ranking analysis
- Trend analysis across inspection periods
- Predictive maintenance analysis using Python
- Dashboard performance optimisation

---

## Author

**Ming Ding**

Master of Artificial Intelligence and Machine Learning  
The University of Adelaide

Interested in Data Analytics, Business Intelligence and Infrastructure Asset Management.
