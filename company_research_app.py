import streamlit as st
import logging
import importlib.util
from serpapi import GoogleSearch
import openai

# —— 0) Runtime dependency check ——
if importlib.util.find_spec("serpapi.GoogleSearch") is None:
    st.error("🔴 GoogleSearch NOT found—ensure 'google-search-results' is in requirements.txt")
else:
    st.success("✅ GoogleSearch is available")

# —— 1) SerpAPI function ——
def fetch_headlines(company: str, serpapi_key: str, num: int = 3) -> list[str]:
    """Return top news headlines for a company via SerpAPI."""
    if not serpapi_key:
        raise ValueError("SERPAPI_KEY is missing!")
    params = {"engine": "google_news", "q": company, "api_key": serpapi_key, "num": num}
    search = GoogleSearch(params)
    data = search.get_dict()
    return [item.get("title", "") for item in data.get("news_results", [])]

# —— 2) OpenAI function ——
def generate_overview(company: str, openai_key: str) -> str:
    """Return a concise company overview via OpenAI."""
    if not openai_key:
        raise ValueError("OPENAI_API_KEY is missing!")
    openai.api_key = openai_key
    prompt = f"""
Provide a concise overview of {company}, including:
- Industry
- Headquarters
- Recent news highlights
"""
    resp = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200
    )
    return resp.choices[0].text.strip()

# —— 3) Load keys & logging ——
openai_key = st.secrets.get("OPENAI_API_KEY")
serpapi_key = st.secrets.get("SERPAPI_KEY")

if openai_key:
    logging.info("✅ OPENAI_API_KEY loaded")
else:
    logging.error("❌ OPENAI_API_KEY missing")

if serpapi_key:
    logging.info("✅ SERPAPI_KEY loaded")
else:
    logging.error("❌ SERPAPI_KEY missing")
    st.error("Missing SERPAPI_KEY—check secrets")
    st.stop()

# —— 4) Streamlit UI ——
st.title("Company Research Assistant")
company = st.text_input("Enter a company name", placeholder="e.g. Acme Corp")

col1, col2 = st.columns(2)
with col1:
    if st.button("Get News Headlines") and company:
        try:
            headlines = fetch_headlines(company, serpapi_key)
            st.subheader("News Headlines")
            for i, h in enumerate(headlines, 1):
                st.write(f"{i}. {h}")
        except Exception as e:
            st.error(f"Error fetching headlines: {e}")

with col2:
    if st.button("Get AI Overview") and company:
        try:
            overview = generate_overview(company, openai_key)
            st.subheader("AI‑Generated Overview")
            st.write(overview)
        except Exception as e:
            st.error(f"Error generating overview: {e}")
