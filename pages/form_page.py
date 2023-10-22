import streamlit as st

# def app():
st.title("Form Page")

card_title = st.session_state.get('card_title', 'Default Card Title')
agent_goal = st.session_state.get('agent_goal', 'Default Agent Goal')

st.write(f"Card Title: {card_title}")
st.write(f"AI Agent Goal: {agent_goal}")

# Form for user input
with st.form(key='form'):
    user_input = st.text_input(label='Your Input')
    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.write(f"You submitted: {user_input}")
