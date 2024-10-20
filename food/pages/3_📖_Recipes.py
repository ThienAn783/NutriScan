# pages/3_📖_Recipes.py

import streamlit as st
import requests
import os
from utils import format_number

st.title("Recipes 📖")

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

if not SERPAPI_API_KEY:
    st.error("SERPAPI_API_KEY environment variable not set.")
    st.stop()

# Check if display_name is available
if 'display_name' in st.session_state:
    display_name = st.session_state['display_name']

    st.write(f"Showing recipes for **{display_name}**.")

    # Get recipe suggestions
    params = {
        "q": f"{display_name} recipe",
        "location": "United States",
        "hl": "en",
        "gl": "us",
        "api_key": SERPAPI_API_KEY
    }

    response = requests.get('https://serpapi.com/search', params=params)
    try:
        response.raise_for_status()
        results = response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
        st.write(response.text)
        st.stop()
    except Exception as err:
        st.error(f"An error occurred: {err}")
        st.stop()

    # Display recipe links
    if "organic_results" in results:
        for result in results["organic_results"][:5]:
            title = result.get("title")
            link = result.get("link")
            if title and link:
                st.markdown(f"- [{title}]({link})")
    else:
        st.write("No recipes found.")
else:
    st.info("Please analyze a food item on the 'Food Analysis' page first.")
