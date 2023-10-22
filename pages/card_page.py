import streamlit as st
from streamlit_extras.switch_page_button import switch_page



# def app():
st.title("Card Page")

if st.button("GPT Model 1"):
    st.session_state['card_title'] = 'Card 1 Title'
    st.session_state['agent_goal'] = 'Goal of AI Agent 1'
    st.write("Redirecting to Form Page...")
    # st.write('# form page', unsafe_allow_html=True)
    st.session_state['page'] = 'form page'
    switch_page("form page")
    # ... redirect to form page

# pip install streamlit-extras Clear the redirection state after use

if st.button("GPT Model 2"):
    st.session_state['card_title'] = 'Card 2 Title'
    st.session_state['agent_goal'] = 'Goal of AI Agent 2'
    st.write("Redirecting to Form Page...")
    # st.write('# form page', unsafe_allow_html=True)
    st.session_state['page'] = 'form page'
    switch_page("form page")

if st.button("GPT Model 3"):
    st.session_state['card_title'] = 'Card 3 Title'
    st.session_state['agent_goal'] = 'Goal of AI Agent 3'
    st.write("Redirecting to Form Page...")
    # st.write('# form page', unsafe_allow_html=True)
    # st.session_state['page'] = 'form page'
    switch_page("form page")
