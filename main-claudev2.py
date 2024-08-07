
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_aws import BedrockLLM
import boto3
import time
import os
import streamlit as st


os.environ["AWS_PROFILE"] ="terraform-user"

#bedrock client

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

model_id = "anthropic.claude-v2"

llm = BedrockLLM(
    model_id=model_id,
    client=bedrock_client,
    model_kwargs={"max_tokens_to_sample": 2000, "temperature": 1}
    
)

def my_chatbot(language, freeform_text):
    prompt = PromptTemplate(
        input_variables=["language", "freeform_text"],
        template="You are a chatbot. You are in {language}.\n\n{freeform_text}"
    )
    
    bedrock_chain = LLMChain(llm=llm, prompt=prompt)
    
    response=bedrock_chain({'language': language, 'freeform_text': freeform_text })
    
    return response

# print(my_chatbot("English", "Who is Buhda"))

def text_generator(text, chunk_size=50):
    for i in range(0, len(text), chunk_size):
        yield text[i:i+chunk_size]
        time.sleep(0.1)


st.title("Tims Chatbot")

language = st.sidebar.selectbox("language", ["english", "spanish", "german", "manderin"])

if language:
    freeform_text = st.sidebar.text_area(label="what is your question?", max_chars=100)
    
if freeform_text:
    response = my_chatbot(language,freeform_text)
    st.write_stream(text_generator(response['text']))
    
 