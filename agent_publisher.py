"""
An agent that writes children books and publishes to Kindle
"""

import streamlit as st
from langchain.llms import OpenAI
from key_config import get_openai_key
import autogen

st.title('🦜🔗 Book Publisher')

# Load the OpenAI Key
try:
    openai_api_key = get_openai_key()
    st.write(f"DEBUG OpenAI Key Loaded: {openai_api_key[:5]}...")  # Display the first few characters of the key for debugging
except ValueError as e:
    st.error(str(e))
    openai_api_key = ""


def ask_planner(message, planner, planner_user):
    planner_user.initiate_chat(planner, message=message)
    return planner_user.last_message()["content"]


def setup_agents():
    planner = autogen.AssistantAgent(
        name="planner",
        llm_config={
            "config_list": autogen.config_list_from_json("OAI_CONFIG_LIST.json"),
            "api_key": openai_api_key
        },
        system_message="You are a helpful AI assistant..."
    )

    planner_user = autogen.UserProxyAgent(
        name="planner_user",
        max_consecutive_auto_reply=0,
        human_input_mode="NEVER",
    )

    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config={
            "temperature": 0,
            "request_timeout": 600,
            "seed": 42,
            "model": "gpt-4",
            "config_list": autogen.config_list_openai_aoai(exclude="aoai"),
            "api_key": openai_api_key,
            "functions": [{
                "name": "ask_planner",
                "description": "ask planner to ...",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "question to ask planner...",
                        },
                    },
                    "required": ["message"],
                },
            }],
        }
    )

    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="TERMINATE",
        max_consecutive_auto_reply=10,
        code_execution_config={"work_dir": "planning", "enabled": False}, # disable code execution
        function_map={"ask_planner": ask_planner},
    )

    return planner, assistant, user_proxy


# initialization to set a default state
if 'response' not in st.session_state:
    st.session_state.response = ""

with st.form('my_form'):
    task_desc = st.text_area('Enter your task:', 'Write me a childrens book and publish it to Kindle. Dont execute '
                                                 'code, just outline how you would do it.')
    submitted = st.form_submit_button('Submit')

    if submitted:
        if not openai_api_key.startswith('sk-'):
            st.warning('Please ensure your OpenAI API key is set correctly!', icon='⚠')
        else:
            # Initialize the agents
            planner, assistant, user_proxy = setup_agents()
            st.write("DEBUG Agents set up successfully!")

            # Initiate chat with the assistant
            user_proxy.initiate_chat(assistant, message=task_desc)
            st.write("DEBUG Chat initiated with assistant!")

            # Save the response to the session state
            st.session_state.response = user_proxy.last_message()["content"]
            st.write(f"DEBUG Saved response: {st.session_state.response}")

# Display
if st.session_state.response:
    st.subheader('Response from AI:')
    st.write(st.session_state.response)
else:
    st.write("DEBUG No response saved in session state.")