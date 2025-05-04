# app.py

import streamlit as st
import importlib
from pathlib import Path
import logging

# ── 1. Configure logging ──────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

# ── 2. Load and validate API keys ─────────────────────────────────────────────
openai_key  = st.secrets.get("OPENAI_API_KEY")
serpapi_key = st.secrets.get("SERPAPI_KEY")

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
    st.stop()  # stop the app if keys are missing

# ── 3. App title ────────────────────────────────────────────────────────────────
st.title("Company Research Assistant")

# ── 4. Ensure research_models.py exists ────────────────────────────────────────
models_path = Path("research_models.py")
if not models_path.exists():
    models_path.write_text(
        "# your research logic goes here\n"
        "def run_research(company, openai_key, serpapi_key):\n"
        "    # TODO: implement multi-prompt flows\n"
        "    return {'overview': '…', 'headlines': []}\n"
    )

# ── 5. Sidebar editor for research_models.py ──────────────────────────────────
st.sidebar.header("⚙️ Edit Research Models")
source_code = models_path.read_text()
edited = st.sidebar.text_area(
    "research_models.py", source_code, height=400
)
if st.sidebar.button("Save & Reload"):
    models_path.write_text(edited)
    importlib.invalidate_caches()
    import research_models  # noqa: F401
    importlib.reload(research_models)
    st.sidebar.success("Reloaded research_models.py!")

# ── 6. Main UI: run research with error handling ───────────────────────────────
company = st.text_input("Enter a company name", placeholder="e.g. Acme Corp")
if st.button("Run Research") and company:
    import research_models  # noqa: F401

    try:
        results = research_models.run_research(company, openai_key, serpapi_key)
    except Exception as e:
        logging.exception("Research API call failed")
        st.error(f"❌ Research failed: {e}")
    else:
        # Headlines
        st.subheader("Top News Headlines")
        headlines = results.get("headlines") or []
        if headlines:
            for i, h in enumerate(headlines, 1):
                st.write(f"{i}. {h}")
        else:
            st.warning("No headlines returned.")

        # Overview
        st.subheader("AI‑Generated Overview")
        overview = results.get("overview")
        if overview:
            st.write(overview)
        else:
            st.warning("No overview returned.")
