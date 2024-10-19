import streamlit as st
#Navigation bar

def render_sidebar():
    st.sidebar.title("Navigation")
    home_btn = st.sidebar.button("Home")
    foodscanner_btn = st.sidebar.button("Food Scanner")
    about_btn = st.sidebar.button("About")
    FAQ_btn = st.sidebar.button("FAQ")

    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'Home'

    if home_btn:
        st.title("Home Page")
        st.write("This is the main content of the homepage.")
        
    elif foodscanner_btn:
        st.title("Food Scanner")

    elif about_btn:
        st.title("About Us")
        st.write("")

    elif FAQ_btn:
        st.title()
    else:
        st.title("Home Page")
        st.write("This is the main content of the homepage.")