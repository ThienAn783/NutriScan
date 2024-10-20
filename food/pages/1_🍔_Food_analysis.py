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

def format_number(value):
    if value is not None:
        formatted = f"{value:.10f}"
        return f"{formatted.rstrip('0').rstrip('.')}"
    else:
        value = '0'
        return value

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
    def total_sum_expander():
        with st.expander("Nutritional Information"):
            st.write(f"**Total Calories:** {format_number(calorie_sum)} kcal")
            st.write(f"**Total Fat:** {format_number(fat_sum)} g")
            st.write(f"**Total Cholesterol:** {format_number(cholesterol_sum)} mg")
            st.write(f"**Total Sodium:** {format_number(sodium_sum)} mg")
            st.write(f"**Total Carbohydrates:** {format_number(carbs_sum)} g")
            st.write(f"**Total Dietary Fiber:** {format_number(fiber_sum)} g")
            st.write(f"**Total Sugars:** {format_number(sugars_sum)} g")
            st.write(f"**Total Protein:** {format_number(protein_sum)} g")
            st.write(f"**Total Vitamin A:** {format_number(vitamin_a_sum)} µg")
            st.write(f"**Total Vitamin C:** {format_number(vitamin_c_sum)} mg")
            st.write(f"**Total Vitamin D:** {format_number(vitamin_d_sum)} µg")
            st.write(f"**Total Vitamin B12:** {format_number(vitamin_b12_sum)} µg")
            st.write(f"**Total Calcium:** {format_number(calcium_sum)} mg")
            st.write(f"**Total Iron:** {format_number(iron_sum)} mg")
            st.write(f"**Total Potassium:** {format_number(potassium_sum)} mg")
    #variable initializations
    calorie_sum = 0
    fat_sum = 0
    cholesterol_sum = 0
    sodium_sum = 0
    carbs_sum = 0
    fiber_sum = 0
    sugars_sum = 0
    protein_sum = 0
    vitamin_a_sum = 0
    vitamin_c_sum = 0
    vitamin_d_sum = 0
    vitamin_b12_sum = 0
    calcium_sum = 0
    iron_sum = 0
    potassium_sum = 0

    for i, item in enumerate(items):
        food_list = item.get('food', [])
        if food_list:
            food = food_list[0]
            food_info = food.get('food_info', {})
            if food_info:
                nutrition = food_info.get('nutrition', {})
                calorie_sum += (nutrition.get('calories_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('calories_100g') is not None else 0
                fat_sum += (nutrition.get('fat_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('fat_100g') is not None else 0
                cholesterol_sum += (nutrition.get('cholesterol_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('cholesterol_100g') is not None else 0
                sodium_sum += (nutrition.get('sodium_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('sodium_100g') is not None else 0
                carbs_sum += (nutrition.get('carbs_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('carbs_100g') is not None else 0
                fiber_sum += (nutrition.get('fibers_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('fibers_100g') is not None else 0
                sugars_sum += (nutrition.get('sugars_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('sugars_100g') is not None else 0
                protein_sum += (nutrition.get('proteins_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('proteins_100g') is not None else 0
                
                # If expanding vitamins and minerals
                vitamin_a_sum += (nutrition.get('vitamin_a_retinol_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('vitamin_a_retinol_100g') is not None else 0
                vitamin_c_sum += (nutrition.get('vitamin_c_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('vitamin_c_100g') is not None else 0
                vitamin_d_sum += (nutrition.get('vitamin_d_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('vitamin_d_100g') is not None else 0
                vitamin_b12_sum += (nutrition.get('vitamin_b12_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('vitamin_b12_100g') is not None else 0
                
                calcium_sum += (nutrition.get('calcium_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('calcium_100g') is not None else 0
                iron_sum += (nutrition.get('iron_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('iron_100g') is not None else 0
                potassium_sum += (nutrition.get('potassium_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('potassium_100g') is not None else 0
    st.markdown('<span style="font-size: 24px;">Total Nutritional Information for Meal</span>', unsafe_allow_html=True)
    total_sum_expander()

    for i, item in enumerate(items):
        food_list = item.get('food', [])  # Get the list of foods, default to empty list if key is missing
        # Only process the first food item for each item
        if food_list:  # Ensure that the food list is not empty
            food = food_list[0]  # Get the first food item
            food_info = food.get('food_info', {})  # Use .get() to avoid KeyError
            if food_info:  # Check if food_info is not empty
                display_name = food_info.get('display_name', 'Unknown')
                nutrition = food_info.get('nutrition', {})
                # Display food information using Streamlit
                st.markdown(f'<span style="font-size: px;">Ingredient {i+1}: </span><strong>{display_name}</strong>', unsafe_allow_html=True)
                with st.expander("Nutritional Information"):
                    st.write(f"**Serving Size:** {food_info.get('g_per_serving')} g")
                    st.write(
                        f"**Calories:** {format_number((nutrition['calories_100g'] / 100 * food_info.get('g_per_serving')) if nutrition.get('calories_100g') is not None else 0)} kcal"
                        )
                    # Display nutritional information with ternary operators for safety
                    st.write(f"**Total Fat:** {format_number((nutrition.get('fat_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('fat_100g') is not None else 0)} g")
                    st.write(f"**Cholesterol:** {format_number((nutrition.get('cholesterol_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('cholesterol_100g') is not None else 0)} mg")
                    st.write(f"**Sodium:** {format_number((nutrition.get('sodium_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('sodium_100g') is not None else 0)} mg")
                    st.write(f"**Total Carbohydrates:** {format_number((nutrition.get('carbs_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('carbs_100g') is not None else 0)} g")
                    st.write(f"  - **Dietary Fiber:** {format_number((nutrition.get('fibers_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('fibers_100g') is not None else 0)} g")
                    st.write(f"  - **Total Sugars:** {format_number((nutrition.get('sugars_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('sugars_100g') is not None else 0)} g")
                    st.write(f"**Protein:** {format_number((nutrition.get('proteins_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('proteins_100g') is not None else 0)} g")
    
                    if st.checkbox("Expand to see Vitamins", key=f"vitamins_{i}"):
                        st.write(f"**Vitamin A:** {format_number((nutrition.get('vitamin_a_retinol_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('vitamin_a_retinol_100g') is not None else 0)} µg")
                        st.write(f"**Vitamin C:** {format_number((nutrition.get('vitamin_c_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('vitamin_c_100g') is not None else 0)} mg")
                        st.write(f"**Vitamin D:** {format_number((nutrition.get('vitamin_d_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('vitamin_d_100g') is not None else 0)} µg")
                        st.write(f"**Vitamin B12:** {format_number((nutrition.get('vitamin_b12_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('vitamin_b12_100g') is not None else 0)} µg")
    
                    if st.checkbox("Expand to see Minerals", key=f"minerals_{i}"):
                        st.write(f"**Calcium:** {format_number((nutrition.get('calcium_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('calcium_100g') is not None else 0)} mg")
                        st.write(f"**Iron:** {format_number((nutrition.get('iron_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('iron_100g') is not None else 0)} mg")
                        st.write(f"**Potassium:** {format_number((nutrition.get('potassium_100g', 0) / 100 * food_info.get('g_per_serving', 0)) if nutrition.get('potassium_100g') is not None else 0)} mg")
    
            else:
                st.write(f"Food[{i}]: No food info available.")

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
