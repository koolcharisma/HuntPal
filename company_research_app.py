import streamlit as st
import logging
import openai

# —— 0) Runtime dependency check ——
try:
    from serpapi import GoogleSearch
    st.success("✅ GoogleSearch is available")
except ImportError:
    st.error("🔴 GoogleSearch NOT found—ensure 'google-search-results' is in requirements.txt")
    st.stop()

# —— 1) SerpAPI function ——
def fetch_headlines(company: str, serpapi_key: str, num: int = 3) -> list[str]:
    """Return top news headlines for a company via SerpAPI (Google News)."""
    if not serpapi_key:
        raise ValueError("SERPAPI_KEY is missing!")
    params = {
        "engine": "google",   # use Google engine
        "tbm": "nws",         # news tab
        "q": company,
        "api_key": serpapi_key,
        "num": num
    }
    search = GoogleSearch(params)
    data = search.get_dict()
    news = data.get("news_results", [])
    return [item.get("title", "") for item in news], data

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

if not openai_key:
    st.error("Missing OPENAI_API_KEY—check secrets")
    st.stop()
if not serpapi_key:
    st.error("Missing SERPAPI_KEY—check secrets")
    st.stop()

# —— 4) Streamlit UI ——
st.title("Company Research Assistant")
company = st.text_input("Enter a company name", placeholder="e.g. Acme Corp")

col1, col2 = st.columns(2)
with col1:
    if st.button("Get News Headlines") and company:
        try:
            headlines, raw = fetch_headlines(company, serpapi_key)
            if headlines:
                st.subheader("News Headlines")
                for i, h in enumerate(headlines, 1):
                    st.write(f"{i}. {h}")
            else:
                st.warning("No headlines found.")
                st.subheader("Raw SerpAPI response")
                st.json(raw)
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
