
# Vehicle Registration Dashboard 🚗📊

Welcome! This project is an interactive dashboard for exploring and analyzing vehicle registration data, designed for both investors and data enthusiasts. Built with Streamlit, it lets you visualize trends, filter by manufacturer or category, and gain insights from real registration data.

---

## 🚀 Quick Start

1. **Clone or Download the Repository**
   ```sh
   git clone <repository-url>
   cd fincially
   ```

2. **Install Requirements**
   Make sure you have Python 3.10+ installed. Then run:
   ```sh
   python -m pip install -r dashboard/requirements.txt
   ```

3. **Run the Dashboard**
   ```sh
   streamlit run dashboard/app.py
   ```
   Streamlit will show a local URL (like http://localhost:8501). Open it in your browser to use the dashboard!

---

## 📂 Data Files
- Place your vehicle data CSV files in the `dashboard/data/` folder.
- Example files:
  - `vehicle_data_2023_FOUR_WHEELER.csv`
  - `vehicle_data_2024_FOUR_WHEELER.csv`
  - `vehicle_data_2025_FOUR_WHEELER.csv`

## 🛠 Features
- Year-over-Year (YoY) and Quarter-over-Quarter (QoQ) growth for vehicle categories and manufacturers
- Date range selection
- Filters by vehicle category and manufacturer
- Trend graphs and % change visualizations
- Interactive charts and tables (Plotly, Pandas)

## 📑 Data Source
- Data is scraped or downloaded from the [Vahan Dashboard](https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml)
- Data is stored in the `dashboard/data/` folder as CSV files.

## 🧰 Additional Scripts
- `dashboard/scraper.py`: Utilities for scraping and collecting vehicle data.

## 🗺️ Feature Roadmap
- Automated data scraping
- More granular filtering (state, RTO)
- Export graphs and tables

## ❓ Troubleshooting
- If you see missing package errors, make sure you installed all dependencies with the correct Python version.
- For any issues, check the terminal output for details.

## 🎥 Video Walkthrough
- [Add your video link here]

## 💡 Investment Insights
- [Add your insights here after analysis]

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## 📄 License
This project is licensed under the MIT License.
