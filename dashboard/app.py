import streamlit as st
import pandas as pd
import plotly.express as px


# --- Streamlit UI ---
st.set_page_config(page_title="Vehicle Registration Dashboard", layout="wide")
st.title("Vehicle Registration Dashboard")

# --- Data Loading ---
@st.cache_data
def load_main_csv():
    import os
    # Try manufacturer file first
    manu_path = "../VAHAN_Vehicle_Registrations_with_Manufacturer.csv"
    manu_alt = "data/VAHAN_Vehicle_Registrations_with_Manufacturer.csv"
    manu_local = "VAHAN_Vehicle_Registrations_with_Manufacturer.csv"
    if os.path.exists(manu_path):
        return pd.read_csv(manu_path)
    elif os.path.exists(manu_alt):
        return pd.read_csv(manu_alt)
    elif os.path.exists(manu_local):
        return pd.read_csv(manu_local)
    # Fallback to old sample file
    file_path = "../VAHAN Vehicle Registrations by Vehicle Category_Sample_Data.csv"
    alt_path = "data/VAHAN Vehicle Registrations by Vehicle Category_Sample_Data.csv"
    local_path = "VAHAN Vehicle Registrations by Vehicle Category_Sample_Data.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    elif os.path.exists(alt_path):
        return pd.read_csv(alt_path)
    elif os.path.exists(local_path):
        return pd.read_csv(local_path)
    else:
        st.error("Sample data CSV not found. Please place it in the project root or data folder.")
        return pd.DataFrame()

df = load_main_csv()

if not df.empty:
    # Preprocess
    df['Date'] = pd.to_datetime(df['Date (date)'])
    df['Year'] = df['Date'].dt.year
    df['Quarter'] = df['Date'].dt.to_period('Q').astype(str)
    df['Vehicle Category'] = df['Vehicle Category (vehicle_type)']
    df['Registrations'] = pd.to_numeric(df['Registrations (registrations)'], errors='coerce')
    if 'Manufacturer' in df.columns:
        df['Manufacturer'] = df['Manufacturer'].astype(str)
        manufacturers = sorted(df['Manufacturer'].unique())
    else:
        manufacturers = []

    # Sidebar filters
    years = sorted(df['Year'].unique())
    categories = sorted(df['Vehicle Category'].unique())
    selected_years = st.sidebar.multiselect("Select Years", years, default=years)
    selected_categories = st.sidebar.multiselect("Select Vehicle Category", categories, default=categories)
    if manufacturers:
        selected_manufacturers = st.sidebar.multiselect("Select Manufacturer", manufacturers, default=manufacturers)
    else:
        selected_manufacturers = []

    filtered = df[
        df['Year'].isin(selected_years)
        & df['Vehicle Category'].isin(selected_categories)
        & (df['Manufacturer'].isin(selected_manufacturers) if manufacturers else True)
    ]

    # Aggregate by year, category, and manufacturer
    st.subheader("Total Registrations by Year, Vehicle Category, and Manufacturer")
    if manufacturers:
        agg = filtered.groupby(['Year', 'Vehicle Category', 'Manufacturer'], as_index=False)['Registrations'].sum()
    else:
        agg = filtered.groupby(['Year', 'Vehicle Category'], as_index=False)['Registrations'].sum()
    st.dataframe(agg)

    # Trend Graphs
    st.subheader("Trend by Vehicle Category (Total Registered)")
    fig = px.bar(agg, x='Year', y='Registrations', color='Vehicle Category', barmode='group', text='Registrations')
    st.plotly_chart(fig, use_container_width=True)
    if manufacturers:
        st.subheader("Trend by Manufacturer (Total Registered)")
        figm = px.bar(agg, x='Year', y='Registrations', color='Manufacturer', barmode='group', text='Registrations')
        st.plotly_chart(figm, use_container_width=True)

    # YoY Growth Calculation
    st.subheader("Year-over-Year (YoY) Growth")
    if manufacturers:
        agg = agg.sort_values(['Manufacturer', 'Vehicle Category', 'Year'])
        agg['Prev_Registrations'] = agg.groupby(['Manufacturer', 'Vehicle Category'])['Registrations'].shift(1)
        agg['YoY_Growth_%'] = ((agg['Registrations'] - agg['Prev_Registrations']) / agg['Prev_Registrations'] * 100).round(2)
        st.dataframe(agg[['Year', 'Vehicle Category', 'Manufacturer', 'Registrations', 'YoY_Growth_%']])
        fig2 = px.line(agg, x='Year', y='YoY_Growth_%', color='Manufacturer', line_dash='Vehicle Category', markers=True)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        agg = agg.sort_values(['Vehicle Category', 'Year'])
        agg['Prev_Registrations'] = agg.groupby('Vehicle Category')['Registrations'].shift(1)
        agg['YoY_Growth_%'] = ((agg['Registrations'] - agg['Prev_Registrations']) / agg['Prev_Registrations'] * 100).round(2)
        st.dataframe(agg[['Year', 'Vehicle Category', 'Registrations', 'YoY_Growth_%']])
        fig2 = px.line(agg, x='Year', y='YoY_Growth_%', color='Vehicle Category', markers=True)
        st.plotly_chart(fig2, use_container_width=True)

    # QoQ Growth Calculation
    st.subheader("Quarter-over-Quarter (QoQ) Growth")
    if manufacturers:
        agg_q = filtered.groupby(['Quarter', 'Vehicle Category', 'Manufacturer'], as_index=False)['Registrations'].sum()
        agg_q = agg_q.sort_values(['Manufacturer', 'Vehicle Category', 'Quarter'])
        agg_q['Prev_Registrations'] = agg_q.groupby(['Manufacturer', 'Vehicle Category'])['Registrations'].shift(1)
        agg_q['QoQ_Growth_%'] = ((agg_q['Registrations'] - agg_q['Prev_Registrations']) / agg_q['Prev_Registrations'] * 100).round(2)
        st.dataframe(agg_q[['Quarter', 'Vehicle Category', 'Manufacturer', 'Registrations', 'QoQ_Growth_%']])
        fig3 = px.line(agg_q, x='Quarter', y='QoQ_Growth_%', color='Manufacturer', line_dash='Vehicle Category', markers=True)
        st.plotly_chart(fig3, use_container_width=True)
    else:
        agg_q = filtered.groupby(['Quarter', 'Vehicle Category'], as_index=False)['Registrations'].sum()
        agg_q = agg_q.sort_values(['Vehicle Category', 'Quarter'])
        agg_q['Prev_Registrations'] = agg_q.groupby('Vehicle Category')['Registrations'].shift(1)
        agg_q['QoQ_Growth_%'] = ((agg_q['Registrations'] - agg_q['Prev_Registrations']) / agg_q['Prev_Registrations'] * 100).round(2)
        st.dataframe(agg_q[['Quarter', 'Vehicle Category', 'Registrations', 'QoQ_Growth_%']])
        fig3 = px.line(agg_q, x='Quarter', y='QoQ_Growth_%', color='Vehicle Category', markers=True)
        st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Please add the required data CSV in the project root or data folder.")
