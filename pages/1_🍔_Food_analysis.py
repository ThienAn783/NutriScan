from openai import OpenAI
import streamlit as st
import requests
from PIL import Image
import io
import os
from dotenv import load_dotenv
import random
from datetime import datetime
import json
from streamlit_calendar import calendar

load_dotenv()
list_of_ingredients = []
import json
import os
import os
import json
import streamlit as st

def load_user_data(user_id):
    filename = "users.json"
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({}, f)
    with open(filename, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    return data.get(user_id, {})

def save_user_data(user_id, data):
    filename = "users.json"
    with open(filename, 'r') as f:
        users_data = json.load(f)
    users_data[user_id] = data
    with open(filename, 'w') as f:
        json.dump(users_data, f, indent=4)

if 'user_id' not in st.session_state:
    user_id_input = st.text_input("Enter your User ID to proceed:", key="user_id_input")
    
    if st.button("Submit", key="submit_user_id"):
        if user_id_input:
            st.session_state['user_id'] = user_id_input
            st.rerun()
        else:
            st.warning("Please enter your User ID.")

if 'user_id' in st.session_state:
    user_id = st.session_state['user_id']
    st.success(f"Logged in as: {user_id}")

    if 'user_data' not in st.session_state:
        st.session_state['user_data'] = load_user_data(user_id)

    user_data = st.session_state['user_data']

    st.write("Proceed with the food analysis...")

    if 'analyzed_foods' not in st.session_state:
        st.session_state['analyzed_foods'] = []
    if 'meals' not in st.session_state:
        st.session_state['meals'] = []

    if 'analyzed_foods' in st.session_state and st.session_state['analyzed_foods']:
        for i, food in enumerate(st.session_state['analyzed_foods']):
            display_name = food.get('display_name', 'Unknown Food')
            st.write(f"Analyzed Food {i + 1}: {display_name}")
    if 'meals' in st.session_state and st.session_state['meals']:
        for i, meal in enumerate(st.session_state['meals']):
            st.write(f"Meal {i + 1}:")
            st.write(f"  Calories: {meal['Calories']}")
            st.write(f"  Fat: {meal['Fat']}")
            st.write(f"  Cholesterol: {meal['Cholesterol']}")
            st.write(f"  Sodium: {meal['Sodium']}")
            st.write(f"  Carbohydrates: {meal['Carbohydrates']}")
            st.write(f"  Fiber: {meal['Fiber']}")
            st.write(f"  Sugars: {meal['Sugars']}")
            st.write(f"  Protein: {meal['Protein']}")

def update_food_journal(user_id, date, name, calorie_sum, protein_sum, fat_sum, cholesterol_sum, sodium_sum, carbs_sum, fiber_sum, sugars_sum):
    filename = f"temp_users/{user_id}.json"
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        with open(filename, 'w') as f:
            json.dump({}, f)
    with open(filename, 'r') as f:
        try:
            food_journal = json.load(f)
        except json.JSONDecodeError:
            food_journal = {}
    if date not in food_journal:
        food_journal[date] = []
    food_journal[date].append({
        "mealname": name,
        "calorie_sum": calorie_sum,
        "protein_sum": protein_sum,
        "fat_sum": fat_sum,
        "cholesterol_sum": cholesterol_sum,
        "sodium_sum": sodium_sum,
        "carbs_sum": carbs_sum,
        "fiber_sum": fiber_sum,
        "sugars_sum": sugars_sum,
    })
    with open(filename, 'w') as f:
        json.dump(food_journal, f, indent=4)

def format_number(value):
    if value is not None:
        formatted = f"{value:.10f}"
        return f"{formatted.rstrip('0').rstrip('.')}"
    else:
        value = '0'
        return value
API_KEY = st.secrets["api_credentials"]["API_KEY"]
SERPAPI_API_KEY = st.secrets["api_credentials"]["SERPAPI_API_KEY"]
api_key = st.secrets["api_credentials"]["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)
if not API_KEY:
    st.error("FOODVISOR_API_KEY environment variable not set.")
    st.stop()
if not SERPAPI_API_KEY:
    st.error("SERPAPI_API_KEY environment variable not set.")
    st.stop()

uploaded_file = st.file_uploader("Upload an image of your food", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:

    image_bytes = uploaded_file.read()

    filename = uploaded_file.name
    if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
        mime_type = 'image/jpeg'
    elif filename.lower().endswith('.png'):
        mime_type = 'image/png'
    else:
        st.error("Unsupported file type. Please upload a JPG or PNG image.")
        st.stop()

    image = Image.open(io.BytesIO(image_bytes))
    st.image(image, caption='Uploaded Food Image', use_column_width=True)

    url = "https://vision.foodvisor.io/api/1.0/en/analysis/"
    headers = {"Authorization": "Api-Key " + API_KEY}
    files = {
        "image": (filename, image_bytes, mime_type)
    }

    with st.spinner('Analyzing image...'):
        try:
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
            st.write(response.text)
            st.stop()
        except Exception as err:
            st.error(f"An error occurred: {err}")
            st.stop()

    st.success('Analysis complete!')

    items = data.get('items', None)

    if not items:
        st.error("No food items detected in the image.")
        st.stop()

    for i, item in enumerate(items):

        food_list = item.get('food', [])
        if not food_list:
            st.write(f"Item {i + 1}: No foods detected.")
            continue

        food_info = food_list[0].get('food_info', {})
        if not food_info:
            st.write(f"Item {i + 1}: No food information available.")
            continue

else:
    st.info("Please upload an image to start the food analysis.")

def display_and_choose_food_option(item, i):
    food_options = [food['food_info']['display_name'] for food in item['food']]
    food_options.append("None")
    key = f"selectbox_ingredient_{i}"
    selected_option = st.selectbox(f"Select the correct food item for Ingredient {i+1}", food_options, key=key)
    if selected_option == "None":
        food_info = {
            'display_name': 'None',
            'nutrition': {
                'calories_100g': 0.0,
                'fat_100g': 0.0,
                'cholesterol_100g': 0.0,
                'sodium_100g': 0.0,
                'carbs_100g': 0.0,
                'fibers_100g': 0.0,
                'sugars_100g': 0.0,
                'proteins_100g': 0.0,
                'vitamin_a_retinol_100g': 0.0,
                'vitamin_c_100g': 0.0,
                'vitamin_d_100g': 0.0,
                'vitamin_b12_100g': 0.0,
                'calcium_100g': 0.0,
                'iron_100g': 0.0,
                'potassium_100g': 0.0
            },
            'g_per_serving': 0.0
        }
    else:
        selected_food = next(food for food in item['food'] if food['food_info']['display_name'] == selected_option)
        food_info = selected_food['food_info']
        list_of_ingredients.append(food_info['display_name'])
    nutrition = food_info['nutrition']
    st.markdown(f"**Ingredient {i+1}: {food_info['display_name']}**")
    if selected_option != "None":
        with st.expander("Nutritional Information"):
            serving_size = food_info.get('g_per_serving', 0)
            st.write(f"**Serving Size:** {serving_size} g")
            st.write(f"**Calories:** {format_number((nutrition.get('calories_100g',0) / 100 * serving_size))} kcal")
            st.write(f"**Total Fat:** {format_number((nutrition.get('fat_100g', 0) / 100 * serving_size))} g")
            st.write(f"**Cholesterol:** {format_number((nutrition.get('cholesterol_100g', 0) / 100 * serving_size))} mg")
            st.write(f"**Sodium:** {format_number((nutrition.get('sodium_100g', 0) / 100 * serving_size))} mg")
            st.write(f"**Total Carbohydrates:** {format_number((nutrition.get('carbs_100g', 0) / 100 * serving_size))} g")
            st.write(f"  - **Dietary Fiber:** {format_number((nutrition.get('fibers_100g', 0) / 100 * serving_size))} g")
            st.write(f"  - **Sugars:** {format_number((nutrition.get('sugars_100g', 0) / 100 * serving_size))} g")
            st.write(f"**Protein:** {format_number((nutrition.get('proteins_100g', 0) / 100 * serving_size))} g")
    else:
        st.write("Ingredient not included in the meal.")
    
    return food_info

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

if uploaded_file is not None:
    for i, item in enumerate(items):
        food_info = display_and_choose_food_option(item, i)
        display_name = food_info['display_name']
        nutrition = food_info['nutrition']

        calorie_sum += round((nutrition.get('calories_100g', 0) / 100 * food_info.get('g_per_serving', 0)), 2) if nutrition.get('calories_100g') is not None else 0
        fat_sum += round((nutrition.get('fat_100g', 0) / 100 * food_info.get('g_per_serving', 0)), 2) if nutrition.get('fat_100g') is not None else 0
        cholesterol_sum += round((nutrition.get('cholesterol_100g', 0) / 100 * food_info.get('g_per_serving', 0)), 2) if nutrition.get('cholesterol_100g') is not None else 0
        sodium_sum += round((nutrition.get('sodium_100g', 0) / 100 * food_info.get('g_per_serving', 0)), 2) if nutrition.get('sodium_100g') is not None else 0
        carbs_sum += round((nutrition.get('carbs_100g', 0) / 100 * food_info.get('g_per_serving', 0)), 2) if nutrition.get('carbs_100g') is not None else 0
        fiber_sum += round((nutrition.get('fibers_100g', 0) / 100 * food_info.get('g_per_serving', 0)), 2) if nutrition.get('fibers_100g') is not None else 0
        sugars_sum += round((nutrition.get('sugars_100g', 0) / 100 * food_info.get('g_per_serving', 0)), 2) if nutrition.get('sugars_100g') is not None else 0
        protein_sum += round((nutrition.get('proteins_100g', 0) / 100 * food_info.get('g_per_serving', 0)), 2) if nutrition.get('proteins_100g') is not None else 0

        vitamin_a_sum += round((nutrition.get('vitamin_a_retinol_100g', 0) / 100 * food_info.get('g_per_serving', 0)), 2) if nutrition.get('vitamin_a_retinol_100g') is not None else 0
        vitamin_c_sum += round((nutrition.get('vitamin_c_100g', 0) / 100 * food_info.get('g_per_serving', 0)), 2) if nutrition.get('vitamin_c_100g') is not None else 0
        vitamin_d_sum += round((nutrition.get('vitamin_d_100g', 0) / 100 * food_info.get('g_per_serving', 0)), 2) if nutrition.get('vitamin_d_100g') is not None else 0
        vitamin_b12_sum += round((nutrition.get('vitamin_b12_100g', 0) / 100 * food_info.get('g_per_serving', 0)), 2) if nutrition.get('vitamin_b12_100g') is not None else 0

        calcium_sum += round((nutrition.get('calcium_100g', 0) / 100 * food_info.get('g_per_serving', 0)) , 2) if nutrition.get('calcium_100g') is not None else 0
        iron_sum += round((nutrition.get('iron_100g', 0) / 100 * food_info.get('g_per_serving', 0)), 2) if nutrition.get('iron_100g') is not None else 0
        potassium_sum += round((nutrition.get('potassium_100g', 0) / 100 * food_info.get('g_per_serving', 0)),2) if nutrition.get('potassium_100g') is not None else 0
        st.session_state['analyzed_foods'].append(food_info)
        mealname = ", ".join(list_of_ingredients)
        analyzed_food = {
            'mealname': mealname,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'calorie_sum': calorie_sum,
            'protein_sum': protein_sum,
            'fat_sum': fat_sum,
            'cholesterol_sum': cholesterol_sum,
            'sodium_sum': sodium_sum,
            'carbs_sum': carbs_sum,
            'fiber_sum': fiber_sum,
            'sugars_sum': sugars_sum
        }

        new_meal = {
            'Meal': f'Meal {len(st.session_state["meals"]) + 1}',
            'Calories': calorie_sum,
            'Fat': fat_sum,
            'Cholesterol': cholesterol_sum,
            'Sodium': sodium_sum,
            'Carbohydrates': carbs_sum,
            'Fiber': fiber_sum,
            'Sugars': sugars_sum,
            'Protein': protein_sum,
            'Eaten': False
        }

    st.session_state['meals'].append(new_meal)
    st.markdown('<span style="font-size: 24px;">Total Nutritional Information for Meal</span>', unsafe_allow_html=True)

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

def generate_nutritional_data(food_name):
    return {
        "calories_100g": random.uniform(50, 400),
        "fat_100g": random.uniform(0, 30),
        "proteins_100g": random.uniform(1, 30),
        "carbs_100g": random.uniform(1, 100),
        "fibers_100g": random.uniform(0, 15),
        "sugars_100g": random.uniform(0, 50),
        "cholesterol_100g": random.uniform(0, 150),
        "sodium_100g": random.uniform(0, 1000),
        "vitamin_a_retinol_100g": random.uniform(0, 500),
        "vitamin_c_100g": random.uniform(0, 100),
        "vitamin_d_100g": random.uniform(0, 10),
        "vitamin_b12_100g": random.uniform(0, 5),
        "calcium_100g": random.uniform(0, 500),
        "iron_100g": random.uniform(0, 10),
        "potassium_100g": random.uniform(0, 1000)
    }

def add_manual_food_optional():
    st.markdown("<span style='font-size: 24px;'>Add Food Manually</span>", unsafe_allow_html=True)
    
    manual_food_needed = st.checkbox("I need to manually add food")
    
    if manual_food_needed:
        manual_food_name = st.text_input("Enter the food name:")
        
        if manual_food_name:
            food_nutrition = generate_nutritional_data(manual_food_name)
            serving_size = st.number_input(f"Enter serving size for {manual_food_name} (g)", min_value=0)

            if serving_size > 0:

                calories = (food_nutrition['calories_100g'] / 100) * serving_size
                fat = (food_nutrition['fat_100g'] / 100) * serving_size
                protein = (food_nutrition['proteins_100g'] / 100) * serving_size
                carbs = (food_nutrition['carbs_100g'] / 100) * serving_size
                fiber = (food_nutrition['fibers_100g'] / 100) * serving_size
                sugars = (food_nutrition['sugars_100g'] / 100) * serving_size
                cholesterol = (food_nutrition['cholesterol_100g'] / 100) * serving_size
                sodium = (food_nutrition['sodium_100g'] / 100) * serving_size

                st.markdown(f"**Manually Added Food: {manual_food_name}**")
                with st.expander("Nutritional Information"):
                    st.write(f"**Serving Size:** {serving_size} g")
                    st.write(f"**Calories:** {format_number(calories)} kcal")
                    st.write(f"**Total Fat:** {format_number(fat)} g")
                    st.write(f"**Protein:** {format_number(protein)} g")
                    st.write(f"**Total Carbohydrates:** {format_number(carbs)} g")
                    st.write(f"  - **Dietary Fiber:** {format_number(fiber)} g")
                    st.write(f"  - **Sugars:** {format_number(sugars)} g")
                    st.write(f"**Cholesterol:** {format_number(cholesterol)} mg")
                    st.write(f"**Sodium:** {format_number(sodium)} mg")

                include_in_total = st.checkbox(f"Include {manual_food_name} in total nutritional data")

                if include_in_total:
                    global calorie_sum, fat_sum, protein_sum, carbs_sum, fiber_sum, sugars_sum, cholesterol_sum, sodium_sum
                    calorie_sum += calories
                    fat_sum += fat
                    protein_sum += protein
                    carbs_sum += carbs
                    fiber_sum += fiber
                    sugars_sum += sugars
                    cholesterol_sum += cholesterol
                    sodium_sum += sodium

                    total_sum_expander()

if uploaded_file is not None:
    add_manual_food_optional()

    st.session_state['calorie_sum'] = calorie_sum
    st.session_state['fat_sum'] = fat_sum
    st.session_state['cholesterol_sum'] = cholesterol_sum
    st.session_state['sodium_sum'] = sodium_sum
    st.session_state['carbs_sum'] = carbs_sum
    st.session_state['fiber_sum'] = fiber_sum
    st.session_state['sugars_sum'] = sugars_sum
    st.session_state['protein_sum'] = protein_sum
    st.session_state['vitamin_a_sum'] = vitamin_a_sum
    st.session_state['vitamin_c_sum'] = vitamin_c_sum
    st.session_state['vitamin_d_sum'] = vitamin_d_sum
    st.session_state['vitamin_b12_sum'] = vitamin_b12_sum
    st.session_state['calcium_sum'] = calcium_sum
    st.session_state['iron_sum'] = iron_sum
    st.session_state['potassium_sum'] = potassium_sum

    total_sum_expander()
    
    mealname = ", ".join(list_of_ingredients)
    date = datetime.now().strftime("%Y-%m-%d")
    update_food_journal(user_id, date, mealname, calorie_sum, protein_sum, fat_sum, cholesterol_sum, sodium_sum, carbs_sum, fiber_sum, sugars_sum)

    st.session_state['analyzed_foods'].append({'mealname': mealname, 'date': date})
    user_data['analyzed_foods'] = st.session_state['analyzed_foods']
    save_user_data(user_id, user_data)

if st.checkbox("Would you like to immediately add today's meal to your journal?"):
    date = datetime.now()
    date_string = date.strftime("%Y-%m-%d")
    update_food_journal(user_id, date_string, mealname, calorie_sum, protein_sum, fat_sum, cholesterol_sum, sodium_sum, carbs_sum, fiber_sum, sugars_sum)
elif st.checkbox("Would you like to add the meal to a specific day?"):
    date = st.date_input("Select a date for your food journal", value=None)
    if date is not None:
        date_string = date.strftime("%Y-%m-%d")
        update_food_journal(user_id, date_string, mealname, calorie_sum, protein_sum, fat_sum, cholesterol_sum, sodium_sum, carbs_sum, fiber_sum, sugars_sum)


