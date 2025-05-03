import streamlit as st

st.title("Company Research Assistant")

# Load API keys from secrets
openai_key = st.secrets["OPENAI_API_KEY"]
serpapi_key = st.secrets["SERPAPI_KEY"]

st.write("✅ API keys successfully loaded from secrets.toml.")