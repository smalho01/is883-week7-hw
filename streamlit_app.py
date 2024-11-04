import streamlit as st
from openai import OpenAI
from langchain.llms import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch

openai_api_key = st.secrets["MyOpenAIKey"]
llm = OpenAI(openai_api_key=openai_api_key)

st.title("Trip Review Chatbot")
st.write("This is a simple chatbot to record and analyze your the experience of your most recent trip")

if prompt := st.text_input("Share with us your experience of the latest trip:"):

    review_system_template = """You are an expert customer service representative for an airline company called Sahil's Speedy Service. Your name is Arnold.
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

    review_system_negative_base_template = """You are an expert customer service representative for an airline company called Sahil's Speedy Service. Your name is Arnold.
        From the following customer review text, determine whether the negativity of the review is the airline's fault or not.

        Do not provide any justifcation for who's fault it is and answer simply with only one word. 
        It the negativity in the review is the airline's fault, you should output "airline", otherwise you should ouput "other".

        Customer Review:
        {review}

        """

    flight_negative_base_review_chain = (
        PromptTemplate.from_template(review_system_negative_base_template)
        | llm
    )

    review_system_positive_base_template = """You are an expert customer service representative for an airline companycalled Sahil's Speedy Service. Your name is Arnold.
    Based on the following customer review text, you should thank them for their feedback and for choosing to fly with the airline.

    Your response should follow these guidelines:
    1. Thank them for their feedback 
    2. Thank them for flying with our airline
    3. Respond to their feedback with a personal conversational message regarding their specifics of the feedback, addessing the customer directly.
    

    Customer Review:
    {review}

    """

    flight_positive_base_review_chain = (
        PromptTemplate.from_template(review_system_positive_base_template)
        | llm
    )

    branch_sentiment_analysis = RunnableBranch(
        (lambda x: "negative" in x["sentiment"].lower(), flight_negative_base_review_chain),
        flight_positive_base_review_chain,
    )

    full_chain = {"sentiment": flight_review_chain, "review": lambda x: x["review"]} | branch_sentiment_analysis

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