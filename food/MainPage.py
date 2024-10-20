import streamlit as st
import streamlit.components.v1 as components

# Function to load local CSS file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the first CSS file
local_css("https://raw.githubusercontent.com/ThienAn783/dope/main/index.css")

# Load the second CSS file
local_css("https://raw.githubusercontent.com/ThienAn783/dope/main/nicepage.css")

# Load HTML content from the external HTML file (index.html)
with open("https://raw.githubusercontent.com/ThienAn783/dope/main/index.html", "r", encoding='utf-8') as html_file:
    html_content = html_file.read()

# Use components.html to display the HTML content
components.html(html_content, height=1200, scrolling=True)

# Optionally, you can include additional Streamlit elements if needed
st.write("Streamlit app is working with external HTML and CSS files.")
