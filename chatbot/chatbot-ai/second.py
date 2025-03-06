import os
import weaviate
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
    
    client.collections.create("Project")
    
    jeopardy = client.collections.create(
        "Article",
        properties=[
            Property(name="title", data_type=DataType.TEXT),
            Property(name="body", data_type=DataType.TEXT),
        ]
    )
    
    uuid = jeopardy.data.insert({
        "title": "Chatbot Project",
        "description": "A chatbot using Weaviate and LangChain"
    })
    
    print(uuid)
    
    #response = client.data_object.create(data_object, class_name="Project")
    #weaviate_id = response["id"] 
    
    # Save into PostgreSQL
    cur.execute("INSERT INTO documents (weaviate_id, title, content) VALUES (%s, %s, %s)",
                (uuid, "Vector Database", "Weaviate is a powerful vector database"))
    conn.commit()
    
    print("Data is saved into PostgreSQL")

    # Set OpenAI API Key (if needed)
    os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

    # Load local embedding model
    local_embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # OpenAI embedding as fallback
    # openai_embedding_model = OpenAIEmbeddings()
except Exception as e:
    print("Error :", e)
finally:
    client.close()
    conn.close()