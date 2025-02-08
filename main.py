import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
import seaborn as sns
import pymysql  # Ensure pymysql is installed

def clean_data(df):
    """
    Cleans the input dataframe by handling missing values,
    formatting date columns, and normalizing units.
    """
    # Handling missing data
    if 'COVERAGE' in df.columns:  
        df['COVERAGE'] = df['COVERAGE'].ffill()  # Fix for FutureWarning
    if 'INCIDENCE_RATE' in df.columns:
        df['INCIDENCE_RATE'] = df['INCIDENCE_RATE'].ffill()
    if 'CASES' in df.columns:
        df['CASES'] = df['CASES'].ffill()
    
    df.dropna(inplace=True)

    # Convert 'YEAR' to datetime
    if 'YEAR' in df.columns:
        try:
            df['YEAR'] = pd.to_datetime(df['YEAR'], errors='coerce', format='%Y')
            df.dropna(subset=['YEAR'], inplace=True)
        except Exception as e:
            print(f"Error formatting YEAR column: {e}")

    # Normalize 'COVERAGE' column
    if 'COVERAGE' in df.columns:
        df['COVERAGE'] = df['COVERAGE'] / 100  

    return df


# Load and clean vaccination data
coverage_data = pd.read_excel('coverage-data.xlsx')
incidence_data = pd.read_excel('incidence-rate-data.xlsx')
reported_cases_data = pd.read_excel('reported-cases-data.xlsx')
vaccine_intro_data = pd.read_excel('vaccine-introduction-data.xlsx')
vaccine_schedule_data = pd.read_excel('vaccine-schedule-data.xlsx')

# Clean data
coverage_data = clean_data(coverage_data)
incidence_data = clean_data(incidence_data)
reported_cases_data = clean_data(reported_cases_data)
vaccine_intro_data = clean_data(vaccine_intro_data)
vaccine_schedule_data = clean_data(vaccine_schedule_data)

# Step 2: SQL Database Setup
username = "root"  # Replace with your MySQL username
password = "123"      # Replace with your MySQL password (if any)
host = "localhost"  # MySQL server host
port = 3306         # Default MySQL port

# Connect to MySQL server
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}")

def create_database(database_name):
    """
    Creates a MySQL database if it does not exist.
    """
    try:
        # Establish raw MySQL connection
        connection = pymysql.connect(host=host, user=username, password=password)
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}`;")
        connection.commit()
        cursor.close()
        connection.close()
        print(f"Database '{database_name}' created or already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")

database_name = "vaccination_analysis"
create_database(database_name)


database_name = "vaccination_analysis"
create_database(database_name)

# Connect to the new database
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}")

# Create Tables
def create_tables():
    try:
        with engine.connect() as connection:
            connection.execute(text('''CREATE TABLE IF NOT EXISTS coverage_data (
                `GROUP` TEXT,
                `CODE` TEXT,
                `NAME` TEXT,
                `YEAR` DATE,
                `ANTIGEN` TEXT,
                `ANTIGEN_DESCRIPTION` TEXT,
                `COVERAGE_CATEGORY` TEXT,
                `COVERAGE_CATEGORY_DESCRIPTION` TEXT,
                `TARGET_NUMBER` INTEGER,
                `DOSES` INTEGER,
                `COVERAGE` REAL
            );'''))
            connection.execute(text('''CREATE TABLE IF NOT EXISTS incidence_rate (
                `GROUP` TEXT,
                `CODE` TEXT,
                `NAME` TEXT,
                `YEAR` DATE,
                `DISEASE` TEXT,
                `DISEASE_DESCRIPTION` TEXT,
                `DENOMINATOR` INTEGER,
                `INCIDENCE_RATE` REAL
            );'''))
            connection.execute(text('''CREATE TABLE IF NOT EXISTS reported_cases_data (
                `GROUP` TEXT,
                `CODE` TEXT,
                `NAME` TEXT,
                `YEAR` DATE,
                `DISEASE` TEXT,
                `DISEASE_DESCRIPTION` TEXT,
                `CASES` INTEGER
            );'''))
            connection.execute(text('''CREATE TABLE IF NOT EXISTS vaccine_intro_data (
                `ISO_3_CODE` TEXT,
                `COUNTRYNAME` TEXT,
                `WHO_REGION` TEXT,
                `YEAR` DATE,
                `DESCRIPTION` TEXT,
                `INTRO` DATE
            );'''))
            connection.execute(text('''CREATE TABLE IF NOT EXISTS vaccine_schedule_data (
                `ISO_3_CODE` TEXT,
                `COUNTRYNAME` TEXT,
                `WHO_REGION` TEXT,
                `YEAR` DATE,
                `VACCINECODE` TEXT,
                `VACCINE_DESCRIPTION` TEXT,
                `SCHEDULEROUNDS` TEXT,
                `TARGETPOP` INTEGER,
                `TARGETPOP_DESCRIPTION` TEXT,
                `GEOAREA` TEXT,
                `AGEADMINISTERED` TEXT,
                `SOURCECOMMENT` TEXT
            );'''))
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")

# Populate Tables
def populate_tables():
    try:
        coverage_data.to_sql('coverage_data', con=engine, if_exists='replace', index=False)
        incidence_data.to_sql('incidence_rate', con=engine, if_exists='replace', index=False)
        reported_cases_data.to_sql('reported_cases_data', con=engine, if_exists='replace', index=False)
        vaccine_intro_data.to_sql('vaccine_intro_data', con=engine, if_exists='replace', index=False)
        vaccine_schedule_data.to_sql('vaccine_schedule_data', con=engine, if_exists='replace', index=False)

        print("Data populated into tables successfully!")
    except Exception as e:
        print(f"Error populating tables: {e}")

create_tables()
populate_tables()

# Step 3: Exploratory Data Analysis (EDA)
def plot_vaccination_trends(df):
    """
    Plots vaccination trends over years.
    """
    if 'YEAR' not in df.columns or 'COVERAGE' not in df.columns or 'NAME' not in df.columns:
        print("Required columns for plotting are missing.")
        return

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='YEAR', y='COVERAGE', hue='NAME')
    plt.title('Vaccination Trends by Country')
    plt.xlabel('Year')
    plt.ylabel('Coverage (%)')
    plt.show()

plot_vaccination_trends(coverage_data)

# Correlation between vaccination and incidence
def correlate_vaccination_incidence(coverage_df, incidence_df):
    """
    Analyzes correlation between vaccination rates and disease incidence.
    """
    if 'COVERAGE' not in coverage_df.columns or 'INCIDENCE_RATE' not in incidence_df.columns:
        print("Required columns for correlation analysis are missing.")
        return

    merged_df = pd.merge(coverage_df, incidence_df, on=['CODE', 'YEAR'], how='inner')
    correlation = merged_df['COVERAGE'].corr(merged_df['INCIDENCE_RATE'])
    print(f"Correlation between vaccination coverage and disease incidence: {correlation}")

correlate_vaccination_incidence(coverage_data, incidence_data)