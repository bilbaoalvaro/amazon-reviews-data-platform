# Amazon Reviews — Data & Databases

Final project for the **Databases** course in the BSc in Mathematical
Engineering & Artificial Intelligence at **Universidad Pontificia Comillas
(ICAI)**.

The project builds a small data-management and analysis system around Amazon
reviews using three complementary database technologies:

- **MySQL** for structured entities and relationships
- **MongoDB** for semi-structured review content
- **Neo4j** for graph-based relationships and similarity analysis

A Python application connects the databases and provides interactive
command-line visualizations and analysis.

## What the project covers

### 1. Data modelling and loading

A relational schema is designed around `USER`, `ITEM` and `REVIEW`, with a
composite key for reviews. Structured fields are stored in MySQL while
semi-structured fields such as review text and helpfulness arrays are stored
in MongoDB.

### 2. Data visualization

The Python menu provides analyses including:

- Reviews over time
- Article popularity
- Rating distributions
- Review activity over time
- Reviews per user
- Word clouds by product category
- Unique users by category

### 3. Neo4j graph analysis

The project uses Neo4j to analyse relationships between users and articles,
including:

- User similarity based on Pearson correlation
- User–article connections
- Users reviewing multiple product categories
- Popular articles and common items between users

### 4. New dataset integration

A new Amazon review dataset can be inserted into the existing MySQL and
MongoDB architecture without redesigning the core schema.

### 5. Further analysis

The project also includes additional visualizations with Tableau and a
simple popularity-based recommendation model combining article rating,
review count and user category preferences.

## Project structure

```text
amazon-reviews-data-platform/
├── README.md
├── requirements.txt
├── config.py
├── .env.example
├── .gitignore
├── src/
│   ├── load_data.py
│   ├── insert_dataset.py
│   ├── menu_visualization.py
│   └── neo4j_analysis.py
├── data/
│   └── README.md
└── docs/
    ├── project_report.pdf
    └── project_poster.pdf
```

## Technologies

**Python · MySQL · MongoDB · Neo4j · SQL · Cypher · Matplotlib · WordCloud · Tableau**

## Setup

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and provide the credentials for your local
MySQL, MongoDB and Neo4j installations.

The expected Amazon review JSON files should be placed in `data/`.

The loading scripts create the MySQL database/tables and populate MongoDB.
The visualization and Neo4j modules can then be run against the local
databases.

## Project context

**Course:** Databases  
**Degree:** Mathematical Engineering & Artificial Intelligence  
**University:** Universidad Pontificia Comillas — ICAI  
**Academic year:** 2025/26  

**Individual academic project.**
