"""
An agent that writes children's books and publishes to Kindle
"""

import streamlit as st
from langchain.llms import OpenAI
from key_config import get_openai_key
import autogen

st.title('🦜🔗 Book Publisher')

# Load the OpenAI Key
try:
    openai_api_key = get_openai_key()
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

    planner_user = autogen.UserProxyAgent(name="planner_user", max_consecutive_auto_reply=0, human_input_mode="NEVER")

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
        code_execution_config={"work_dir": "planning", "enabled": False},
        function_map={"ask_planner": ask_planner},
    )

    return planner, assistant, user_proxy

# Initialize chat session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# The agent's pre-populated instruction
agent_instruction = ("Write me a children's book and publish it to Kindle. No need to execute code. Outline how you "
                     "would do it.")

# Use chat input widget to ask the user about the book topic
book_topic = st.chat_input("What would you like the book to be about?")
if book_topic:
    st.session_state.messages.append({"role": "user", "content": book_topic})
    with st.chat_message("user"):
        st.markdown(book_topic)

    if not openai_api_key.startswith('sk-'):
        st.warning('Please ensure your OpenAI API key is set correctly!', icon='⚠')
    else:
        planner, assistant, user_proxy = setup_agents()
        combined_message = f"{agent_instruction} The topic is: {book_topic}."
        user_proxy.initiate_chat(assistant, message=combined_message)

        response_from_assistant = user_proxy.last_message()["content"]
        st.session_state.messages.append({"role": "assistant", "content": response_from_assistant})

        with st.chat_message("assistant"):
            st.markdown(response_from_assistant)
