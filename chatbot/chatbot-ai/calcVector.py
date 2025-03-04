from sentence_transformers import SentenceTransformer
import weaviate
import numpy as np

# link to  Weaviate
client = weaviate.Client("http://localhost:8080")

# define vectorization model
model = SentenceTransformer("all-MiniLM-L6-v2")  # lightweight text embedding model

# define Weaviate schema
class_obj = {
    "class": "Document",
    "vectorIndexType": "hnsw",
    "properties": [
        {"name": "title", "dataType": ["string"]},
        {"name": "content", "dataType": ["string"]}
    ]
}
client.schema.create_class(class_obj)

# compute vector
text = "Weaviate is a powerful vector database."
vector = model.encode(text).tolist()

# store into Weaviate
data_object = {
    "title": "vector database",
    "content": text
}
response = client.data_object.create(data_object, "Document", vector=vector)

# get the weaviate_id from the response
weaviate_id = response["id"]

# Store the weaviate_id into another variable for use in another file
# Example of storing it to a file (e.g., weaviate_id.txt)
#with open('weaviate_id.txt', 'w') as f:
#    f.write(str(weaviate_id))

print(f"Data is successfully saved into Weaviate. The weaviate_id is {weaviate_id}.")