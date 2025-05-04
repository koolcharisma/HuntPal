# app.py
import streamlit as st
import importlib, inspect
from pathlib import Path

# —— 1. Load API keys ——
openai_key = st.secrets["OPENAI_API_KEY"]
serpapi_key = st.secrets["SERPAPI_KEY"]

st.title("Company Research Assistant")

# —— 2. Load or create research_models.py if missing ——
models_path = Path("research_models.py")
if not models_path.exists():
    models_path.write_text(
        "# your research logic goes here\n"
        "def run_research(company, openai_key, serpapi_key):\n"
        "    # TODO: implement multi-prompt flows\n"
        "    return {'overview': '…', 'headlines': []}\n"
    )

# —— 3. Show an editor for the research_models.py source ——
st.sidebar.header("⚙️ Edit Research Models")
source_code = models_path.read_text()
edited = st.sidebar.text_area(
    "research_models.py", source_code, height=400
)
if st.sidebar.button("Save & Reload"):
    models_path.write_text(edited)
    importlib.invalidate_caches()
    import research_models
    importlib.reload(research_models)
    st.sidebar.success("Reloaded!")

# —— 4. Main UI: run research —— 
company = st.text_input("Enter a company name", placeholder="e.g. Acme Corp")
if st.button("Run Research") and company:
    import research_models
    results = research_models.run_research(company, openai_key, serpapi_key)

    st.subheader("Top News Headlines")
    for idx, h in enumerate(results.get("headlines", []), 1):
        st.write(f"{idx}. {h}")

    st.subheader("AI‑Generated Overview")
    st.write(results.get("overview", "No overview returned."))
