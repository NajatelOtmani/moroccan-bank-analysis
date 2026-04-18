import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Moroccan Bank Analytics", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("cleaned_bank_data.csv")

df = load_data()

st.title("🇲🇦 Moroccan Banking Sector Sentiment Analysis")
st.sidebar.header("User Filters")

# Sidebar - Bank Selection
banks = st.sidebar.multiselect("Select Banks", options=df['Business Name'].unique(), default=df['Business Name'].unique()[:5])
# Sidebar - City Selection
cities = st.sidebar.multiselect("Select Cities", options=df['City'].unique(), default=df['City'].unique()[:5])

filtered_df = df[(df['Business Name'].isin(banks)) & (df['City'].isin(cities))]

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Reviews", len(filtered_df))
col2.metric("Avg Rating", f"{filtered_df['Stars'].mean():.2f} ⭐")
col3.metric("Positive %", f"{(filtered_df['sentiment'] == 'positive').mean()*100:.1f}%")

# Main Plot
st.subheader("Ratings over the Years")
ts_fig = px.line(filtered_df.groupby(['Year', 'Business Name'])['Stars'].mean().reset_index(), 
                 x='Year', y='Stars', color='Business Name')
st.plotly_chart(ts_fig, use_container_width=True)