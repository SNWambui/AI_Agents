import streamlit as st

# def app():
st.title("Agent Tasks")

card_title = st.session_state.get('card_title', 'Default Card Title')
agent_goal = st.session_state.get('agent_goal', 'Default Agent Goal')

st.write(f"{card_title}")
st.write(f"{agent_goal}")

# Form for user input
with st.form(key='form'):
    default_input = st.text_input("AI Agent", f"{card_title}")
    user_input = st.text_input(label='Your Objective')
    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        # replace this with the logic for an agent
        st.write(f"You submitted: {user_input}")

        # agent_model(user_input)

# need to make this dynamic: thinking of writing a function 
# that takes in the model as an input and outputs the result of the model
# for example, this then allows to reuse the form
# def agent_model(agent, user_input):
#     model = LLL(get_api_key)
#     st.info(model(user_input))
    