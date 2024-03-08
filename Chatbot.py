

import streamlit as st
#from openai import OpenAI
from langchain.llms import OpenAI

st.title(f'\u2708 Travel App')

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

#Basic LLM Call
def generate_response(input_text):
    
    llm = OpenAI(temperature=0.1, openai_api_key=openai_api_key)
    st.info(llm(input_text))
    
#RAG Model: Write function here
   #May want to look at implementing an Agent for various types of queryies


#Add a radio button option to provide context for the location. This will also help to route the prompt to the appropriate RAG path
#Add a date option as well to preset the prompt.
with st.sidebar:
   city =  st.radio("Where Are You travelling?:sunglasses:", ['London', 'NYC','N/A'])
   if city == 'N/A':
       city = "I\'m travelling"
   else:
       city = "I\'m travelling to " + city
       
   d1 = st.date_input("Travel Start Date", value="today")
   d2 = st.date_input("Travel End Date", value="today")

with st.form('my_form'):
    text = st.text_area('Enter text:', f'{city} from {d1} to {d2} and I would like to know more about')
    submitted = st.form_submit_button('Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submitted and openai_api_key.startswith('sk-'):
        if city == 'London': #write code to pass it into the London data store before calling the LLM
          generate_response(text)  #call the generic LLM function
        elif city == 'NYC':  #write code to pass it into the London data store before calling the LLM
          generate_response(text)  #call the generic LLM function
        else:
          generate_response(text)  
            
        
        
