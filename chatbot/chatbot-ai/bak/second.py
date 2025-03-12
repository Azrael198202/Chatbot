import os
import numpy as np

import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import MetadataQuery
import psycopg2
from langchain_community.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Weaviate
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import create_retrieval_chain
from langchain.llms import Ollama  # Local AI
from langchain_ollama import OllamaLLM

try:
    # Connect to Weaviate
    client = weaviate.connect_to_local()
    assert client.is_live()
    print('------weaviate is connected------')

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="chatbot_db",
        user="chatbot",
        password="chatbot!",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    
    # CreateTable
    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        weaviate_id TEXT UNIQUE,
        title TEXT,
        content TEXT
    )
    """)
    conn.commit()
    print("documents is created")
    
    if client.collections.exists("Project"):
        print("existed project will be deleted")
        client.collections.delete("Project")
    
    jeopardy = client.collections.create(
        "Project",
        vectorizer_config={"vectorizer": "text2vec-transformers"},
        properties=[
            Property(name="title", data_type=DataType.TEXT),
            Property(name="body", data_type=DataType.TEXT),
        ]
    )

    print("Project is created")
    
    #uuid = jeopardy.data.insert({
    #    "title": "Chatbot Project",
    #    "description": "A chatbot using Weaviate and LangChain"
    #})
    
    #print(uuid)
    
    #response = client.data_object.create(data_object, class_name="Project")
    #weaviate_id = response["id"] 

    # Set OpenAI API Key (if needed)
    os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

    # Load local embedding model
    print("Load local embedding model")
    local_embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # **Generate Text Embeddings**
    def get_embedding(text):
        return local_embedding_model.embed_query(text)  
       
    # **Store Documents in Weaviate**
    def store_document(title, content):
        vector = get_embedding(content)
        uuid = jeopardy.data.insert({
            "title": title,
            "description": content
        })
        print(f"Stored in Weaviate: {title}, uuid :{uuid}")
        # Save into PostgreSQL
        cur.execute("INSERT INTO documents (weaviate_id, title, content) VALUES (%s, %s, %s)",
                    (str(uuid), title, content))
        conn.commit()
    
        print("Data is saved into PostgreSQL")
        
    # **Retrieve Similar Documents from Weaviate**
    def search_weaviate(query_text):
        query_vector = get_embedding(query_text)
        print(f"Query vector : {query_vector}")
        
        query_vector = np.array(query_vector)
        print(f"Query vector as array : {query_vector}")
        jeopardy = client.collections.get("Project")
        response = jeopardy.query.near_text(
            query= query_text,
            limit=5,
            return_metadata=MetadataQuery(distance=True)
        )
        for o in response.objects:
            print(o.properties)
            print(o.metadata.distance)
                    
    # OpenAI embedding as fallback
    # openai_embedding_model = OpenAIEmbeddings()
    print("OllamaLLM will be connected")
    llm = OllamaLLM(model="mistral", base_url="http://localhost:11434")
    
    store_document("Vector Database", "Weaviate is a powerful vector database")
    
    print("question will start")
    query = "What is a vector database?"
    search_weaviate(query)
    
except Exception as e:
    print("Error :", e)
finally:
    client.close()
    conn.close()