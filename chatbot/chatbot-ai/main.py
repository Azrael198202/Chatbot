#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: main.py
Author: Kan
Create Date: 2025-03-12
Description: The main entry point is used to start the FastAPI service and provide AI answering functionality.
Version: 1.0.0
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from weaviate_client import add_document as add_to_weaviate, get_answer
from database import get_db, add_document as add_to_postgres
from agent import run_agent
import threading
from tasks import schedule_tasks

app = FastAPI()
threading.Thread(target=schedule_tasks, daemon=True).start()

@app.post("/add")
async def add(content: str, db: Session = Depends(get_db)):
    """
    add question into PostgreSQL and Weaviate。
    """
    # add question into  PostgreSQL
    db_document = add_to_postgres(db, content)
    
    # add question into  Weaviate
    add_to_weaviate(content)
    return {"id": db_document.id, "content": db_document.content}

@app.post("/ask")
async def ask(query: str):
    """use AI Agent to generate the answer"""
    answer = run_agent(query)
    return {"query": query, "answer": answer}