import streamlit as st
import eurostat
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="EU Renewables Top 10", page_icon="🏆", layout="wide")

st.title("🏆 European Renewable Energy: Top 10 Tracker")

# --- DATA FETCHING (Cached) ---
@st.cache_data
def get_eurostat_data():
    # 'nrg_ind_ren' = Share of energy from renewable sources
    code = 'nrg_ind_ren'
    df = eurostat.get_data_df(code)
    # Rename country column to standard 'Country'
    df.rename(columns={col: 'Country' for col in df.columns if 'geo' in col.lower()}, inplace=True)
    return df

# --- HELPER: Identify Aggregates vs Countries ---
AGGREGATES = [
    'EU27_2020', 'EU28', 'EA19', 'EA20', 'EU27_2007', 'EU15', 'EA', 'BA', 'XK'
]

try:
    with st.spinner("Fetching data for all countries..."):
        raw_df = get_eurostat_data()

    # --- DATA CLEANING ---
    year_cols = [col for col in raw_df.columns if str(col).isdigit()]
    df = raw_df.melt(
        id_vars=['unit', 'nrg_bal', 'Country'], 
        value_vars=year_cols,
        var_name='Year',
        value_name='Value'
    )
    
    df['Year'] = df['Year'].astype(int)
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    df.dropna(subset=['Value'], inplace=True)

    SECTOR_MAP = {
        'REN': 'Overall Share',
        'REN_ELC': 'Electricity Only',
        'REN_TRA': 'Transport',
        'REN_HEAT_CL': 'Heating & Cooling'
    }
    df = df[df['nrg_bal'].isin(SECTOR_MAP.keys())]
    df['Sector'] = df['nrg_bal'].map(SECTOR_MAP)

    # --- SIDEBAR CONTROLS ---
    st.sidebar.header("Filter Options")
    selected_sector = st.sidebar.selectbox("Select Energy Sector", list(SECTOR_MAP.values()))

    # --- MAIN LOGIC ---
    sector_df = df[df['Sector'] == selected_sector]
    latest_year = sector_df['Year'].max()
    latest_df = sector_df[sector_df['Year'] == latest_year].copy()
    
    # Filter out aggregates to get only countries
    countries_only_df = latest_df[~latest_df['Country'].isin(AGGREGATES)]
    
    # Get Top 10
    top_10_df = countries_only_df.sort_values(by='Value', ascending=False).head(10)

    # --- VISUALIZATIONS ---
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"🥇 Top 10 Countries in {latest_year}")
        fig_bar = px.bar(
            top_10_df,
            x="Country",
            y="Value",
            color="Country",
            text="Value",
            title=f"Top 10 Performers ({selected_sector})",
            labels={"Value": "% Share"},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("📋 Leaderboard")
        display_table = top_10_df[['Country', 'Value']].reset_index(drop=True)
        display_table.index += 1 
        st.dataframe(display_table, use_container_width=True)

    # --- TRENDS ---
    st.divider()
    st.subheader(f"📈 History of the Top 5")
    top_5_codes = top_10_df['Country'].head(5).tolist()
    trend_df = sector_df[sector_df['Country'].isin(top_5_codes)]
    
    fig_line = px.line(
        trend_df, x="Year", y="Value", color="Country", markers=True
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # --- RAW DATA SECTION (RESTORED) ---
    st.divider()
    with st.expander("📂 View Full Raw Data (All Countries & Years)"):
        st.markdown(f"**Full Dataset for sector: {selected_sector}**")
        st.write("You can sort and search this table.")
        
        # Show the full dataset for this sector, sorted by Year (desc) then Country
        full_table = sector_df.sort_values(by=['Year', 'Country'], ascending=[False, True])
        st.dataframe(full_table, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")
