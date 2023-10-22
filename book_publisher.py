"""
An agent that writes children's books and publishes to Kindle
"""

import streamlit as st
from langchain.llms import OpenAI
from key_config import get_openai_key
import autogen
import sys
import io
import logging

import logging


class CaptureLogs:
    def __init__(self, logger_name=None):
        self.log_output = io.StringIO()
        self.logger = logging.getLogger(logger_name) if logger_name else logging.root

    def __enter__(self):
        self.original_logging_handler = self.logger.handlers[:]
        self.logger.handlers = [logging.StreamHandler(self.log_output)]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.handlers = self.original_logging_handler

    def get_logs(self):
        return self.log_output.getvalue()


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
    role = message["role"]
    content = message["content"]
    if role == "user":
        st.markdown(f"**You**: {content}")
    else:
        st.markdown(f"**Assistant**: {content}")

# The agent's pre-populated instruction
agent_instruction = ("Write me a children's book and publish it to Kindle. No need to execute code. Outline how you "
                     "would do it.")

# Use chat input widget to ask the user about the book topic
book_topic = st.chat_input("What would you like the book to be about?")
if book_topic:
    st.session_state.messages.append({"role": "user", "content": book_topic})
    st.markdown(f"**You**: {book_topic}")

    if not openai_api_key.startswith('sk-'):
        st.warning('Please ensure your OpenAI API key is set correctly!', icon='⚠')
    else:
        planner, assistant, user_proxy = setup_agents()
        combined_message = f"{agent_instruction} The topic is: {book_topic}."

        # Display a status indicating the assistant is processing the message
        with st.status("Grinding for you 🛠️⚙️..."):
            # Capture both console and logging outputs
            with CaptureLogs("autogen") as log_catcher:
                user_proxy.initiate_chat(assistant, message=combined_message)
                logs = log_catcher.get_logs()

            # Display the captured logs in Streamlit inside a box
            if logs.strip():
                st.info(f"Logs:\n\n{logs.strip()}")

            response_from_assistant = user_proxy.last_message()["content"]
            st.session_state.messages.append({"role": "assistant", "content": response_from_assistant})

            st.markdown(f"**Assistant**: {response_from_assistant}")