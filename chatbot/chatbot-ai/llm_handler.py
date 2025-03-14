#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: llm_handler.py
Author: Your Name
Create Date: 2025-03-07
Description: initializes LangChain and Ollama to generate responses using LLM
Version: : 1.0.0
"""

from langchain import LLMChain, PromptTemplate
from langchain.llms import Ollama

# initializes Ollama
#llm = Ollama(model="gpt-3")
llm = Ollama(model="hotel")

# initializes template
template = """
You are a helpful AI assistant. Answer the following question based on the context provided.

Context:
{context}

Question:
{query}

Answer:
"""
prompt = PromptTemplate(template=template, input_variables=["context", "query"])

# initializes LLMChain
chain = LLMChain(llm=llm, prompt=prompt)

def generate_answer(query: str, context: str = ""):
    """
    Use LLM to generate reponse

    parameter:
        query (str): question
        context (str): Context (Optional).

    result:
        str: answer
    """
    return chain.run(query=query, context=context)

def retrain_model():
    """Model optimization: Fine-tune the model based on the latest data. """
    from database import SessionLocal, Document
    db = SessionLocal()
    documents = db.query(Document).all()
    training_data = [doc.content for doc in documents]
    
    # Assuming the use of Ollama's fine-tuning API (adjust according to the actual API)."
    llm.fine_tune(training_data, model="hotel")
    print("Model retrained with latest data.")