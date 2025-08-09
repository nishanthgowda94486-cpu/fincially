import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def fetch_vahan_data(year=2025, vehicle_type='FOUR WHEELER'):
    """
    Scrapes vehicle class-wise data for a given year and vehicle type from Vahan Dashboard.
    Returns a DataFrame.
    """
    # NOTE: The Vahan Dashboard uses dynamic JS and POST requests, so this is a placeholder for manual download or advanced scraping.
    # For demo, load from screenshot or manually downloaded CSV.
    # Replace this with actual scraping logic if possible.
    file_path = os.path.join('data', f'vehicle_data_{year}_{vehicle_type.replace(" ", "_")}.csv')
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"Please download the data for {year} - {vehicle_type} and save as {file_path}")
        return pd.DataFrame()

if __name__ == "__main__":
    # Example usage
    df = fetch_vahan_data()
    print(df.head())
