import os
import json
import streamlit as st
from streamlit_calendar import calendar

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

def main():
    st.title("Fooddiary - View Your Calorie Calendar")

    if 'user_id' not in st.session_state:
        user_id_input = st.text_input("Enter your User ID to proceed:", key="user_id_input")
        if st.button("Submit"):
            if user_id_input:
                st.session_state['user_id'] = user_id_input
                st.experimental_rerun()
            else:
                st.warning("Please enter your User ID.")

    if 'user_id' in st.session_state:
        user_id = st.session_state['user_id']
        st.success(f"Logged in as: {user_id}")

        user_data = load_user_data(user_id)

        calendar_events = []
        calories_by_date = {}

        for entry in user_data.get('analyzed_foods', []):
            date = entry.get('date')
            mealname = entry.get('mealname')
            calories = entry.get('calorie_sum', 0)

            if date and mealname:
                if date not in calories_by_date:
                    calories_by_date[date] = 0
                calories_by_date[date] += calories

        for date, total_calories in calories_by_date.items():
            calendar_events.append({
                "title": f"Total Calories: {total_calories:.2f} kcal",
                "start": f"{date}T00:00:00",
                "end": f"{date}T23:59:59",
            })

        calendar_options = {
            "editable": False,
            "selectable": True,
            "initialView": "dayGridMonth",
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "dayGridMonth,timeGridWeek"
            },
            "events": calendar_events,
        }

        st.write(calendar(events=calendar_events, options=calendar_options))

        if "selected_date" in st.session_state:
            selected_date = st.session_state.selected_date
            if selected_date in user_data.get("calories", {}):
                st.write(f"Nutrition details for {selected_date}:")
                for meal in user_data["calories"][selected_date]["nutrition"]:
                    st.write(f"**Meal:** {meal['mealname']}")
                    st.write(f"Calories: {meal['calories']} kcal")
                    st.write(f"Protein: {meal['protein']} g")
                    st.write(f"Fat: {meal['fat']} g")
                    st.write(f"Cholesterol: {meal['cholesterol']} mg")
                    st.write(f"Sodium: {meal['sodium']} mg")
                    st.write(f"Carbohydrates: {meal['carbs']} g")
                    st.write(f"Fiber: {meal['fiber']} g")
                    st.write(f"Sugars: {meal['sugars']} g")
            else:
                st.write(f"No data available for {selected_date}.")
        else:
            if len(calories_by_date) == 0:
                st.write("No data available yet. Please add some calorie entries.")
            else:
                st.write("Select a day to view detailed nutrition info.")

if __name__ == "__main__":
    main()
