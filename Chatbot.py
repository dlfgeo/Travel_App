
import os
import streamlit as st
from openai import OpenAI
from llama_index.core import VectorStoreIndex, SummaryIndex, Settings, SimpleDirectoryReader
from langchain.llms import OpenAI
from llama_index.llms.openai import OpenAI

#from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader, SummaryIndex
 
st.title(f'\u2708 Travel App')

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
os.environ["OPENAI_API_KEY"] = openai_api_key
#Future Requirement Need an ingestion pipeline to pull data and refresh the RAG model: https://docs.llamaindex.ai/en/stable/module_guides/loading/ingestion_pipeline/root.html

#RAG Model for locations that we're tracking

def generate_response_RAG(input_text):
    #Settings.llm = OpenAI(temperature=0.1, api_key=openai_api_key) # could input this parameter: model="gpt-4",
    documents = SimpleDirectoryReader("./").load_data("London_Wikipedia.rtf") #include other data sources as they become available
    documents = SimpleDirectoryReader("./").load_data("NYC_Wikipedia.rtf") #include other data sources as they become available
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()   
    response = query_engine.query(input_text)
    st.info(response)
  
#Basic LLM Call for locations where we don't have data. 
def generate_response(input_text):
    llm = OpenAI(temperature=0.1, openai_api_key=openai_api_key)
    st.info(llm(input_text))

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
         generate_response_RAG(text)
        #if city == 'London': #write code to pass it into the London data store before calling the LLM
          #generate_response_RAG(text)  #call the generic LLM function
        #elif city == 'NYC':  #write code to pass it into the London data store before calling the LLM
          #generate_response_RAG(text)  #call the generic LLM function
        #else:
          #generate_response_RAG(text)  
            
        
        
