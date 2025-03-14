from weaviate_client import get_answer

query = "How does Weaviate store data?"
answer = get_answer(query)
print(f"Generated Answer: {answer}")