import streamlit as st
import json
from datetime import datetime

def load_meals(date):
    with open('user.json', 'r') as file:
        data = json.load(file)
        
    # Extract meals for the specified date
    meals = data.get(date.strftime("%Y-%m-%d"), [])
    return meals

st.title("Food Journal")

selected_date = st.date_input("Select a date:", datetime.now())

meals = load_meals(selected_date)
if meals:
    st.write(f"Meals for {selected_date}:")
    for meal in meals:
        st.write(f"- **{meal['mealname']}**: Calories: {meal['calorie_sum']}, Protein: {meal['protein_sum']}g, Fat: {meal['fat_sum']}g, Cholesterol: {meal['cholesterol_sum']} mg, Sodium: {meal['sodium_sum']} mg, Carbs: {meal['carbs_sum']} g, Fiber: {meal['fiber_sum']} g, Total Sugar: {meal['sugars_sum']} g")
else:
    st.write("No meals recorded for this date.")
