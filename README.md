# Company Research Assistant (Streamlit App)

This is a lightweight Streamlit application designed to research companies across cybersecurity, M365, AI, and executive strategy.

## ✅ Features
- Multiprompt GPT-4o-powered research
- Executive discovery via LinkedIn (via SerpApi)
- Custom prompts per category
- Secrets loaded securely using `.streamlit/secrets.toml`

## 🔧 Setup

1. Clone this repo:
   ```
   git clone https://github.com/yourusername/company-research-assistant.git
   cd company-research-assistant
   ```

2. Install requirements:
   ```
   pip install -r requirements.txt
   ```

3. Set your API keys in `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "your-openai-key"
   SERPAPI_KEY = "your-serpapi-key"
   ```

4. Run the app:
   ```
   streamlit run company_research_app.py
   ```

## 🚫 Do not commit your secrets file
`.gitignore` already excludes `.streamlit/secrets.toml` to keep your keys safe.