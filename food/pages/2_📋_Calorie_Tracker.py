# pages/2_Calorie_Tracker.py

import streamlit as st
from utils import format_number

st.set_page_config(
    page_title="Calorie Tracker",
    page_icon="📋",
    layout="wide",
)

st.title("Calorie Tracker 📋")

# Initialize session state
if 'food_log' not in st.session_state:
    st.session_state['food_log'] = []

# Check if nutrition data is available
if 'nutrition' in st.session_state and 'display_name' in st.session_state:
    nutrition = st.session_state['nutrition']
    display_name = st.session_state['display_name']

    # Input for quantity consumed
    quantity = st.number_input(f"How many grams of {display_name} did you consume?", min_value=0.0, value=100.0)

    if st.button("Add to Calorie Tracker"):
        # Calculate total calories based on quantity
        calories_per_100g = float(nutrition.get('calories_100g', 0))
        total_calories = (calories_per_100g / 100) * quantity

        # Add to food log
        st.session_state['food_log'].append({
            'food_name': display_name,
            'quantity': quantity,
            'calories': total_calories
        })
        st.success(f"Added {quantity}g of {display_name} to your calorie tracker.")
else:
    st.info("Please analyze a food item on the 'Food Analysis' page first.")

# Display the food log
if st.session_state['food_log']:
    st.subheader("Today's Food Intake")
    total_calories_consumed = 0

    for idx, entry in enumerate(st.session_state['food_log']):
        st.write(f"**{idx + 1}. {entry['food_name']}**")
        st.write(f"- Quantity: {entry['quantity']} g")
        st.write(f"- Calories: {format_number(entry['calories'])} kcal")
        total_calories_consumed += entry['calories']

    st.write(f"**Total Calories Consumed:** {format_number(total_calories_consumed)} kcal")
else:
    st.info("No food items logged yet.")

if 'nutrition_facts' in st.session_state:
    nutrition_facts = st.session_state.nutrition_facts

    st.title(Nutrition Facts Summary:)
