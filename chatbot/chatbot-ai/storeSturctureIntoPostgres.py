import psycopg2
from calcVector import weaviate_id

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="chatbot_db",
    user="chatbot",
    password="chatbot!",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# CreateTable
cur.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    weaviate_id TEXT UNIQUE,
    title TEXT,
    content TEXT
)
""")
conn.commit()

# Save into PostgreSQL
cur.execute("INSERT INTO documents (weaviate_id, title, content) VALUES (%s, %s, %s)",
            (weaviate_id, "Vector Database", "Weaviate is a powerful vector database"))
conn.commit()

print("Data is saved into PostgreSQL")