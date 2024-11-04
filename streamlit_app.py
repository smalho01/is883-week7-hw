import streamlit as st
from openai import OpenAI
from langchain.chat_models import ChatOpenAI


openai_api_key = st.secrets["MyOpenAIKey"]

### Create a ChatOpenAI object
chat = ChatOpenAI(openai_api_key=openai_api_key)

import streamlit as st
from transformers import GPT2LMHeadModel, AutoTokenizer

model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

st.title("Trip Review Chatbot")
st.write("This is a simple chatbot to record and analyze your most recent trip")

prompt = st.text_input("Share with us your experience of the latest trip:")

if st.button("Generate Response"):
    input = tokenizer.encode(prompt, return_tensors='pt')

    high_creativity_response = tokenizer.decode(model.generate(input, max_length=token_length, num_return_sequences=1, temperature=0.7, do_sample=True)[0])
    st.subheader("High Creativity Response:")
    st.write(high_creativity_response)

    low_creativity_response = tokenizer.decode(model.generate(input, max_length=token_length, num_return_sequences=1, temperature=0.3, do_sample=True)[0])
    st.subheader("Predictable Response:")
    st.write(low_creativity_response)