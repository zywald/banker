import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from openai.error import OpenAIError

st.title("VIP Client Call Preparation Assistant")

# OpenAI API Key
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# Check if the API key is not empty
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
else:
    # Client information input form
    with st.form("myform"):
        investment_portfolio = st.multiselect('Investment Portfolio', [
                                            'Bonds', 'Gold', 'Tech Stocks', 'Environmental Stocks', 'Commodities', 'Property'])
        city = st.text_input('City')
        age = st.text_input('Age')
        hobbies = st.text_input('Hobbies')
        additional_information = st.text_input('Additional Information')
        submitted = st.form_submit_button("Submit")

        if submitted:
            # Instantiate LLM model
            llm = OpenAI(model_name='gpt-4',
                        openai_api_key=openai_api_key, temperature=0.8)
            try:
                # Define common instructions
                common_instructions = ("You are an expert banking assistant and I am a private banker preparing for a call with one of my VIP clients. Your role is to help me"
                                    "establish a deeper bond with the client during our conversation, making them feel connected and understood as expected by a VIP banking client."
                                    "Task and what your answer should be only giving: Given the following information about a VIP client, provide me with 3 personalized, factual, and detailed topics to assist me in the upcoming call. Each topic should be carefully crafted, relevant, and designed to deepen the personal bond with the client."
                                    "Each topic should begin with a specific question or conversation starter in bold. Following the starter, include two separate subsections: one providing context and background information on the topic at hand, and the other offering guidance on how to follow-up the initial statement or question."
                                    "Remember, as the banker, I am the one who is informed about the performance of his portfolio. It's my responsibility to discuss this, so your suggestions should not include this aspect. We are focusing on creating a connection with the client through shared interests and understanding their situation."
                                    "Avoid bringing up sensitive topics like divorce directly, and be sure to provide enough context about each topic so I won't fall short during the conversation."
                                    )

                # Define specific instructions based on user input
                specific_instructions = f"The client's information provided is as follows: Investment Portfolio - {investment_portfolio}, City - {city}, Age - {age}, Hobbies - {hobbies}, Additional Information - {additional_information}. "

                # Combine common and specific instructions into the prompt
                prompt_query = common_instructions + specific_instructions

                # Run LLM model
                with st.spinner('Generating response...'):
                    response = llm(prompt_query)

                # Print results
                st.markdown(response)
            except OpenAIError as e:
                st.error(f"An OpenAI API error occurred: {str(e)}")
            except Exception as e:
                st.error(f"An unknown error occurred: {str(e)}")
