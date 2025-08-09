import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# --- Streamlit UI ---
st.set_page_config(
    page_title="Vehicle Registration Analytics", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🚗"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border-radius: 5px;
    }
    
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
    }
    
    .data-table {
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 600;
    }
    
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 2.5rem;">🚗 Vehicle Registration Analytics</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
        Comprehensive insights into vehicle registration trends across India
    </p>
</div>
""", unsafe_allow_html=True)

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

    # Enhanced Sidebar filters
    st.sidebar.markdown("### 🎛️ Filter Controls")
    st.sidebar.markdown("---")
    
    years = sorted(df['Year'].unique())
    categories = sorted(df['Vehicle Category'].unique())
    
    selected_years = st.sidebar.multiselect(
        "📅 Select Years", 
        years, 
        default=years,
        help="Choose the years you want to analyze"
    )
    
    selected_categories = st.sidebar.multiselect(
        "🚙 Select Vehicle Categories", 
        categories, 
        default=categories,
        help="Filter by vehicle types"
    )
    
    if manufacturers:
        selected_manufacturers = st.sidebar.multiselect(
            "🏭 Select Manufacturers", 
            manufacturers, 
            default=manufacturers[:10] if len(manufacturers) > 10 else manufacturers,
            help="Choose manufacturers to compare"
        )
    else:
        selected_manufacturers = []

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Dashboard Info")
    st.sidebar.info(f"""
    **Data Overview:**
    - Total Records: {len(df):,}
    - Date Range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}
    - States Covered: {df['State Name (state_name)'].nunique()}
    - Vehicle Categories: {len(categories)}
    """)

    filtered = df[
        df['Year'].isin(selected_years)
        & df['Vehicle Category'].isin(selected_categories)
        & (df['Manufacturer'].isin(selected_manufacturers) if manufacturers else True)
    ]

    # Key Metrics Section
    st.markdown("### 📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_registrations = filtered['Registrations'].sum()
    avg_registrations = filtered['Registrations'].mean()
    unique_states = filtered['State Name (state_name)'].nunique()
    unique_rtos = filtered['RTO Name (office_name)'].nunique()
    
    with col1:
        st.metric(
            label="Total Registrations",
            value=f"{total_registrations:,.0f}",
            delta=f"{(total_registrations/1000000):.1f}M vehicles"
        )
    
    with col2:
        st.metric(
            label="Average per Record",
            value=f"{avg_registrations:,.0f}",
            delta="Per registration entry"
        )
    
    with col3:
        st.metric(
            label="States Covered",
            value=f"{unique_states}",
            delta="Across India"
        )
    
    with col4:
        st.metric(
            label="RTO Offices",
            value=f"{unique_rtos}",
            delta="Registration offices"
        )

    st.markdown("---")

    # Data Table Section
    if manufacturers:
        agg = filtered.groupby(['Year', 'Vehicle Category', 'Manufacturer'], as_index=False)['Registrations'].sum()
    else:
        agg = filtered.groupby(['Year', 'Vehicle Category'], as_index=False)['Registrations'].sum()
    
    st.markdown("### 📋 Registration Summary Table")
    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    st.dataframe(
        agg.style.format({'Registrations': '{:,.0f}'}),
        use_container_width=True,
        height=400
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Enhanced Trend Graphs
    st.markdown("### 📊 Registration Trends Analysis")
    
    # Vehicle Category Trends
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### 🚙 Registrations by Vehicle Category")
    
    fig = px.bar(
        agg, 
        x='Year', 
        y='Registrations', 
        color='Vehicle Category',
        barmode='group',
        title="Vehicle Registration Trends by Category",
        color_discrete_sequence=px.colors.qualitative.Set3,
        hover_data={'Registrations': ':,.0f'}
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12),
        title_font_size=16,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Manufacturer Trends
    if manufacturers:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 🏭 Registrations by Manufacturer")
        
        # Top manufacturers only for better visualization
        top_manufacturers = agg.groupby('Manufacturer')['Registrations'].sum().nlargest(10).index
        agg_top = agg[agg['Manufacturer'].isin(top_manufacturers)]
        
        figm = px.bar(
            agg_top, 
            x='Year', 
            y='Registrations', 
            color='Manufacturer',
            barmode='group',
            title="Top 10 Manufacturers - Registration Trends",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hover_data={'Registrations': ':,.0f'}
        )
        
        figm.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12),
            title_font_size=16,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode='x unified'
        )
        
        figm.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        figm.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        
        st.plotly_chart(figm, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Enhanced YoY Growth Calculation
    st.markdown("### 📈 Growth Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 📊 Year-over-Year (YoY) Growth")
        
        if manufacturers:
            agg = agg.sort_values(['Manufacturer', 'Vehicle Category', 'Year'])
            agg['Prev_Registrations'] = agg.groupby(['Manufacturer', 'Vehicle Category'])['Registrations'].shift(1)
            agg['YoY_Growth_%'] = ((agg['Registrations'] - agg['Prev_Registrations']) / agg['Prev_Registrations'] * 100).round(2)
            
            # Show top performers
            yoy_display = agg[['Year', 'Vehicle Category', 'Manufacturer', 'Registrations', 'YoY_Growth_%']].dropna()
            st.dataframe(
                yoy_display.style.format({
                    'Registrations': '{:,.0f}',
                    'YoY_Growth_%': '{:.1f}%'
                }).background_gradient(subset=['YoY_Growth_%'], cmap='RdYlGn'),
                use_container_width=True,
                height=300
            )
            
            # Growth trend chart
            fig2 = px.line(
                agg.dropna(), 
                x='Year', 
                y='YoY_Growth_%', 
                color='Manufacturer', 
                line_dash='Vehicle Category',
                markers=True,
                title="YoY Growth Trends by Manufacturer",
                hover_data={'YoY_Growth_%': ':.1f%'}
            )
        else:
            agg = agg.sort_values(['Vehicle Category', 'Year'])
            agg['Prev_Registrations'] = agg.groupby('Vehicle Category')['Registrations'].shift(1)
            agg['YoY_Growth_%'] = ((agg['Registrations'] - agg['Prev_Registrations']) / agg['Prev_Registrations'] * 100).round(2)
            
            yoy_display = agg[['Year', 'Vehicle Category', 'Registrations', 'YoY_Growth_%']].dropna()
            st.dataframe(
                yoy_display.style.format({
                    'Registrations': '{:,.0f}',
                    'YoY_Growth_%': '{:.1f}%'
                }).background_gradient(subset=['YoY_Growth_%'], cmap='RdYlGn'),
                use_container_width=True,
                height=300
            )
            
            fig2 = px.line(
                agg.dropna(), 
                x='Year', 
                y='YoY_Growth_%', 
                color='Vehicle Category',
                markers=True,
                title="YoY Growth Trends by Vehicle Category",
                hover_data={'YoY_Growth_%': ':.1f%'}
            )
        
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12),
            title_font_size=14,
            hovermode='x unified'
        )
        fig2.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        fig2.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 📊 Quarter-over-Quarter (QoQ) Growth")
        
        if manufacturers:
            agg_q = filtered.groupby(['Quarter', 'Vehicle Category', 'Manufacturer'], as_index=False)['Registrations'].sum()
            agg_q = agg_q.sort_values(['Manufacturer', 'Vehicle Category', 'Quarter'])
            agg_q['Prev_Registrations'] = agg_q.groupby(['Manufacturer', 'Vehicle Category'])['Registrations'].shift(1)
            agg_q['QoQ_Growth_%'] = ((agg_q['Registrations'] - agg_q['Prev_Registrations']) / agg_q['Prev_Registrations'] * 100).round(2)
            
            qoq_display = agg_q[['Quarter', 'Vehicle Category', 'Manufacturer', 'Registrations', 'QoQ_Growth_%']].dropna()
            st.dataframe(
                qoq_display.style.format({
                    'Registrations': '{:,.0f}',
                    'QoQ_Growth_%': '{:.1f}%'
                }).background_gradient(subset=['QoQ_Growth_%'], cmap='RdYlBu'),
                use_container_width=True,
                height=300
            )
            
            fig3 = px.line(
                agg_q.dropna(), 
                x='Quarter', 
                y='QoQ_Growth_%', 
                color='Manufacturer', 
                line_dash='Vehicle Category',
                markers=True,
                title="QoQ Growth Trends by Manufacturer",
                hover_data={'QoQ_Growth_%': ':.1f%'}
            )
        else:
            agg_q = filtered.groupby(['Quarter', 'Vehicle Category'], as_index=False)['Registrations'].sum()
            agg_q = agg_q.sort_values(['Vehicle Category', 'Quarter'])
            agg_q['Prev_Registrations'] = agg_q.groupby('Vehicle Category')['Registrations'].shift(1)
            agg_q['QoQ_Growth_%'] = ((agg_q['Registrations'] - agg_q['Prev_Registrations']) / agg_q['Prev_Registrations'] * 100).round(2)
            
            qoq_display = agg_q[['Quarter', 'Vehicle Category', 'Registrations', 'QoQ_Growth_%']].dropna()
            st.dataframe(
                qoq_display.style.format({
                    'Registrations': '{:,.0f}',
                    'QoQ_Growth_%': '{:.1f}%'
                }).background_gradient(subset=['QoQ_Growth_%'], cmap='RdYlBu'),
                use_container_width=True,
                height=300
            )
            
            fig3 = px.line(
                agg_q.dropna(), 
                x='Quarter', 
                y='QoQ_Growth_%', 
                color='Vehicle Category',
                markers=True,
                title="QoQ Growth Trends by Vehicle Category",
                hover_data={'QoQ_Growth_%': ':.1f%'}
            )
        
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12),
            title_font_size=14,
            hovermode='x unified'
        )
        fig3.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)', tickangle=45)
        fig3.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
        
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Additional Insights Section
    st.markdown("---")
    st.markdown("### 🎯 Market Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 🏆 Top Performing States")
        
        state_summary = filtered.groupby('State Name (state_name)')['Registrations'].sum().nlargest(10)
        
        fig_states = px.bar(
            x=state_summary.values,
            y=state_summary.index,
            orientation='h',
            title="Top 10 States by Total Registrations",
            color=state_summary.values,
            color_continuous_scale='viridis'
        )
        
        fig_states.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12),
            title_font_size=14,
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig_states, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 📊 Vehicle Category Distribution")
        
        category_dist = filtered.groupby('Vehicle Category')['Registrations'].sum()
        
        fig_pie = px.pie(
            values=category_dist.values,
            names=category_dist.index,
            title="Market Share by Vehicle Category",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12),
            title_font_size=14,
            height=400
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px; margin-top: 2rem;">
        <p style="margin: 0; color: #6c757d;">
            📊 Vehicle Registration Analytics Dashboard | 
            Data Source: <a href="https://vahan.parivahan.gov.in/vahan4dashboard/" target="_blank">Vahan Dashboard</a> | 
            Built with ❤️ using Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: #fff3cd; border-radius: 10px; border-left: 4px solid #ffc107;">
        <h3 style="color: #856404;">⚠️ Data Not Found</h3>
        <p style="color: #856404; margin: 1rem 0;">
            Please add the required data CSV file in the project root or data folder to get started.
        </p>
        <p style="color: #856404; font-size: 0.9rem;">
            Expected file: <code>VAHAN_Vehicle_Registrations_with_Manufacturer.csv</code>
        </p>
    </div>
    """, unsafe_allow_html=True)
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
