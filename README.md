# DS_Vaccination-Data-Analysis-and-Visualization
DS_Vaccination Data Analysis and Visualization
Vaccination Data Analysis
Overview
This project analyzes global vaccination data, including vaccination coverage, incidence rates, reported cases, and vaccine introduction schedules. It integrates data cleaning, SQL database storage, and exploratory data analysis (EDA) to provide insights into vaccination trends and their relationship with disease incidence.

Features
Data Cleaning: Handles missing data, formats columns, and normalizes coverage percentages.
SQL Database Integration: Stores data in a MySQL database for efficient querying and analysis.
Exploratory Data Analysis (EDA):
Visualization of vaccination trends.
Correlation analysis between vaccination rates and disease incidence.
Data Sources
The project uses the following datasets:

Coverage Data: Vaccination coverage percentages by country and year.
Incidence Data: Disease incidence rates by country and year.
Reported Cases: Number of reported cases for diseases by country and year.
Vaccine Introduction Data: Introduction dates of vaccines by country.
Vaccine Schedule Data: Vaccine schedules, target populations, and administration details.
Requirements
Python 3.7+
MySQL Server
Libraries:
pandas
numpy
sqlalchemy
pymysql
matplotlib
seaborn
Setup Instructions
1. Clone the Repository
bash
Copy
Edit
git clone <repository_url>
cd <repository_folder>
2. Install Dependencies
Install the required Python libraries:

bash
Copy
Edit
pip install pandas numpy sqlalchemy pymysql matplotlib seaborn
3. Set Up the MySQL Database
Ensure MySQL is installed and running.
Update the username, password, host, and port variables in the script to match your MySQL configuration.
Create the database and tables by running the script.
4. Run the Script
Execute the Python script to clean data, store it in the database, and perform analysis:

bash
Copy
Edit
python vaccination_analysis.py
Project Structure
bash
Copy
Edit
.
├── coverage-data.xlsx           # Vaccination coverage data
├── incidence-rate-data.xlsx     # Disease incidence rate data
├── reported-cases-data.xlsx     # Reported cases data
├── vaccine-introduction-data.xlsx # Vaccine introduction dates
├── vaccine-schedule-data.xlsx   # Vaccine schedules and target populations
├── vaccination_analysis.py      # Main script for data analysis
└── README.md                    # Project documentation
Key Functions
1. Data Cleaning
Handles missing data using forward fill.
Converts year columns to datetime format.
Normalizes coverage percentages.
2. SQL Database Setup
Creates a MySQL database and tables for storing datasets.
Populates tables with cleaned data.
3. Exploratory Data Analysis
Vaccination Trends: Visualizes vaccination coverage over time for different countries.
Correlation Analysis: Calculates the correlation between vaccination rates and disease incidence.
Example Outputs
Vaccination Trends

Correlation Analysis
