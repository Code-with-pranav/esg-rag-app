# rag_app.py
import pathway as pw
from pathway.stdlib.ml.index import KNNIndex
import requests
import json
import os
from fastapi import FastAPI, Request
import uvicorn
import threading
import pandas as pd
import logging

# Configure logging for FastAPI/Uvicorn
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn.error")

# Define schema for ESG reports
class EsgReportSchema(pw.Schema):
    company: str
    emissions: int
    date: str

# Define schema for news data
class NewsSchema(pw.Schema):
    title: str
    description: str
    published_at: str
    source: str
    url: str

# Read ESG data stream
esg_stream = pw.io.jsonlines.read(
    "esg_stream_output.jsonl",
    schema=EsgReportSchema,
    mode="streaming"
)

# Read news data stream
news_stream = pw.io.jsonlines.read(
    "esg_news.jsonl",
    schema=NewsSchema,
    mode="static"
)

# Process ESG and news data separately
esg_data_with_text = esg_stream.select(
    text=pw.this.company + " emissions: " + pw.cast(str, pw.this.emissions) + " tons on " + pw.this.date,
    metadata=pw.this.company + "|" + pw.cast(str, pw.this.emissions) + "|" + pw.this.date,
    source=pw.make_tuple("esg")
)

news_data_with_text = news_stream.select(
    text=pw.this.title + " " + pw.this.description,
    metadata=pw.this.title + "|" + pw.this.description + "|" + pw.this.published_at + "|" + pw.this.source + "|" + pw.this.url,
    source=pw.make_tuple("news")
)

# Write intermediate tables for debugging
pw.io.jsonlines.write(esg_stream, "debug_esg_stream.jsonl")
pw.io.jsonlines.write(news_stream, "debug_news_stream.jsonl")
pw.io.jsonlines.write(esg_data_with_text, "debug_esg_data_with_text.jsonl")
pw.io.jsonlines.write(news_data_with_text, "debug_news_data_with_text.jsonl")

# Ensure both tables have the same schema and disjoint universes before concatenation
esg_data_with_text = esg_data_with_text.promise_universes_are_disjoint(news_data_with_text)

# Combine data for indexing
combined_data_for_indexing = pw.Table.concat(
    esg_data_with_text,
    news_data_with_text
)

# Generate embeddings (simplified for demo; in practice, use a proper embedding model)
def generate_embeddings(text):
    print(f"Generating embedding for text: {text[:50]}...")
    return [hash(text) % 1000] * 384  # Dummy 384-dim vector

# Create a table with embeddings
combined_data_with_embeddings = combined_data_for_indexing.select(
    text=pw.this.text,
    metadata=pw.this.metadata,
    source=pw.this.source,
    embedding=pw.apply(generate_embeddings, pw.this.text)
)

# Write tables to temporary files for debugging
pw.io.jsonlines.write(combined_data_for_indexing, "debug_combined_data.jsonl")
pw.io.jsonlines.write(combined_data_with_embeddings, "debug_combined_data_with_embeddings.jsonl")

# Create a KNN index for retrieval
index = KNNIndex(
    combined_data_with_embeddings.embedding,
    combined_data_with_embeddings,
    n_dimensions=384
)

# Function to query the LLM (Ollama with Phi3)
def query_llm(prompt):
    print("Querying LLM with prompt:", prompt[:100], "...")
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False
            }
        )
        print("LLM response status:", response.status_code)
        if response.status_code == 200:
            return response.json().get("response", "No response from LLM")
        else:
            return f"Error: LLM request failed with status {response.status_code}"
    except Exception as e:
        print("Error querying LLM:", str(e))
        return f"Error querying LLM: {e}"

# Inside rag_function
def rag_function(query: str) -> dict:
    print("Starting rag_function with query:", query)
    try:
        query_embedding = generate_embeddings(query)
        print("Generated query embedding:", query_embedding[:5], "...")

        print("Checking combined_data_with_embeddings...")
        with open("debug_combined_data_with_embeddings.jsonl", "r") as f:
            combined_data = [json.loads(line) for line in f]
        if not combined_data:
            print("Error: combined_data_with_embeddings is empty.")
            return {"error": "No data available for retrieval. Check data ingestion."}
        print(f"Found {len(combined_data)} entries in combined_data_with_embeddings.")

        # Compute hybrid scores: vector distance + keyword score
        print("Computing hybrid scores...")
        query_words = set(query.lower().split())
        for item in combined_data:
            # Vector distance
            emb = item['embedding']
            vector_distance = sum((e - q) ** 2 for e, q in zip(emb, query_embedding)) ** 0.5
            # Keyword score (simple BM25-like scoring)
            text = item['text'].lower()
            keyword_score = sum(1 for word in query_words if word in text) / (len(query_words) + 1)
            # Combine scores (adjust weights as needed)
            item['hybrid_score'] = 0.7 * (1 - keyword_score) + 0.3 * (vector_distance / 1000)  # Normalize vector distance
        print("Hybrid scores computed.")

        # Sort by hybrid score and take top 3
        print("Sorting and selecting nearest items...")
        combined_data.sort(key=lambda x: x['hybrid_score'])
        nearest = combined_data[:3]
        print("Nearest items selected:", nearest)

        # Extract context and metadata
        context = "\n".join([item['text'] for item in nearest])
        metadata = "\n".join([item['metadata'] for item in nearest])
        print("Context extracted:", context[:100], "...")
        print("Metadata extracted:", metadata[:100], "...")

        prompt = f"Context:\n{context}\n\nQuery: {query}\n\nAnswer the query using the provided context."
        print("Prompt constructed:", prompt[:100], "...")
        answer = query_llm(prompt)
        print("Answer generated from LLM:", answer[:100], "...")

        response = {
            "answer": answer,
            "context": context,
            "metadata": metadata
        }
        print("Returning response:", response)
        return response
    except Exception as e:
        print("Error in rag_function:", str(e))
        return {"error": f"Error in rag_function: {str(e)}"}

# Start the Pathway pipeline in a separate thread
def run_pathway():
    print("Starting Pathway pipeline...")
    pw.run(monitoring_level=pw.MonitoringLevel.ALL)
    print("Pathway pipeline finished.")

# Create a FastAPI app
app = FastAPI()

# Define the REST API endpoint
@app.post("/rag")
async def rag_endpoint(request: Request):
    print("Received request at /rag endpoint.")
    try:
        data = await request.json()
        print("Request data:", data)
        query = data.get("query")
        if not query:
            print("No query provided.")
            return {"error": "Query parameter is required"}
        result = rag_function(query)
        print("Returning result:", result)
        return result
    except Exception as e:
        print("Error in rag_endpoint:", str(e))
        logger.error("Error in rag_endpoint: %s", str(e))
        return {"error": f"Error in rag_endpoint: {str(e)}"}

# Run FastAPI server in the main thread
if __name__ == "__main__":
    print("Starting rag_app.py...")
    # Start Pathway in a separate thread
    pathway_thread = threading.Thread(target=run_pathway, daemon=True)
    pathway_thread.start()
    print("Pathway thread started.")

    # Start FastAPI server
    print("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
    print("FastAPI server started.")