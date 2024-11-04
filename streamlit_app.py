import streamlit as st
from openai import OpenAI
from langchain.chat_models import ChatOpenAI


openai_api_key = st.secrets["MyOpenAIKey"]
chat = ChatOpenAI(openai_api_key=openai_api_key)

st.title("Trip Review Chatbot")
st.write("This is a simple chatbot to record and analyze your the experience of your most recent trip")

if prompt := st.text_input("Share with us your experience of the latest trip:"):

    review_system_template = """You are an expert professional customer service representative for an airline company.
        From the following customer review text, determine whether the sentiment of the customer is positive or negative.

        Do not respond with more than one word.

        Customer Review:
        {review}

        """

    flight_review_chain = (
        PromptTemplate.from_template(review_system_template)
        | llm
        | StrOutputParser()
    )

    output = full_chain.invoke({"review": prompt})
    st.write(output)

#     Handling Negative Experiences Caused by the Airline

# If the app detects that:
# The user had a negative experience, and
# The cause of their dissatisfaction is the airline's fault (e.g., lost luggage),
# Then, the app should display a message offering sympathies and inform the user that customer service will contact them soon to resolve the issue or provide compensation. (5 Points)
# Handling Negative Experiences Beyond the Airline's Control

# If the app detects that:
# The user had a negative experience, and
# The cause of their dissatisfaction is beyond the airline's control (e.g., a weather-related delay),
# Then, the app should offer sympathies but explain that the airline is not liable in such situations. (5 Points)
# Handling Positive Experiences

# If the user's experience is positive, the app should thank them for their feedback and for choosing to fly with the airline. (5 Points)
# Make sure the agent's responses sound acceptable (e.g., professional, to the point, etc.)