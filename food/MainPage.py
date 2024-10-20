import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Food Nutrition App",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load CSS from external file
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# --- CSS Styling ---
st.markdown(
    """
    <style>
    .main-header {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #282c34; /* Dark grey */
        text-align: center;
    }
    .main-description {
        font-family: 'Open Sans', sans-serif;
        color: #444;
        text-align: center;
        line-height: 1.6;
        margin-top: -20px; /* Adjust spacing */
    }
    .feature-list {
        text-align: center;
        list-style-type: none;
        padding: 0;
    }
    .feature-list li {
        display: inline-block;
        margin: 0 15px;
        font-family: 'Source Sans Pro', sans-serif;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# --- End CSS Styling ---

# Display logo
st.image('logo.png', width=200)

# Title and description with CSS classes
st.markdown('<h1 class="main-header">Welcome to the Food Nutrition App 🍽️</h1>', unsafe_allow_html=True)
st.markdown(
    """
    <p class="main-description">
    This app allows you to:
    <ul class="feature-list">
        <li>- <b>Analyze food images</b> to get nutritional information.</li>
        <li>- <b>Track your calorie intake.</b></li>
        <li>- <b>Get recipe suggestions.</b></li>
        <li>- <b>Calculate your daily calorie recommendations.</b></li>
    </ul>
    Use the navigation menu on the left to select a page.
    </p>
    """,
    unsafe_allow_html=True,
)
