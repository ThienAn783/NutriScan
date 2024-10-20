import streamlit as st
import pandas as pd
from utils import format_number

st.set_page_config(
    page_title="Calorie Tracker",
    page_icon="📋",
    layout="wide",
)

st.title("Calorie Tracker 📋")

# Initialize session state for meals if not already initialized
if 'meals' not in st.session_state:
    st.session_state['meals'] = []

# Check if nutritional data exists from the Food Analysis page
if 'calorie_sum' in st.session_state:
    # Create a meal data dictionary with the current analyzed nutritional information
    meal_data = {
        'Meal': f'Meal {len(st.session_state["meals"]) + 1}',  # Unique meal name based on the current count
        'Calories': st.session_state['calorie_sum'],  # Total calories for this meal
        'Fat': st.session_state['fat_sum'],
        'Cholesterol': st.session_state['cholesterol_sum'],
        'Sodium': st.session_state['sodium_sum'],
        'Carbohydrates': st.session_state['carbs_sum'],
        'Fiber': st.session_state['fiber_sum'],
        'Sugars': st.session_state['sugars_sum'],
        'Protein': st.session_state['protein_sum'],
        'Eaten': False  # Default to False, meal not eaten yet
    }

    # Avoid duplicating the same meal if already added
    if not st.session_state['meals'] or st.session_state['meals'][-1]['Calories'] != meal_data['Calories']:
        st.session_state['meals'].append(meal_data)

# Create a DataFrame to display the meals
df = pd.DataFrame(st.session_state['meals'])

# Display table with meal data and checkboxes for "Eaten"
st.subheader("Your Meals")
for index, meal in df.iterrows():
    # Checkbox for each meal to mark whether it was eaten or not
    eaten = st.checkbox(f"{meal['Meal']}: {format_number(meal['Calories'])} kcal", key=f"eaten_{index}")
    st.session_state['meals'][index]['Eaten'] = eaten

# Calculate the total nutrition from eaten meals
total_calories = sum(meal['Calories'] for meal in st.session_state['meals'] if meal['Eaten'])
total_fat = sum(meal['Fat'] for meal in st.session_state['meals'] if meal['Eaten'])
total_cholesterol = sum(meal['Cholesterol'] for meal in st.session_state['meals'] if meal['Eaten'])
total_sodium = sum(meal['Sodium'] for meal in st.session_state['meals'] if meal['Eaten'])
total_carbs = sum(meal['Carbohydrates'] for meal in st.session_state['meals'] if meal['Eaten'])
total_fiber = sum(meal['Fiber'] for meal in st.session_state['meals'] if meal['Eaten'])
total_sugars = sum(meal['Sugars'] for meal in st.session_state['meals'] if meal['Eaten'])
total_protein = sum(meal['Protein'] for meal in st.session_state['meals'] if meal['Eaten'])

# Display the total sum
st.subheader("Total Nutritional Information from Eaten Meals")
st.write(f"**Total Calories:** {format_number(total_calories)} kcal")
st.write(f"**Total Fat:** {format_number(total_fat)} g")
st.write(f"**Total Cholesterol:** {format_number(total_cholesterol)} mg")
st.write(f"**Total Sodium:** {format_number(total_sodium)} mg")
st.write(f"**Total Carbohydrates:** {format_number(total_carbs)} g")
st.write(f"**Total Dietary Fiber:** {format_number(total_fiber)} g")
st.write(f"**Total Sugars:** {format_number(total_sugars)} g")
st.write(f"**Total Protein:** {format_number(total_protein)} g")
