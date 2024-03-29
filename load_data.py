"""
Script used to load your documents and ingest the text and vector embeddings, in a MongoDB collection.
"""

from langchain_community.document_loaders import DirectoryLoader
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient

from key_param import MONGO_URI
from key_param import OPENAI_API_KEY

if __name__ == "__main__":
    # set the MongoDB URI
    client = MongoClient(MONGO_URI)
    # set the database
    dbName = "langchain_demo"
    # set the collection name
    collectionName = "collection_of_text_blobs"
    # create the collection
    collection = client[dbName][collectionName]

    # initialize the DirectoryLoader
    loader = DirectoryLoader("./sample_files", glob="./*.txt", show_progress=True)
    data = loader.load()

    # define the OpenAI Embedding Model we want to use for the source data
    # the embedding model is different from the language generation model
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # initialize the VectorStore
    # vectorise the text from the documents using the specified embedding model, and insert them
    # into the specified MongoDB collection
    vectorStore = MongoDBAtlasVectorSearch.from_documents(data, embeddings, collection=collection)
