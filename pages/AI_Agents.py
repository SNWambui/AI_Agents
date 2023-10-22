import streamlit as st
from streamlit_extras.switch_page_button import switch_page



# def app():
st.title("AI Agents")

# checking whether an agent has already been added
if "agents" not in st.session_state:
        st.session_state["agents"] = []

if st.button("GPT Model 1"):
    st.session_state['card_title'] = 'GPT Model 1'
    st.session_state['agent_goal'] = 'Goal of AI Agent 1'
    st.write("Redirecting to Tasks Page...")
    # st.write('# form page', unsafe_allow_html=True)
    st.session_state['page'] = "Perform Task"
    switch_page("Perform Task")
    # ... redirect to form page

# pip install streamlit-extras Clear the redirection state after use

if st.button("GPT Model 2"):
    st.session_state['card_title'] = 'GPT Model 2'
    st.session_state['agent_goal'] = 'Goal of AI Agent 2'
    st.write("Redirecting to Tasks Page...")
    # st.write('# form page', unsafe_allow_html=True)
    st.session_state['page'] = "Perform Task"
    switch_page("Perform Task")

if st.button("GPT Model 3"):
    st.session_state['card_title'] = 'GPT Model 3'
    st.session_state['agent_goal'] = 'Goal of AI Agent 3'
    st.write("Redirecting to Form Page...")
    # st.write('# form page', unsafe_allow_html=True)
    st.session_state['page'] = "Perform Task"
    switch_page("Perform Task")

if st.button("Add An Agent"):
    with st.form(key='add_agent'):
        default_input = st.text_input("AI Agent")
        user_input = st.text_input("Agent goal")
        submit_button = st.form_submit_button(label='Submit')
        if submit_button and user_input:
            st.session_state['card_title'] = f"{default_input}"
            st.session_state['agent_goal'] = f"{user_input}"
            st.write("Adding new agent...")
            st.session_state['page'] = "AI Agents"
#             st.session_state['agents'].append({
#                     'card_title': f"{default_input}",
#                     'agent_goal': f"{user_input}",
#                 })
#             st.write("Adding new agent...")

# for i, agent in enumerate(st.session_state["agents"]):
#     if st.button(agent['card_title'], key=f'btn_{i}'):
#         st.session_state['card_title'] = agent['card_title']
#         st.session_state['agent_goal'] = agent['agent_goal']
#         st.write(f"Selected Agent: {agent['card_title']}")
