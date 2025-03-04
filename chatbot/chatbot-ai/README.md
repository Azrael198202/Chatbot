# Chatbot ai

# Ollama (for running local AI models like LLaMA, Mistral, Gemma, etc.).   
 # 1. Download Local AI Models 
    exec in the termial
    docker exec -it ollama_ai ollama pull mistral    or   
    docker exec -it ollama_ai ollama pull llama2

# 2.  Install Required Python Packages
    > chatbot-ai
    pip install langchain weaviate-client psycopg2 sentence-transformers openai ollama


# If you have to use v3 code, install the v3 client and pin the v3 dependency in your requirements file: weaviate-client>=3.26.7;<4.0.0
    pip install "weaviate-client>=3.26.7,<4.0.0"



