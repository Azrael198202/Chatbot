#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: weaviate_client.py
Author: Your Name
Create Date: 2025-03-07
Description: initializes the Weaviate client and provides an interface for interacting with Weaviate.
Version: : 1.0.0
"""

import weaviate
from llm_handler import generate_answer

# initialize Weaviate Client
client = weaviate.Client("http://localhost:8080")

def create_schema():
    """
    create Weaviate schema。
    """
    schema = {
        "classes": [
            {
                "class": "Document",
                "description": "A document containing text data",
                "properties": [
                    {
                        "name": "content",
                        "dataType": ["text"],
                        "description": "The text content of the document"
                    }
                ]
            }
        ]
    }
    client.schema.create(schema)

def add_document(content: str):
    """
    save documents into Weaviate.

    parameter:
        content (str): document's content
    """
    client.data_object.create(
        data_object={"content": content},
        class_name="Document"
    )

def search_documents(query: str, limit: int = 1):
    """
    query from Weaviate

    parameter:
        query (str): query
        limit (int): result's count。

    result:
        list: result
    """
    response = client.query\
        .get("Document", ["content"])\
        .with_near_text({"concepts": [query]})\
        .with_limit(limit)\
        .do()
    return response["data"]["Get"]["Document"]

def get_answer(query: str):
    """
    use Weaviate and LLM to generate response.

    parameter:
        query (str): question

    result:
        str: answer
    """
    # with Weaviate to query documents
    results = search_documents(query)
    context = results[0]["content"] if results else "No relevant context found."

    # use LLM to generate response.
    answer = generate_answer(query, context)
    return answer

# initialize to create the schema
create_schema()