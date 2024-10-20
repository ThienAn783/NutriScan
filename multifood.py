import altair as alt
import pandas as pd
import streamlit as st
import requests 

def format_number(value):
    if value is not None:
        formatted = f"{value:.10f}"
        return f"{formatted.rstrip('0').rstrip('.')}"
    else:
        value = '0'
        return value

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
