#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: database.py
Author: Your Name
Create Date: 2025-03-07
Description: Initializes the PostgreSQL database connection, defines database models, and provides an interface for interacting with PostgreSQL. 
Version: : 1.0.0
"""

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# configure the url
DATABASE_URL = "postgresql://chatbot:chatbot!@localhost:5432/chatbot_db"

# create the database engine
engine = create_engine(DATABASE_URL)

# create SessionLocal 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# define the base class
Base = declarative_base()

# create Document model
class Document(Base):
    """
    Document table model to save the documents
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

# create table
Base.metadata.create_all(bind=engine)

def get_db():
    """
     get database instance

    result:
        SessionLocal: get database instance
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_document(db, content: str):
    """
    save data into PostgreSQL

    parameter:
        db: database instance
        content (str): content
    """
    db_document = Document(content=content)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_document(db, document_id: int):
    """
    get data from PostgreSQL

    parameter:
        db: database instance
        document_id (int): doucment's ID。

    result:
        Document: data
    """
    return db.query(Document).filter(Document.id == document_id).first()