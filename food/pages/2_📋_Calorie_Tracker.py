# pages/2_Calorie_Tracker.py

import streamlit as st
from utils import format_number

st.set_page_config(
    page_title="Calorie Tracker",
    page_icon="📋",
    layout="wide",
)

st.title("Calorie Tracker 📋")

# Check if total nutritional sums are available from Page 1
if 'calorie_sum' in st.session_state:
    # Retrieve the total nutritional values from session state
    calorie_sum = st.session_state['calorie_sum']
    fat_sum = st.session_state['fat_sum']
    cholesterol_sum = st.session_state['cholesterol_sum']
    sodium_sum = st.session_state['sodium_sum']
    carbs_sum = st.session_state['carbs_sum']
    fiber_sum = st.session_state['fiber_sum']
    sugars_sum = st.session_state['sugars_sum']
    protein_sum = st.session_state['protein_sum']
    vitamin_a_sum = st.session_state['vitamin_a_sum']
    vitamin_c_sum = st.session_state['vitamin_c_sum']
    vitamin_d_sum = st.session_state['vitamin_d_sum']
    vitamin_b12_sum = st.session_state['vitamin_b12_sum']
    calcium_sum = st.session_state['calcium_sum']
    iron_sum = st.session_state['iron_sum']
    potassium_sum = st.session_state['potassium_sum']

    # Display a summary of the total nutrition for all analyzed foods
    st.subheader("Total Nutritional Information for the Day")

    # Display the totals in an expander or directly
    with st.expander("Nutritional Information", expanded=True):
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

    if st.button("Add information to your nutrition log"):
        st.session_state.nutrition_info = {}

else:
    st.info("Please analyze food items on the 'Food Analysis' page first.")
