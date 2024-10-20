# pages/3_📖_Recipes.py

import streamlit as st
import requests
import os

st.title("Recipes 📖")

# SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')
SERPAPI_API_KEY = '5312ce5c5c97a3ff70fe04fcf1e49d7e38039018892ceec45dbb0798c200137a'

if not SERPAPI_API_KEY:
    st.error("SERPAPI_API_KEY environment variable not set.")
    st.stop()

# Check if analyzed foods are available from Page 1
if 'analyzed_foods' in st.session_state and st.session_state['analyzed_foods']:
    # Get all the analyzed food items from Page 1
    food_options = [food['display_name'] for food in st.session_state['analyzed_foods']]
    
    # Allow the user to select one or more ingredients to find recipes for
    selected_foods = st.multiselect("Select ingredients to find recipes for:", food_options, default=food_options)

    # Join selected ingredients into a single query string for the recipe search
    query_string = ", ".join(selected_foods)

    st.write(f"Showing recipes for: **{query_string}**.")

    # Get recipe suggestions based on the selected ingredients
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

    # Display recipe links for the selected ingredients
    if "organic_results" in results:
        st.subheader("Recipe Results")
        for result in results["organic_results"][:5]:
            title = result.get("title")
            link = result.get("link")
            if title and link:
                st.markdown(f"- [{title}]({link})")
    else:
        st.write("No recipes found for the selected ingredients.")

    # Optional: Add more filters, like food allergies
    show_food_allergies = st.checkbox("Do you want to specify any food allergies?")

    allergy_string = ""
    if show_food_allergies:
        food_allergies = st.multiselect(
            "Select your food allergies (if any):",
            options=["Nuts", "Dairy", "Gluten", "Eggs", "Shellfish", "Soy", "Wheat"],
        )
        # Build the allergy filter string
        if food_allergies:
            allergy_string = " without " + " and ".join(food_allergies)

    # Additional user input for custom recipe search
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

        # Display recipe links for the additional user search
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
