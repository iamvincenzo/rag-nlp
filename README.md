# Retrieval Augmented Generation (RAG)

GitHub repository dedicated to Retrieval-Augmented Generation for Natural Language Processing (NLP).

---

## Theory

[Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) (RAG) is an advanced technique in natural language
processing (NLP) that combines `Retrieval` and `Text Generation` capabilities to improve the performance of `Large
Language Models` (LLM).

Essentially, RAG works by integrating a generative language model with an information retrieval system. The generative
model can be a large language model such as GPT (Generative Pre-trained Transformer), which is trained to generate
coherent and meaningful text. On the other hand, the retrieval system can be a specialised search engine or information
retrieval model that can extract relevant information from a large body of text. The operation of the RAG can be divided
into two main phases:

1. **Retrieval:** In this phase, RAG uses the retrieval system to extract relevant information from a set of documents
   or
   data. This can be done using techniques such as keyword search, semantic search or other information extraction
   methods.

2. **Generation:** Once the relevant information has been retrieved, the generative language model is used to generate a
   coherent response or text based on this information. The model can integrate the extracted information into the
   generation process to produce a more informative and accurate output.

The main objective of RAG is to improve the quality and relevance of the generated text using the information extracted
from the retrieval system. This technique has been successfully applied to a variety of NLP tasks, including `answering
questions`, generating coherent text, and creating informative documents.

## MongoDB Atlas Vector Search

[MongoDB Atlas Vector Search](https://www.mongodb.com/it-it/products/platform/atlas-vector-search) enables `semantic
similarity search` of data using `vector embeddings` to build powerful custom NLP applications. Embedding vectors
organise data so that similar elements are close together in the embedding space, allowing the data to be understood and
manipulated through numerical vectors. `Vector search` finds similar or relevant information to the input query using
both query embeddings and stored document embeddings, based on a `measure of distance` between vectors. MongoDB Atlas
Vector Search provides an efficient way to perform semantic similarity searches on data from various sources and in
different formats, represented as vector embeddings.

## RAG graphical schema

<p align="center">
  <img src="./imgs/rag_schema.png" width="800" />
</p>

---

# Setup Guide for Retrieval-Augmented Generation (RAG)

Follow these steps to configure your environment and set up MongoDB Atlas Vector Search for Retrieval-Augmented
Generation:

### Prerequisites

- A MongoDB Atlas account (sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)).
- Python installed on your local machine, with `pymongo` and `mongodb` libraries. You can install required packages by
  running:
   ```bash
   pip install pymongo
   ```

### Step-by-Step Setup

### 1. **Create a Cluster in MongoDB Atlas**

- Log in to your MongoDB Atlas account.
- Navigate to the **Clusters** tab and select **Create** to start a new cluster.
- Choose your cluster settings. For initial testing, the **free-tier cluster** option (M0) should be sufficient.
- Once your cluster is created, go to **Connect** to retrieve the connection string.
- Create a `key_param.py` script with this connection string to enable your application to access the MongoDB cluster.

#### 2. **Configure Database and Collections**

- After creating the cluster, go to **Database Access** to add a new database user. Set a username and password, and
  assign **readWrite** permissions to allow full access to the collections. Make sure to save the password securely, as
  you’ll need it for connecting to the database later.

<!-- - Go to **Network Access** and add your IP address to allow connections.-->

#### 3. **Run `create_database.py` Script**

- This script initializes your MongoDB database, collections, and inserts required data.
- Execute the script by running:
   ```bash
   python create_database.py
   ```
- Ensure your MongoDB connection URI in `create_database.py` is correctly configured to match your cluster details.

#### 4. **Create a Vector Search Index in MongoDB Atlas**

- Go to **Clusters** > **Browse Collections** and select the collection you created.
- Under **Search Indices**, click **Create Search Index**.
- Choose **JSON Editor** and paste the following JSON configuration to set up a vector search index:

  ```json
  {
    "mappings": {
      "dynamic": true,
      "fields": {
        "embedding": [
          {
            "dimensions": 1536,
            "similarity": "cosine",
            "type": "knnVector"
          }
        ]
      }
    }
  }
  ```

- Save the index configuration and wait for the index to complete creation (this may take a few minutes).

#### 5. **Set Up OpenAI API Key**

- Sign up or log in to your [OpenAI account](https://platform.openai.com/account/api-keys).
- Navigate to the **API Keys** section and create a new API key.
- Copy the API key and securely store it. You’ll need this key to integrate OpenAI's language model with your project
  inside a script named `key_param.py`.

#### 6. **Run `extract_information.py` Script**

- This script extracts relevant data from MongoDB Atlas using the configured vector search and processes it for RAG.
- Run the script with:
   ```bash
   python extract_information.py
   ```

- Ensure any dependencies are installed and that the MongoDB URI in `extract_information.py` is correctly set to your
  cluster.

---

## Credits

- [RAG Atlas Vector Search Langchain OpenAI](https://www.mongodb.com/developer/products/atlas/rag-atlas-vector-search-langchain-openai/)