import pickle
# Load the list of links
with open('food_db.pkl', 'rb') as f:
    food_db = pickle.load(f)
# Print the list of links
for (city, food_type, doc) in food_db:
    print(city, food_type, doc)
    print ("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")