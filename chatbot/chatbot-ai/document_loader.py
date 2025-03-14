#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: document_loader.py
Author: Kan
Create Date: 2025-03-12
Description: Load files ,supoort json, csv and txt
Version: 1.0.0
"""

import os
import json
import csv
from datetime import datetime
from typing import List, Dict
from pathlib import Path
from database import SessionLocal, Document
from weaviate_client import add_document as add_to_weaviate, add_document_title as add_to_weaviate_title
from weaviate_client import initialize_client, create_schema

def parse_json(filepath: str) -> List[Dict]:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}") 
    
    """interpret JSON"""
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {filepath}: {e}")

def parse_csv(filepath: str) -> List[Dict]:
    """interpret CSV"""
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}") 
    
    data = []
    with open(filepath, "r",encoding="utf-8") as f:
        try:
            reader = csv.DictReader(f)
        
            for row in reader:
                data.append({"content": row["content"]})
        except Exception as e:
            raise ValueError(f"Invalid CSV format in {filepath}: {e}")
        
    return data

def parse_txt(filepath: str) -> List[Dict]:
    """interpret TXT """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}") 
    
    with open(filepath, "r",encoding="utf-8") as f:
        try:
            content = f.read()
            return [{"content": content}]
        except Exception as e:
            raise ValueError(f"Invalid TXT format in {filepath}: {e}")
    

def load_documents(directory: str) -> List[Dict]:
    """Load files from a specified fold"""
    documents = []
    print(f"File Path is outputed :{directory}")
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if filename.endswith(".json"):           
            docs = parse_json(filepath)
        elif filename.endswith(".csv"):
            docs = parse_csv(filepath)
        elif filename.endswith(".txt"):
            docs = parse_txt(filepath)
        else:
            continue
        documents.extend(docs)
        # move the dealed file into sub fold
        processed_dir = os.path.join(directory, "processed")
        Path(processed_dir).mkdir(exist_ok=True)
        os.rename(filepath, os.path.join(processed_dir, filename))
    return documents

def initialize_learning():
    """Initialization learning: Load initial documents."""
    db = SessionLocal()

    # Initialize Weaviate client
    client = initialize_client()
    questions = create_schema(client)
    
    if questions is None:
        print("Schema creation failed. Aborting initialization.")
        client.close()
        return

    print("load_documents will be executed!")
    directory = os.path.abspath(os.path.join(os.getcwd(), "../documents"))
    print(f"directory:{directory}")

    documents = load_documents(directory)
    print(f"document's content's count: {len(documents)}")

    for doc in documents:
        try:
            # Save to Weaviate
            
            if not "question" in doc:
                print(f"inserting document: title")
                print(doc)
                uuid = add_to_weaviate_title(client, questions, 'Win Villa 民泊', doc["content"])
                
                # Save to PostgreSQL
                db_doc = Document(weaviate_id=uuid, title='Win Villa 民泊', content=doc["content"])
                db.add(db_doc)
            else:
                print(f"inserting document: question and answer")
                uuid = add_to_weaviate(client, questions, doc["question"], doc["answer"])
                
                # Save to PostgreSQL
                db_doc = Document(weaviate_id=uuid, question=doc["question"], answer=doc["answer"])
                db.add(db_doc)
        except Exception as e:
            print(f"Error inserting document: {e}")

    db.commit()
    db.close()
    client.close()  # Ensure the Weaviate client is closed properly


def continuous_learning():
    """Continuous learning: Monitor and process newly added documents."""
    new_docs_dir = "../documents/new_documents"

    client = initialize_client()
    questions = create_schema(client)

    if questions is None:
        print("Schema creation failed. Aborting continuous learning.")
        client.close()
        return

    while True:
        if os.path.exists(new_docs_dir):
            documents = load_documents(new_docs_dir)
            db = SessionLocal()

            for doc in documents:
                try:
                    # Save to Weaviate
                    uuid = add_to_weaviate(client, questions, doc["question"], doc["answer"])
                    
                    # Save to PostgreSQL
                    db_doc = Document(weaviate_id=uuid, title=doc["question"], content=doc["answer"])
                    db.add(db_doc)
                except Exception as e:
                    print(f"Error inserting document: {e}")

            db.commit()
            db.close()
        client.close()  # Ensure the Weaviate client is closed properly
