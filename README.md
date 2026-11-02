# 🍬 Nassau Candy Distributor – Shipping Route Efficiency Analysis

## 📌 Project Overview

This project focuses on analyzing shipping operations for Nassau Candy Distributor to evaluate delivery performance, identify inefficient shipping routes, and understand factors affecting shipment lead times.

Using Python, SQL, Pandas, and Streamlit, the project transforms raw shipping data into meaningful business insights through data cleaning, exploratory data analysis, and interactive visualizations.

The objective is to help businesses understand shipping patterns, monitor delivery delays, and identify opportunities to improve logistics efficiency.

## 🎯 Business Objectives

- Analyze overall shipping performance and delivery lead times.
- Identify the fastest and slowest shipping routes.
- Compare delivery performance across different shipping modes.
- Evaluate state-wise shipment performance.
- Analyze geographical variations in shipping lead times.
- Identify delayed shipments based on a configurable delay threshold.

## 🛠️ Tools & Technologies

| Tool | Purpose |
|---|---|
| Python | Data analysis and processing |
| Pandas | Data cleaning and manipulation |
| SQL | Data querying and analysis |
| Plotly | Interactive data visualizations |
| Streamlit | Interactive dashboard development |
| Jupyter Notebook | Exploratory data analysis |
| GitHub | Project documentation and version control |

## 📂 Project Structure

```text
nassau-candy-analysis/
│
├── data/
│   ├── raw_dataset.csv
│   └── cleaned.csv
│
├── Nassau_Candy_Analysis.ipynb
│
├── my_app.py
│
├── requirements.txt
│
└── README.md
```

## 🔍 Project Workflow

### 1. Data Understanding
- Imported and examined the raw shipping dataset.
- Reviewed dataset structure, data types, and missing values.
- Identified important shipping-related variables.

### 2. Data Cleaning and Preparation
- Handled missing and inconsistent values.
- Converted order dates into appropriate date formats.
- Prepared relevant columns for analysis.
- Created calculated metrics such as shipping lead time and delivery delay indicators.

### 3. Exploratory Data Analysis (EDA)
- Analyzed shipment volumes and delivery lead times.
- Examined shipping performance across different modes.
- Evaluated factory-to-state shipping routes.
- Identified geographical differences in delivery performance.

### 4. Interactive Dashboard Development

Developed a Streamlit dashboard with four analytical sections:

**A. Shipping Route Analysis**
- Identifies the fastest and slowest shipping routes.
- Compares average lead times across routes.
- Displays shipment volumes by route.

**B. Shipping Mode Analysis**
- Compares delivery lead-time distributions across shipping modes.
- Uses box plots to understand variability and outliers.
- Evaluates average lead time by shipping mode.

**C. State-wise Drill-down**
- Analyzes average lead time across states.
- Compares shipment volumes by state.
- Allows users to select individual states and explore shipment details.

**D. Geographical Analysis**
- Visualizes state-wise shipping performance using an interactive US map.
- Allows users to switch between average lead time, delay percentage, and shipment volume.

## 📊 Key Performance Indicators

The dashboard includes the following performance metrics:

- **Total Shipments:** Number of shipment records in the selected dataset.
- **Average Lead Time:** Average number of days taken for shipments.
- **Delay Percentage:** Percentage of shipments exceeding the selected delay threshold.

The dashboard also provides interactive filters for:
- Shipping mode
- Region
- State
- Order date range
- Delay threshold

## 💡 Business Value

This analysis can help businesses:

- Identify routes with longer delivery lead times.
- Understand differences in shipping mode performance.
- Monitor geographical variations in delivery efficiency.
- Track delivery delays using configurable thresholds.
- Support data-driven logistics and operational decisions.

## 🚀 Running the Streamlit Dashboard

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Navigate to the Project Folder

```bash
cd nassau-candy-analysis
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Dashboard

```bash
streamlit run my_app.py
```

The dashboard will open in your browser.

**Note:** Ensure that the cleaned dataset is available at the file path referenced in `my_app.py`.

## 📦 Requirements

The project dependencies are listed in `requirements.txt`.

## 👩‍💻 Author

**Sakshi Pocham Zadi**

Engineering Graduate | Aspiring Business Analyst

Interested in business analytics, data-driven problem solving, and operational efficiency.

---

⭐ If you find this project useful, feel free to explore the repository and its analytical workflow.
