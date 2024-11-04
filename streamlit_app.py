import streamlit as st
from openai import OpenAI
from langchain.chat_models import ChatOpenAI


openai_api_key = st.secrets["MyOpenAIKey"]

### Create a ChatOpenAI object
chat = ChatOpenAI(openai_api_key=openai_api_key)

st.title("Trip Review Chatbot")
st.write("This is a simple chatbot to record and analyze your most recent trip")

if prompt := st.chat_input("Share with us your experience of the latest trip:"):

    print(prompt)