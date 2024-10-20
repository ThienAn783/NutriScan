# pages/1_Food_Analysis.py

import streamlit as st
import requests
from PIL import Image
import io
import os
from utils import format_number
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Food Analysis",
    page_icon="🍔",
    layout="wide",
)

# Set page title
st.title("Food Analysis 🍔")

# Access API keys
API_KEY = os.getenv('FOODVISOR_API_KEY')
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

if not API_KEY:
    st.error("FOODVISOR_API_KEY environment variable not set.")
    st.stop()
if not SERPAPI_API_KEY:
    st.error("SERPAPI_API_KEY environment variable not set.")
    st.stop()

# File uploader for the user to upload an image
uploaded_file = st.file_uploader("Upload an image of your food", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image file
    image_bytes = uploaded_file.read()

    # Determine the MIME type
    filename = uploaded_file.name
    if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
        mime_type = 'image/jpeg'
    elif filename.lower().endswith('.png'):
        mime_type = 'image/png'
    else:
        st.error("Unsupported file type. Please upload a JPG or PNG image.")
        st.stop()

    # Display the uploaded image
    image = Image.open(io.BytesIO(image_bytes))
    st.image(image, caption='Uploaded Food Image', use_column_width=True)

    # Prepare and send the request to the Foodvisor API
    url = "https://vision.foodvisor.io/api/1.0/en/analysis/"
    headers = {"Authorization": "Api-Key " + API_KEY}
    files = {
        "image": (filename, image_bytes, mime_type)
    }

    with st.spinner('Analyzing image...'):
        response = requests.post(url, headers=headers, files=files)
        try:
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
            st.write(response.text)
            st.stop()
        except Exception as err:
            st.error(f"An error occurred: {err}")
            st.stop()

    # Check if any items were detected
    items = data.get('items')
    if not items:
        st.error("No food items detected in the image.")
        st.stop()

    # Extract data from the API response
    try:
        display_name = data["items"][0]["food"][0]["food_info"]["display_name"]
        nutrition = data["items"][0]["food"][0]["food_info"]["nutrition"]
    except (IndexError, KeyError):
        st.error("Unexpected response structure from the API.")
        st.write(data)  # Optionally display the raw data for debugging
        st.stop()

    st.success('Analysis complete!')

    # Display the nutritional information
    with st.expander("Nutritional Information"):
        st.write(f"**Food Item:** {display_name}")
        st.write("**Serving Size:** 100 g")
        st.write(f"**Calories:** {format_number(nutrition.get('calories_100g'))} kcal")
        st.write(f"**Total Fat:** {format_number(nutrition.get('fat_100g'))} g")
        st.write(f"  - **Saturated Fat:** {format_number(nutrition.get('sat_fat_100g'))} g")
        st.write(f"**Cholesterol:** {format_number(nutrition.get('cholesterol_100g'))} mg")
        st.write(f"**Sodium:** {format_number(nutrition.get('sodium_100g'))} mg")
        st.write(f"**Total Carbohydrates:** {format_number(nutrition.get('carbs_100g'))} g")
        st.write(f"  - **Dietary Fiber:** {format_number(nutrition.get('fibers_100g'))} g")
        st.write(f"  - **Sugars:** {format_number(nutrition.get('sugars_100g'))} g")
        st.write(f"**Protein:** {format_number(nutrition.get('proteins_100g'))} g")
        if st.checkbox("Expand to see Vitamins"):
            st.write(f"**Vitamin A:** {format_number(nutrition.get('vitamin_a_retinol_100g'))} µg")
            st.write(f"**Vitamin C:** {format_number(nutrition.get('vitamin_c_100g'))} mg")
            st.write(f"**Vitamin D:** {format_number(nutrition.get('vitamin_d_100g'))} µg")
            st.write(f"**Vitamin B12:** {format_number(nutrition.get('vitamin_b12_100g'))} µg")
        if st.checkbox("Expand to see Minerals"):
            st.write(f"**Calcium:** {format_number(nutrition.get('calcium_100g'))} mg")
            st.write(f"**Iron:** {format_number(nutrition.get('iron_100g'))} mg")
            st.write(f"**Potassium:** {format_number(nutrition.get('potassium_100g'))} mg")

    # Save data to session state for use in other pages
    st.session_state['display_name'] = display_name
    st.session_state['nutrition'] = nutrition

    # Function for taking in user input and searching it on the web
    def search_user_input():
        user_input = st.text_input("What would you like to know about this food?", "")

        if user_input:
            query = display_name + " " + user_input

            params = {
                "q": query,
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
                return
            except Exception as err:
                st.error(f"An error occurred: {err}")
                return

            if "organic_results" in results:
                for result in results["organic_results"]:
                    title = result.get("title")
                    link = result.get("link")
                    if title and link:
                        st.markdown(f"[{title}]({link})")
            else:
                st.write("No results found.")

    search_user_input()
else:
    st.info("Please upload an image of your food to get started.")
