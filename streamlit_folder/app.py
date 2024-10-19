# app.py

import streamlit as st
import requests
from PIL import Image
import os

# Set your Foodvisor API Key
FOODVISOR_API_KEY = os.getenv('FOODVISOR_API_KEY')  # Recommended to use environment variables

if not FOODVISOR_API_KEY:
    st.error("API key not found. Please set the FOODVISOR_API_KEY environment variable.")
else:
    # Title
    st.title("Calorie Tracker App")

    # Initialize session state
    if 'food_log' not in st.session_state:
        st.session_state.food_log = []

    # Image upload
    uploaded_file = st.file_uploader("Upload an image of your food", type=["jpg", "jpeg", "png"])

    # Function to call Foodvisor API
    def get_nutrition_info(image_bytes):
        url = "https://vision.foodvisor.io/api/1.0/en/analysis/"
        headers = {
            "Authorization": f"Api-Key s4KvFyQy.f1GvtvWfS2WvwpnalDP5zSTnRdG9xH6k"
        }
        files = {
            "image": ("image.jpg", image_bytes, "image/jpeg")
        }
        response = requests.post(url, headers=headers, files=files)
        
        try:
            response.raise_for_status()  # Raises HTTPError for bad responses (4XX or 5XX)
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
            st.header("Nutrition Information")
            
            # Access the 'items' key from the response
            items = result.get('items', [])
            
            if items:
                for idx, item in enumerate(items):
                    # Each item may contain multiple food options
                    foods = item.get('food', [])
                    for food in foods:
                        # Get food information
                        food_info = food.get('food_info', {})
                        food_name = food_info.get('display_name', 'Unknown')
                        nutrition = food_info.get('nutrition', {})
                        
                        st.subheader(f"Detected Food {idx + 1}: {food_name}")
                        
                        # Display nutrition details
                        st.write("**Nutrition Details (per 100g):**")
                        for nutrient, value in nutrition.items():
                            if value is not None:
                                nutrient_name = nutrient.replace('_100g', '').replace('_', ' ').capitalize()
                                st.write(f"- {nutrient_name}: {value}")
                        
                        # Log the food
                        st.session_state.food_log.append({
                            'food_name': food_name,
                            'nutrition': nutrition
                        })
            else:
                st.warning("No food items detected in the image.")
        else:
            st.error("Failed to retrieve nutrition information.")

    # Display daily intake
    if st.session_state.food_log:
        st.header("Today's Food Intake")
        total_calories = 0

        for idx, entry in enumerate(st.session_state.food_log):
            st.write(f"**{idx + 1}. {entry['food_name']}**")
            nutrition = entry['nutrition']
            for nutrient, value in nutrition.items():
                if value is not None:
                    nutrient_name = nutrient.replace('_100g', '').replace('_', ' ').capitalize()
                    st.write(f"- {nutrient_name}: {value}")
                    if nutrient == 'calories_100g':
                        total_calories += float(value)
        st.write(f"**Total Calories Consumed:** {total_calories} kcal")
    else:
        st.write("No food items logged yet.")

    # Daily calorie recommendation
    st.header("Daily Calorie Recommendation")

    age = st.number_input("Enter your age:", min_value=1, max_value=120, value=25)
    gender = st.selectbox("Select your gender:", options=["Male", "Female"])
    weight = st.number_input("Enter your weight (kg):", min_value=1.0, max_value=300.0, value=70.0)
    height = st.number_input("Enter your height (cm):", min_value=50.0, max_value=250.0, value=170.0)
    activity_level = st.selectbox("Select your activity level:", options=[
        "Sedentary (little or no exercise)",
        "Lightly active (light exercise/sports 1-3 days/week)",
        "Moderately active (moderate exercise/sports 3-5 days/week)",
        "Very active (hard exercise/sports 6-7 days a week)",
        "Extra active (very hard exercise/sports & physical job)"
    ])

    def calculate_bmr(gender, weight, height, age):
        if gender == "Male":
            return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    def calculate_daily_calories(bmr, activity_level):
        activity_multipliers = {
            "Sedentary (little or no exercise)": 1.2,
            "Lightly active (light exercise/sports 1-3 days/week)": 1.375,
            "Moderately active (moderate exercise/sports 3-5 days/week)": 1.55,
            "Very active (hard exercise/sports 6-7 days a week)": 1.725,
            "Extra active (very hard exercise/sports & physical job)": 1.9
        }
        return bmr * activity_multipliers[activity_level]

    if st.button("Calculate Recommended Daily Calories"):
        bmr = calculate_bmr(gender, weight, height, age)
        daily_calories = calculate_daily_calories(bmr, activity_level)
        st.write(f"**Your Recommended Daily Calorie Intake:** {daily_calories:.2f} kcal")
