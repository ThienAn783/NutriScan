import streamlit as st
import requests
import os

st.title("Recipes 📖")
SERPAPI_API_KEY = st.secrets["api_credentials"]["SERPAPI_API_KEY"]
if not SERPAPI_API_KEY:
    st.error("SERPAPI_API_KEY environment variable not set.")
    st.stop()

if 'analyzed_foods' in st.session_state and st.session_state['analyzed_foods']:
    # Safely get the 'display_name', and if not available, skip or provide a default name
    food_options = [food.get('display_name', 'Unknown Food') for food in st.session_state['analyzed_foods']]
    food_options = list(set(food_options))

    selected_foods = st.multiselect("Select ingredients to find recipes for:", food_options, default=food_options)
    query_string = ", ".join(selected_foods)

    st.write(f"Showing recipes for: **{query_string}**.")

    params = {
        "q": f"{query_string} recipe",
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
        st.stop()
    except Exception as err:
        st.error(f"An error occurred: {err}")
        st.stop()

    if "organic_results" in results:
        st.subheader("Recipe Results")
        for result in results["organic_results"][:5]:
            title = result.get("title")
            link = result.get("link")
            if title and link:
                st.markdown(f"- [{title}]({link})")
    else:
        st.write("No recipes found for the selected ingredients.")

    show_food_allergies = st.checkbox("Do you want to specify any food allergies?")

    allergy_string = ""
    if show_food_allergies:
        food_allergies = st.multiselect(
            "Select your food allergies (if any):",
            options=["Nuts", "Dairy", "Gluten", "Eggs", "Shellfish", "Soy", "Wheat"],
        )
        if food_allergies:
            allergy_string = " without " + " and ".join(food_allergies)

    user_input = st.text_input("Search for something specific about these ingredients: ")

    if user_input:
        user_message = user_input.lower()
        params = {
            "q": f"{query_string} {user_message} recipe {allergy_string}",
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
            st.stop()
        except Exception as err:
            st.error(f"An error occurred: {err}")
            st.stop()

        if "organic_results" in results:
            st.subheader("Custom Search Results")
            for result in results["organic_results"][:5]:
                title = result.get("title")
                link = result.get("link")
                if title and link:
                    st.markdown(f"- [{title}]({link})")
        else:
            st.write("No recipes found for your custom search.")
else:
    st.info("Please analyze food items on the 'Food Analysis' page first.")
    st.markdown("[Go to Food Analysis page ➡️](./1_🔍_Food_Analysis)")
