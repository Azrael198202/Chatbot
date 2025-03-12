import os
import weaviate
import psycopg2
from langchain_community.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Weaviate
from langchain_community.chains import RetrievalQA
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

    # Set OpenAI API Key (if needed)
    os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

    # Load local embedding model
    local_embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # OpenAI embedding as fallback
    # openai_embedding_model = OpenAIEmbeddings()

    # **Generate Text Embeddings**
    def get_embedding(text):
        #try:
            return local_embedding_model.embed_query(text)
        #except Exception:
            #return openai_embedding_model.embed_query(text)

    # **Store Documents in Weaviate**
    def store_document(title, content):
        vector = get_embedding(content)
        client.data_object.create(
            {"title": title, "content": content},
            "Document",
            vector=vector
        )
        print(f"Stored in Weaviate: {title}")

    # **Retrieve Similar Documents from Weaviate**
    def search_weaviate(query_text):
        query_vector = get_embedding(query_text)
        properties = ["title", "content"]
        result = client.query.get("Document", properties) \
            .with_near_vector({"vector": query_vector}) \
            .with_limit(3) \
            .do()

        return result['data']['Get']['Document']

    # **Local AI (Ollama)**
    #try:
    #    llm = Ollama(model="mistral", base_url="http://localhost:11434")
    #except Exception:
    #   print("Local AI failed to load, switching to OpenAI")
    #   llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    #llm = Ollama(model="mistral", base_url="http://localhost:11434")
    llm = OllamaLLM(model="mistral", base_url="http://localhost:11434")

    #properties = ["text", "metadata"] 
    #retriever = Weaviate(client, "Document", local_embedding_model, query_attrs=properties).as_retriever()
    #combine_documents_chain = load_qa_chain(llm, chain_type="stuff")
    #qa = RetrievalQA(combine_documents_chain=combine_documents_chain, retriever=retriever)
    #query = "What is a vector database?"
    #response = qa.invoke(query)
    #print(response)

    # **LangChain Question Answering**
    #retriever = Weaviate(client, "Document", local_embedding_model).as_retriever()
    #qa = RetrievalQA(llm=llm, retriever=retriever)
    # Create a combine_documents_chain (you can customize this, but it combines the retrieved documents and LLM)
    #combine_documents_chain = create_retrieval_chain(llm)
    # Initialize the RetrievalQA system
    #qa = RetrievalQA(combine_documents_chain=combine_documents_chain, retriever=retriever)

    # **Ask a Question**
    #query = "What is a vector database?"
    #response = qa.invoke(query)
    #print(response)
finally:
    client.close()