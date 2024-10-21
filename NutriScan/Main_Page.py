# app.py

import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="NutriScan",
    page_icon="🍽️",p
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and description
st.title("Welcome to the NutriScan 🍽️")

st.write("""
This app allows you to:

- **Analyze food images** to get nutritional information.
- **Track your calorie intake.**
- **Get recipe suggestions.**
- **Calculate your daily calorie recommendations.**
- **Calendar**
Use the navigation menu on the left to select a page.
""")

# Optional: Display a logo or image
st.image('https://github.com/LuisMorelos/Washu-Hack-Food-Information-Website/blob/main/NutriScan/logo.png', width=200)  # Ensure 'logo.png' is in the same directory or adjust the path accordingly.
