import streamlit as st
import logging
import importlib
from pathlib import Path

# —— Load API keys ——
openai_key  = st.secrets.get("OPENAI_API_KEY")
serpapi_key = st.secrets.get("SERPAPI_KEY")

# —— Logging & feedback ——
if openai_key:
    logging.info("✅ OPENAI_API_KEY loaded successfully.")
else:
    logging.error("❌ OPENAI_API_KEY is missing!")

if serpapi_key:
    logging.info("✅ SERPAPI_KEY loaded successfully.")
else:
    logging.error("❌ SERPAPI_KEY is missing!")

if openai_key and serpapi_key:
    st.success("All API keys successfully loaded from secrets.toml!")
else:
    if not openai_key:
        st.error("Missing OPENAI_API_KEY in secrets.toml.")
    if not serpapi_key:
        st.error("Missing SERPAPI_KEY in secrets.toml.")
    st.stop()

# —— Define SerpAPI functions ——
def fetch_headlines(company: str, api_key: str, num: int = 3) -> list[str]:
    """
    Fetch top news headlines for a company using SerpAPI.
    """
    from serpapi import GoogleSearch

    params = {
        "engine": "google_news",
        "q": company,
        "api_key": api_key,
        "num": num
    }
    search = GoogleSearch(params)
    data = search.get_dict()
    headlines = [item.get("title", "") for item in data.get("news_results", [])]
    return headlines

# —— Define OpenAI functions ——
def generate_overview(company: str, api_key: str, engine: str = "text-davinci-003") -> str:
    """
    Generate a concise company overview using OpenAI.
    """
    import openai
    openai.api_key = api_key

    prompt = (
        f"Provide a concise overview of {company}, including its industry, headquarters, and recent news highlights."
    )
    resp = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=200
    )
    return resp.choices[0].text.strip()

# —— Sidebar: Edit research_models.py (optional) ——
models_path = Path("research_models.py")
if not models_path.exists():
    models_path.write_text(
        "# Move custom multi-prompt logic here\n"
        "def run_research(company, openai_key, serpapi_key):\n"
        "    # Example combining fetch_headlines + generate_overview\n"
        "    return {\"headlines\": fetch_headlines(company, serpapi_key), \"overview\": generate_overview(company, openai_key)}\n"
    )
st.sidebar.header("⚙️ Edit Research Models")
source_code = models_path.read_text()
edited = st.sidebar.text_area("research_models.py", source_code, height=300)
if st.sidebar.button("Save & Reload"):
    models_path.write_text(edited)
    importlib.invalidate_caches()
    import research_models
    importlib.reload(research_models)
    st.sidebar.success("Reloaded!")

# —— Main UI ——
st.title("Company Research Assistant")
company = st.text_input("Enter a company name", placeholder="e.g. Acme Corp")
if st.button("Fetch Headlines") and company:
    headlines = fetch_headlines(company, serpapi_key)
    st.subheader("Top News Headlines")
    for idx, h in enumerate(headlines, 1):
        st.write(f"{idx}. {h}")

if st.button("Generate Overview") and company:
    overview = generate_overview(company, openai_key)
    st.subheader("AI‑Generated Overview")
    st.write(overview)
