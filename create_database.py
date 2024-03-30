from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient
from pymongo.collection import Collection

from config import config
from key_param import MONGO_URI
from key_param import OPENAI_API_KEY


class DataStore(object):
    """
    Class for loading documents, splitting text, and ingesting text and vector embeddings into a MongoDB collection.
    """

    def __init__(self, db_name: str, collection_name: str, file_pths: str, chunk_size: int, chunk_overlap: int) -> None:
        """
        Initializes the DataStore object.

        Args:
            - db_name (str): The name of the MongoDB database.
            - collection_name (str): The name of the MongoDB collection.
            - file_pths (str): The path to the directory containing the documents.
            - chunk_size (int): The size of each chunk for text splitting.
            - chunk_overlap (int): The overlap size between chunks for text splitting.

        Returns:
            - None.
        """
        self.uri = MONGO_URI
        self.db_name = db_name
        self.collection_name = collection_name
        self.collection = self.connect_db()

        self.file_pths = file_pths
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # define the OpenAI Embedding Model we want to use for the source data
        # NOTE: the embedding model is different from the language generation model
        self.embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    def connect_db(self) -> Collection:
        """
        Connects to MongoDB and returns the collection object.

        Args:
            - None.

        Returns:
            - pymongo.collection.Collection: The MongoDB collection object.
        """
        # set the MongoDB URI
        client = MongoClient(self.uri)
        # create the collection
        collection = client[self.db_name][self.collection_name]

        return collection

    def load_documents(self) -> list[Document]:
        """
        Loads documents from the specified directory.

        Args:
            - None.

        Returns:
            - List[Document]: A list of Document objects.
        """
        # initialize the DirectoryLoader
        loader = DirectoryLoader(self.file_pths, glob="./*.txt", show_progress=True)
        data = loader.load()

        return data

    def split_text(self, documents: list[Document]) -> list[Document]:
        """
        Splits text content of documents into chunks.

        Args:
            - documents (List[Document]): List of Document objects.

        Returns:
            - List[Document]: List of Document objects with split text content.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

        # # debug
        # document = chunks[10]
        # print(document.page_content)
        # print(document.metadata)

        return chunks

    def save_to_mongodb(self, chunks: list[Document]) -> MongoDBAtlasVectorSearch:
        """
        Saves text and vector embeddings into MongoDB collection.

        Args:
            - chunks (List[Document]): List of Document objects containing text content.

        Returns:
            - MongoDBAtlasVectorSearch: MongoDBAtlasVectorSearch object.
        """
        vector_store = MongoDBAtlasVectorSearch.from_documents(chunks,
                                                               self.embeddings, collection=self.collection)

        return vector_store

    def generate_data_store(self) -> MongoDBAtlasVectorSearch:
        """
        Generates data store by loading documents, splitting text, and saving to MongoDB.

        Args:
            - None.

        Returns:
            - None.
        """
        print("\nStarting generating data-store...")

        print("\nLoading documents...")
        documents = self.load_documents()

        print("\nSplitting documents...")
        chunks = self.split_text(documents)

        print("\nSaving documents into MongoDB...")
        vector_store = self.save_to_mongodb(chunks)

        print("\nGenerating data-store Done...\n")

        return vector_store


if __name__ == "__main__":
    ds = DataStore(db_name=config["DB_NAME"],
                   collection_name=config["COLLECTION_NAME"],
                   file_pths=config["FILE_PATHS"],
                   chunk_size=config["CHUNK_SIZE"],
                   chunk_overlap=config["CHUNK_OVERLAP"])
    vs = ds.generate_data_store()
