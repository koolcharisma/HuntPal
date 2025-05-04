import streamlit as st
from serpapi import GoogleSearch
import openai

# —— 1. Load API keys from Streamlit secrets —— 
openai.api_key = st.secrets["OPENAI_API_KEY"]
SERPAPI_KEY = st.secrets["SERPAPI_KEY"]

# —— 2. UI: Company name input & button —— 
st.title("Company Research Assistant")
company = st.text_input("Enter a company name", placeholder="e.g. Acme Corp")
if st.button("Run Research") and company:

    # —— 3. SerpAPI: fetch top 3 news headlines —— 
    params = {
        "engine": "google_news",
        "q": company,
        "api_key": SERPAPI_KEY,
        "num": 3
    }
    search = GoogleSearch(params)
    results = search.get_dict().get("news_results", [])
    headlines = [n["title"] for n in results]

    st.subheader("Top News Headlines")
    for idx, h in enumerate(headlines, 1):
        st.write(f"{idx}. {h}")

    # —— 4. OpenAI: generate company overview —— 
    prompt = (
        f"Provide a concise overview of {company}, "
        "including its industry, headquarters, and recent news highlights."
    )
    resp = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200
    )
    overview = resp.choices[0].text.strip()

    st.subheader("AI‑Generated Overview")
    st.write(overview)
