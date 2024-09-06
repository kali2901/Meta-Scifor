# Import necessary libraries
import os
import kaggle
import pandas as pd
import matplotlib.pyplot as plt

# Ensure Kaggle API is authenticated (this will work if you set up kaggle.json properly)
api = kaggle.api

# Download dataset from Kaggle
# Replace with the correct Kaggle dataset URL/ID
dataset = 'gpreda/covid-world-vaccination-progress'

# Define the directory to save the dataset
dataset_dir = 'datasets'
if not os.path.exists(dataset_dir):
    os.makedirs(dataset_dir)

# Download the dataset
api.dataset_download_files(dataset, path=dataset_dir, unzip=True)

# Load the dataset
csv_file_path = os.path.join(dataset_dir, 'country_vaccinations.csv')
df = pd.read_csv(csv_file_path)

# Basic data exploration
print(df.info())  # View dataset structure
print(df.head())  # Display first few rows

# --- Data Cleaning ---
# Check for missing values
print("\nMissing values before cleaning:")
print(df.isnull().sum())

# Drop rows with missing values in important columns (optional)
df_cleaned = df.dropna(subset=['total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated'])

# Fill missing values for other columns with suitable default values (e.g., 0)
df_cleaned.fillna(0, inplace=True)

# Check for missing values after cleaning
print("\nMissing values after cleaning:")
print(df_cleaned.isnull().sum())

# --- Data Analysis & Visualization ---
# Group by country and get the latest vaccination data
latest_data = df_cleaned.groupby('country').last().reset_index()

# Plot the top 10 countries with the highest total vaccinations
top_countries = latest_data.nlargest(10, 'total_vaccinations')
plt.figure(figsize=(10, 6))
plt.barh(top_countries['country'], top_countries['total_vaccinations'], color='skyblue')
plt.xlabel('Total Vaccinations')
plt.title('Top 10 Countries with Highest Total Vaccinations')
plt.gca().invert_yaxis()  # Invert y-axis to show the largest at the top
plt.show()

# Plot total vaccinations over time for a specific country
country = 'India'  # Change to any country you want to analyze
df_country = df_cleaned[df_cleaned['country'] == country]
plt.figure(figsize=(10, 6))
plt.plot(df_country['date'], df_country['total_vaccinations'], label='Total Vaccinations')
plt.plot(df_country['date'], df_country['people_vaccinated'], label='People Vaccinated')
plt.plot(df_country['date'], df_country['people_fully_vaccinated'], label='Fully Vaccinated')
plt.xlabel('Date')
plt.ylabel('Number of Vaccinations')
plt.title(f'Vaccination Progress Over Time in {country}')
plt.legend()
plt.xticks(rotation=45)
plt.show()
