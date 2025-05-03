#!/bin/bash

echo "🔧 Setting up your Company Research Assistant (Linux)"

# Update and install Python and pip
sudo apt update
sudo apt install -y python3 python3-pip

# Install dependencies
pip3 install -r requirements.txt

# Prompt for API keys
read -p "Enter your OpenAI API Key: " OPENAI_API_KEY
read -p "Enter your SerpApi API Key: " SERPAPI_KEY

# Store in .bashrc
echo "export OPENAI_API_KEY=\"$OPENAI_API_KEY\"" >> ~/.bashrc
echo "export SERPAPI_KEY=\"$SERPAPI_KEY\"" >> ~/.bashrc
source ~/.bashrc

# Run app
streamlit run company_research_app.py