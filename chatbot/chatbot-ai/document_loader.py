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
from weaviate_client import add_document as add_to_weaviate

def parse_json(filepath: str) -> List[Dict]:
    """interpret JSON"""
    with open(filepath, "r") as f:
        return json.load(f)

def parse_csv(filepath: str) -> List[Dict]:
    """interpret CSV"""
    data = []
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({"content": row["content"]})
    return data

def parse_txt(filepath: str) -> List[Dict]:
    """interpret TXT """
    with open(filepath, "r") as f:
        content = f.read()
    return [{"content": content}]

def load_documents(directory: str) -> List[Dict]:
    """Load files from a specified fold"""
    documents = []
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
    """"Initialization learning: Load initial documents. """
    db = SessionLocal()
    documents = load_documents("documents")
    for doc in documents:
        # save into PostgreSQL
        db_doc = Document(content=doc["content"])
        db.add(db_doc)
        # save into  Weaviate
        add_to_weaviate(doc["content"])
    db.commit()
    db.close()

def continuous_learning():
    """Continuous learning: Monitor and process newly added documents."""
    new_docs_dir = "documents/new_documents"
    while True:
        if os.path.exists(new_docs_dir):
            documents = load_documents(new_docs_dir)
            db = SessionLocal()
            for doc in documents:
                db_doc = Document(content=doc["content"])
                db.add(db_doc)
                add_to_weaviate(doc["content"])
            db.commit()
            db.close()