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


# 3. initailize the learning and create vector database and postgresql
         python -c "from document_loader import initialize_learning; initialize_learning()"

# 4. NVIDIA Container Toolkit 
     1. install NVIDIA GPU drivers
          check   :   nvidia-smi
     2. Install NVIDIA Container Toolkit
         # Add NVIDIA Docker repository
        distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
        && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
        && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   
        sudo apt update
        sudo apt install -y nvidia-container-toolkit
     3. restart docker  :   sudo systemctl restart docker

# 5. Run a Docker Container with GPU Support
        docker run --gpus all nvidia/cuda:11.8.0-base nvidia-smi
            --gpus all → Allows the container to use all available GPUs.
            --gpus 1 → Restricts the container to using only one GPU.
            --gpus '"device=0,1"' → Specifies which GPUs (e.g., GPU 0 and 1) the container can use.

# 6. Running GPU-Accelerated Applications in Docker
    1.  Run TensorFlow with GPU
        docker run --gpus all -it tensorflow/tensorflow:latest-gpu bash

        python:
            import tensorflow as tf
            print(tf.config.list_physical_devices('GPU'))

    2.  Run PyTorch with GPU
        docker run --gpus all -it pytorch/pytorch:latest bash

        python:
            import torch
            print(torch.cuda.is_available())  # Should return True if GPU is available
            print(torch.cuda.device_count())  # Returns the number of GPUs available

# 7. ollama
      ollama -v
      ollama list
      ollama run hotel/8b/14b/32b/70b
      llama2:latest       78e26419b446    3.8 GB    9 days ago

      ollama create my-model -f modelfile

      modelfile
        FROM hotel
        SYSTEM "cat knowledge.json"

    knowledge.json
        

