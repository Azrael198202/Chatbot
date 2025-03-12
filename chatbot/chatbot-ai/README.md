# Chatbot ai

# Ollama (for running local AI models like LLaMA, Mistral, Gemma, etc.).   
 # 1. Download Local AI Models 
    exec in the termial
    docker exec -it ollama_ai ollama pull mistral    or   
    docker exec -it ollama_ai ollama pull llama2

# 2.  Install Required Python Packages
    > chatbot-ai
    pip install langchain langchain-community langchain-huggingface langchain-ollama langchain-core weaviate-client psycopg2 sentence-transformers openai ollama
    pip install sqlalchemy elasticsearch
    pip install fastapi uvicorn 


# If you have to use v3 code, install the v3 client and pin the v3 dependency in your requirements file: weaviate-client>=3.26.7;<4.0.0
    pip install "weaviate-client>=3.26.7,<4.0.0"     => client = weaviate.Client("http://localhost:8080")
    pip install --upgrade weaviate-client
    pin install weaviate-client    => client = weaviate.connect_to_local()



