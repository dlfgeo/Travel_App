from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.vectorstores import FAISS
#from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
import os
os.environ['OPENAI_API_KEY'] = "OPENAI_API_KEY"


#load_dotenv()
# llm = OpenAI(temperature=0.7)
# names = llm("I have a dog pet and I need a traditional name suggestion for it. Please give me 5 traditional dog names")
# print(names)

#video_url = "https://www.youtube.com/watch?v=Z2fjZleein4"
embeddings = OpenAIEmbeddings()
def create_db(video_url):
    loader = YoutubeLoader.from_youtube_url(video_url)
    transcript = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=100)
    docs = splitter.split_documents(transcript)
    db = FAISS.from_documents(docs,embeddings)
    return db

def get_response_from_query(db, query,k=1):
    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])
    llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.7)
    prompt = PromptTemplate(
        input_variables = ["question", "docs"],
        template = """
        You are a helpful YouTube assistant that can answer questions about the video based on the video's transcript.
        Answer the following question: {question}
        By searching the following video transcript: {docs}
        
        Only use the factual information from the transcript to answer the question. Be conscise.
        """
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(question=query, docs=docs_page_content)
    return response

food_db = []

import pickle
# Load the list of links
with open('list_of_links.pkl', 'rb') as f:
    list_of_links = pickle.load(f)
# Process each link and save to food_db
for (city, food_type, videoID) in list_of_links:
    try:
        link = f"https://www.youtube.com/watch?v={videoID}"
        db = create_db(link)
        doc = get_response_from_query(db, "Provide a list of restaurants mentioned in this video. For each of the restaurants, provide a short description of why someone may want to go there. Only provide a list with no other words at the start or end.")
        food_db.append((city, food_type, doc))
    except:
        doc = "Sorry, I don't have any recommendations on this."
        food_db.append((city, food_type, doc))
        print(city," ", food_type)

# Save food_db to a file via pickle
with open('food_db.pkl', 'wb') as f:
    pickle.dump(food_db, f)
