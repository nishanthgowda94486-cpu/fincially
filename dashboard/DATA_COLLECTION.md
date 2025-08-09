# Data Collection Instructions

1. Visit the Vahan Dashboard: https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml
2. Select the required filters (Year, Vehicle Type, etc.)
3. Download or manually copy the table data for each year and vehicle type.
4. Save each dataset as a CSV file in the `data/` folder, named as:
   - `vehicle_data_<YEAR>_<VEHICLE_TYPE>.csv`
   - Example: `vehicle_data_2025_FOUR_WHEELER.csv`
5. Repeat for all years and vehicle types needed for analysis.

# Notes
- The dashboard currently uses static CSVs for demo. For production, implement automated scraping or API integration.
- Document any manual steps or scripts used for data collection.
