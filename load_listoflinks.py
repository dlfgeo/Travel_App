# load file list_of_links.pkl
# This file contains a list of tuples (city, food_type, link) that can be used to generate prompts for the user to ask the chatbot.
# Do the imports
import pickle
# Load the list of links
with open('list_of_links.pkl', 'rb') as f:
    list_of_links = pickle.load(f)
# Print the list of links
print(list_of_links)