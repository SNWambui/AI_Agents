import streamlit as st
from pages import home, card_page, form_page

# PAGES = {
#     "Home": home,
#     "Card Page": card_page,
#     "Form Page" : form_page
# }

# st.sidebar.title('Navigation')
# selection = st.sidebar.radio("Go to", list(PAGES.keys()))
# page = PAGES[selection]
# page.app()
st.title("Home")
st.write("Welcome to our application!")
st.write("Here's how our app works: ...")
