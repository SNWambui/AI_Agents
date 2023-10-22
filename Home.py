import streamlit as st
from pages import AI_Agents, About, Perform_Task

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
st.header("Welcome to our application!")
st.write("Here's how our app works: Navigate to the AI Agents page to ask\
         an agent to complete a specific task ")
