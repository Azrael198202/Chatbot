#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: agent.py
Author: Kan
Create Date: 2025-03-12
Description: Define an AI Agent that supports multi-tool invocation (Weaviate and Elasticsearch).
Version: 1.0.0
"""

from langchain.agents import initialize_agent, Tool
from langchain.llms import Ollama
from weaviate_client import search_documents
from elasticsearch import Elasticsearch

# initialize LLM and Elasticsearch
llm = Ollama(model="gpt-3")
es = Elasticsearch("http://localhost:9200")

def weaviate_search(query: str) -> str:
    """Weaviate :Semantic search"""
    results = search_documents(query, limit=3)
    return "\n".join([res["content"] for res in results])

def elasticsearch_search(query: str) -> str:
    """Elasticsearch :Full-text search"""
    response = es.search(
        index="documents",
        body={"query": {"match": {"content": query}}}
    )
    return "\n".join([hit["_source"]["content"] for hit in response["hits"]["hits"]])

# define tools list
tools = [
    Tool(
        name="Semantic Search (Weaviate)",
        func=weaviate_search,
        description="Useful for answering questions requiring semantic understanding."
    ),
    Tool(
        name="Keyword Search (Elasticsearch)",
        func=elasticsearch_search,
        description="Useful for finding documents based on keywords."
    )
]

# initialize Agent
agent = initialize_agent(
    tools, llm, agent="zero-shot-react-description", verbose=True
)

def run_agent(query: str) -> str:
    """run Agent  to query"""
    return agent.run(query)