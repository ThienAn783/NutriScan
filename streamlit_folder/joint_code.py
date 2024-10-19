import altair as alt
import pandas as pd
import streamlit as st
import requests 


# Show the page title and description.
st.set_page_config(page_title="Food", page_icon="🎬")
st.title("FOOD")
import requests

API_KEY = 'n8DXzZmNroJ4Wew6OkGKwoubDTdsee7VlSPY5huK'
def format_number(value):
    if value is not None:
        formatted = f"{value:.10f}"
        return f"{formatted.rstrip('0').rstrip('.')}"
    else:
        value = '0'
        return value
#accessing api for food vision
url = "https://vision.foodvisor.io/api/1.0/en/analysis/"
headers = {"Authorization": "Api-Key t0tXlgF3.lJFuSecTKimVxvGYqlgIPULTfzV1QyAz"}
with open("food.jpg", "rb") as image:
  response = requests.post(url, headers=headers, files={"image": image})
  response.raise_for_status()
data = response.json()

display_name = data["items"][0]["food"][0]["food_info"]["display_name"]
nutrition = data["items"][0]["food"][0]["food_info"]["nutrition"]

st.image('food.jpg', caption='Uploaded Food Image', use_column_width=True)
#creating the image
with st.expander("Nutritional Information"):
    st.write("**Serving Size:** 100 g")
    st.write(f"**Calories:** {format_number(nutrition['calories_100g'])} kcal")
    st.write(f"**Total Fat:** {format_number(nutrition['fat_100g'])} g")
    st.write(f"  - **Saturated Fat:** {format_number(nutrition['sat_fat_100g'])} g")
    st.write(f"  - **Trans Fat:** {format_number(nutrition['sugars_100g'])} g")
    st.write(f"**Cholesterol:** {format_number(nutrition['cholesterol_100g'])} mg")
    st.write(f"**Sodium:** {format_number(nutrition['sodium_100g'])} mg")
    st.write(f"**Total Carbohydrates:** {format_number(nutrition['carbs_100g'])} g")
    st.write(f"  - **Dietary Fiber:** {format_number(nutrition['fibers_100g'])} g")
    st.write(f"  - **Total Sugars:** {format_number(nutrition['sugars_100g'])} g")
    st.write(f"**Protein:** {format_number(nutrition['proteins_100g'])} g")
    if st.checkbox("Expand to see Vitamins"):
        st.write(f"**Vitamin A:** {format_number(nutrition['vitamin_a_retinol_100g'])} µg")
        st.write(f"**Vitamin C:** {format_number(nutrition['vitamin_c_100g'])} mg")
        st.write(f"**Vitamin D:** {format_number(nutrition['vitamin_d_100g'])} µg")
        st.write(f"**Vitamin B12:** {format_number(nutrition['vitamin_b12_100g'])} µg")
    if st.checkbox("Expand to see Minerals"):
        st.write(f"**Calcium:** {format_number(nutrition['calcium_100g'])} mg")
        st.write(f"**Iron:** {format_number(nutrition['iron_100g'])} mg")
        st.write(f"**Potassium:** {format_number(nutrition['potassium_100g'])} mg")

# function for taking in user input and searching it on the web
def search_user_input():
    user_input = st.text_input("You: ", "")

    if user_input:
        user_message = user_input.lower()

        params = {
        "q": display_name + user_message,
        "location": "United States",
        "hl": "en",
        "gl": "us",
        "api_key": "5312ce5c5c97a3ff70fe04fcf1e49d7e38039018892ceec45dbb0798c200137a"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        for result in results["organic_results"]:
            title = result["title"]
            link = result["link"]
            link_text = title
            search_url = link
            st.markdown(f"[{link_text}]({search_url})")

search_user_input()
