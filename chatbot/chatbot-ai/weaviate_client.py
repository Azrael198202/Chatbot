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
import weaviate.classes as wvc
from weaviate.classes.config import Configure, Property, DataType

# Initialize Weaviate Client
def initialize_client():
    client = weaviate.connect_to_local()
    if not client.is_live():
        raise Exception("Weaviate client is not live!")
    return client

def create_schema(client):
    try:
        if not client.collections.exists("Question"):
            questions = client.collections.create(
                name="Question",
                generative_config=wvc.config.Configure.Generative.ollama(
                    model="hotel"
                ),
                properties=[
                    wvc.config.Property(name="question", data_type=wvc.config.DataType.TEXT),
                    wvc.config.Property(name="answer", data_type=wvc.config.DataType.TEXT),
                    wvc.config.Property(name="category", data_type=wvc.config.DataType.TEXT),
                    wvc.config.Property(name="title", data_type=wvc.config.DataType.TEXT),
                    wvc.config.Property(name="content", data_type=wvc.config.DataType.TEXT)
                ]
            )
            print("Question schema created successfully!")
            print(questions.config.get(simple=False))
        else:
            print("Question schema already exists. Skipping creation.")
        return client.collections.get("Question")
    except Exception as e:
        print(f"Error during schema creation: {e}")
        return None

def add_document(client, questions, question: str, answer: str):
    """
    Add document to Weaviate.
    """
    try:
        if questions is None:
            raise Exception("Schema 'Question' was not created successfully. Cannot insert document.")

        uuid = questions.data.insert({
            "question": question,
            "answer": answer
        })
        print(f"Stored in Weaviate: {question}, uuid: {uuid}")
        return uuid
    except Exception as e:
        print(f"Error during document insertion: {e}")
        return None
    
def add_document_title(client, questions, title: str, content: str):
    """
    Add document to Weaviate.
    """
    try:
        if questions is None:
            raise Exception("Schema 'Question' was not created successfully. Cannot insert document.")

        uuid = questions.data.insert({
            "title":title,
            "content": content
        })
        print(f"Stored in Weaviate: {title}, uuid: {uuid}")
        return uuid
    except Exception as e:
        print(f"Error during document insertion: {e}")
        return None

def search_documents(client, query: str, limit: int = 1):
    try:
        response = client.query\
            .get("Question", ["content"])\
            .with_near_text({"concepts": [query]})\
            .with_limit(limit)\
            .do()
        return response["data"]["Get"]["Question"]
    except Exception as e:
        print(f"Error during document search: {e}")
        return []

def get_answer(query: str):
    try:
        client = initialize_client()
        questions = create_schema(client)
        if questions is None:
            raise Exception("Schema creation failed. Cannot proceed with document operations.")
        
        # Add a document if needed
        add_document(client, questions, "Example Title", "Example content for Weaviate document.")
        
        results = search_documents(client, query)
        context = results[0]["content"] if results else "No relevant context found."
        
        # Use LLM to generate response.
        answer = generate_answer(query, context)
        return answer
    finally:
        client.close()

# Initialize client and create schema
client = initialize_client()
questions = create_schema(client)
if questions:
    add_document(client, questions, "Test Title", "This is a test document content.")
client.close()
