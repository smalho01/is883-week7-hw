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

    review_system_template = """You are an expert customer service representative for an airline company.
        From the following customer review text, determine whether the sentiment of the customer is positive or negative.
        If the review is negative, determine if the negativity was caused by the airline or if it was out of the airline's control. 
        Your output should be one of three responses: 
            - "positive" if the review was positive or neutal 
            - "negative - airline" if the review was negative and the airline's fault
            - "negative - other" if the review was negative and out of the airlines contorl

        Do not respond with more than one simple string accoridng to the three options in quotes above.

        Customer Review:
        {review}

        """

    flight_review_chain = (
        PromptTemplate.from_template(review_system_template)
        | llm
        | StrOutputParser()
    )

    review_system_positive_template = """You are an expert customer service representative for an airline company.
    Based on the following customer review text, you should thank them for their feedback and for choosing to fly with the airline.

    Your response should follow these guidelines:
    1. Thank them for their feedback 
    2. Thank them for flying with our airline
    3. Respond to their feedback with a personal conversational message regarding their specifics of the feedback, addessing the customer directly.
    4. The response should end with "Regards, Arnold Chatbot"    

    Customer Review:
    {review}

    """

    flight_positive_review_chain = (
        PromptTemplate.from_template(review_system_positive_template)
        | llm
    )

    review_system_negative_airline_template =  """You are an expert customer service representative for an airline company.
    Based on the following customer review text, you should display a message offering sympathies and inform the user that customer service will contact them soon to resolve the issue or provide compensation.

    Your response should follow these guidelines:
    1. Offet sympathies
    2. Inform the user that customer service will contact them soon to resolve the issue or provide compensation
    3. Respond to their feedback with a personal conversational message regarding their specifics of the feedback, addessing the customer directly.
    4. The response should end with "Regards, Arnold Chatbot"    

    Customer Review:
    {review}

    """

    flight_negative_airline_review_chain = (
        PromptTemplate.from_template(review_system_negative_airline_template)
        | llm
    )

    review_system_negative_other_template = """You are an expert customer service representative for an airline company.
    Based on the following customer review text, you should display a message offering sympathies but explain that the airline is not liable in such situations. (5 Points)

    Your response should follow these guidelines:
    1. Offer sympathies
    2. Explain that the airline is not liable in such situations
    3. Respond to their feedback with a personal conversational message regarding their specifics of the feedback, addessing the customer directly.
    4. The response should end with "Regards, Arnold Chatbot"    

    Customer Review:
    {review}

    """

    flight_negative_other_review_chain = (
        PromptTemplate.from_template(review_system_negative_other_template)
        | llm
    )

    branch_sentiment_analysis = RunnableBranch(
        (lambda x: "negative - airline" in x["sentiment"].lower(), flight_negative_airline_review_chain),
        (lambda x: "negative - other" in x["sentiment"].lower(), flight_negative_other_review_chain),
        flight_positive_review_chain,
    )

    full_chain = {"sentiment": flight_review_chain, "review": lambda x: x["review"]} | branch_sentiment_analysis

    output = full_chain.invoke({"review": prompt})
    st.markdown(output)
