import streamlit as st
from langchain.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import boto3

# Initialize Bedrock client
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'  # replace with your preferred region
)

# Initialize Claude model
llm = Bedrock(
    model_id="anthropic.claude-v2",
    client=bedrock_runtime,
    model_kwargs={"max_tokens_to_sample": 500}
)

# Create a prompt template
prompt_template = PromptTemplate(
    input_variables=["topic"],
    template="Human: Write a short paragraph about {topic}. \n \nAssistant:"
)

# Create an LLMChain
chain = LLMChain(llm=llm, prompt=prompt_template)

# Streamlit app
st.title("Claude on Amazon Bedrock Demo")

# User input
topic = st.text_input("Enter a topic:")

if topic:
    # Generate response
    response = chain.run(topic)
    
    # Display response
    st.write(response)