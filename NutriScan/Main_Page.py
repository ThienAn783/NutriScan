import streamlit as st

st.set_page_config(
    page_title="NutriScan",
    page_icon="https://raw.githubusercontent.com/ThienAn783/NutriScan/main/NutriScan/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# HTML and CSS for styling
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 50px;
            font-weight: bold;
            color: #2E86C1;
        }
        .description {
            text-align: center;
            font-size: 20px;
            margin-top: 20px;
        }
        .logo {
            display: block;
            margin-left: auto;
            margin-right: auto;
            margin-bottom: 20px;
        }
        .app-container {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="app-container">
        <h1 class="main-title">Welcome to NutriScan 🍽️</h1>
        <p class="description">
            This app allows you to:
            <ul>
                <li><b>Analyze food images</b> to get nutritional information.</li>
                <li><b>Track your calorie intake.</b></li>
                <li><b>Get recipe suggestions.</b></li>
                <li><b>Calculate your daily calorie recommendations.</b></li>
                <li><b>View your calorie calendar.</b></li>
            </ul>
            Use the navigation menu on the left to select a page.
        </p>
    </div>
""", unsafe_allow_html=True)
st.markdown("""
    <img src="https://raw.githubusercontent.com/ThienAn783/NutriScan/main/NutriScan/logo.png" alt="NutriScan Logo" class="logo" width="500">
""", unsafe_allow_html=True)
