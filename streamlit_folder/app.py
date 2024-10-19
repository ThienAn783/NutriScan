# app.py

import streamlit as st
import requests
from PIL import Image
import io
import os

# Replace with your actual API key or use environment variables
FOODVISOR_API_KEY = os.getenv('FOODVISOR_API_KEY') or 'YOUR_FOODVISOR_API_KEY'

# Title
st.title("Calorie Tracker App")

# Initialize session state
if 'food_log' not in st.session_state:
    st.session_state.food_log = []

# Image upload
uploaded_file = st.file_uploader("Upload an image of your food", type=["jpg", "jpeg", "png"])

# Function to call FoodVisor API
def get_nutrition_info(image_bytes):
    url = "https://api.foodvisor.io/v1/food_detection"  # Replace with the actual API endpoint
    headers = {
        "Authorization": f"Bearer s4KvFyQy.f1GvtvWfS2WvwpnalDP5zSTnRdG9xH6k",
        "Content-Type": "application/octet-stream"
    }
    response = requests.post(url, headers=headers, data=image_bytes)
    
    try:
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
        st.write(response.text)
    except requests.exceptions.RequestException as err:
        st.error(f"An error occurred: {err}")
    except ValueError:
        st.error("Invalid JSON received from the API.")
        st.write(response.text)
    
    return None

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Convert image to bytes
    img_bytes = uploaded_file.read()

    # Get nutrition info
    with st.spinner('Analyzing image...'):
        result = get_nutrition_info(img_bytes)

    if result:
        st.success('Analysis complete!')

        # Display nutrition information
        st.header("Nutrition Information")

        # Adjust the following based on actual API response
        food_name = result.get('food_name', 'Unknown')
        nutrition = result.get('nutrition', {})

        st.subheader(f"Detected Food: {food_name}")

        st.write("**Nutrition Details:**")
        for nutrient, value in nutrition.items():
            st.write(f"- {nutrient.capitalize()}: {value}")

        # Log the food
        st.session_state.food_log.append({
            'food_name': food_name,
            'nutrition': nutrition
        })
    else:
        st.error("Failed to retrieve nutrition information.")

# The rest of your code remains the same...
