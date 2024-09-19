import streamlit as st
import boto3
from langchain.llms import Bedrock
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# Initialize Bedrock client
bedrock_client = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'  # Replace with your preferred region
)

# Initialize Bedrock LLM
llm = Bedrock(
    model_id="amazon.titan-text-express-v1",
    client=bedrock_client,
    model_kwargs={"maxTokenCount": 512, "temperature": 0.7}
)

# Create a prompt template
prompt_template = PromptTemplate(
    input_variables=["topic"],
    template="Write a short paragraph about {topic}."
)

# Create an LLMChain
chain = LLMChain(llm=llm, prompt=prompt_template)

# Streamlit app
st.title("Titan Text G1 - Express Demo")

# User input
topic = st.text_input("Enter a topic:")

if topic:
    # Generate response
    response = chain.run(topic)
    
    # Display response
    st.write("Generated Response:")
    st.write(response)