
import streamlit as st
#from openai import OpenAI
from langchain_openai import OpenAI

st.title(f'\u2708 Travel App')

#load fooddb from file
import pickle
f = open('food_db.pkl', 'rb')
food_db = pickle.load(f)

openai_api_key = st.text_input('OpenAI API Key', type='password')

#Basic LLM Call
def generate_response(input_text):
    llm = OpenAI(temperature=0.1, openai_api_key=openai_api_key,max_tokens=-1)
    generated_text = llm.invoke(input_text)
    st.session_state['generated_text'] = generated_text


with st.form('my_form'):
    city_to_visit = st.selectbox(
        'What city will you be visiting?',
        ('London', "New York City", "Paris", "Munich", "Toronto", "Vancouver", "Berlin", "Karachi", "Edinburgh", "Cairo", "San Francisco", "Beijing", "Dubai", "Rome"),
        index=None,
        placeholder="Select a city...")

    travel_interests = st.multiselect(
        'What are your interests?',
        ["History", "Art", "Theatre", "Live Music", "Shopping", "Museums", "Iconic Landmarks", "Nature", "Relaxation"],
        [])

    submitted = st.form_submit_button('Submit')
    text = ""
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submitted and  city_to_visit!= None and openai_api_key.startswith('sk-') and not 'generated_text' in st.session_state:
        prompt = f"""You are a helpful assistant that provides travel suggestions for a desired city based on 
        a user's interests. Provide a list of up to 10 attractions in the {city_to_visit} for someone interested in {travel_interests}. For each item in the list, provide a short description about the attraction."""
        generate_response(prompt)
    if 'generated_text' in st.session_state:
        generated_text = st.session_state['generated_text']
        st.info(generated_text)

st.divider()

favfood = st.radio('What kind of restaurants are you interested in?',
    ('Pizza', 'Burgers', 'Fast Food', 'Upscale Restaurant'), index=None,
                   disabled = ('generated_text' not in st.session_state)
    )
if favfood == "Pizza" or favfood == "Burgers" or favfood == "Fast Food" or favfood == "Upscale Restaurant":
    # find matching review in food_db given city_to_visit and favfood
    for (city, food_type, doc) in food_db:
        if city == city_to_visit and food_type == favfood:
            st.write(doc)

