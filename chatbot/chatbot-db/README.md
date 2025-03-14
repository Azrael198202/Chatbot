# Chatbot-db

# Weaviate + PostgreSQL + Local AI Model 

# PostgreSQL (for structured data storage). 

# Weaviate (for vector data storage).   

# Ollama (for running local AI models like LLaMA, Mistral, Gemma, etc.).   
 # 1. Download Local AI Models
    docker exec -it ollama_ai ollama pull mistral    or   
    docker exec -it ollama_ai ollama pull llama2

# 2.  Install Required Python Packages
    pip install langchain weaviate-client psycopg2 sentence-transformers openai ollama

# 3. docker run -d --memory=512m --cpus=1 nginx  / docker run -d --cpuset-cpus="0,1" nginx
