import streamlit as st
from langchain.llms import OpenAI

st.title(f'\u2708 Travel App')

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

def generate_response(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    st.info(llm(input_text))

#Add a radio button option to provide context for the location. This will also help to route the prompt to the appropriate RAG path
#Add a date option as well to preset the prompt.
with st.sidebar:
   city =  st.radio("Where Are You travelling?:sunglasses:", ['London', 'NYC'])
   d1 = st.date_input("Travel Start Date", value="today")
   d2 = st.date_input("Travel End Date", value="today")

with st.form('my_form'):
    text = st.text_area('Enter text:', f'I\'m travelling to {city} from {d1} to {d2} and I would like to know more about')
    submitted = st.form_submit_button('Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submitted and openai_api_key.startswith('sk-'):
        generate_response(text)