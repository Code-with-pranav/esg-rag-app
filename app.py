# app.py (updated)
import streamlit as st
import requests
import json

# Streamlit app
st.title("Real-Time ESG RAG App")

# Description
st.write("This app queries a real-time RAG pipeline to provide insights on ESG data and news.")

# Input query
query = st.text_input("Enter your query (e.g., 'What are the latest ESG emissions for CoalCo?')", "")

# Button to submit query
if st.button("Submit"):
    if query:
        try:
            # Send request to the RAG endpoint
            response = requests.post(
                "http://localhost:8000/rag",
                json={"query": query}
            )
            if response.status_code == 200:
                result = response.json()
                st.write("**Answer:**")
                st.write(result["answer"])
                st.write("**Context Used:**")
                st.write(result["context"])
                st.write("**Metadata:**")
                st.write(result["metadata"])
            else:
                st.error(f"Error: Could not get response. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a query.")

# Display the latest ESG report
st.subheader("Latest ESG Report")
try:
    with open("esg_stream_output.jsonl", "r") as f:
        esg_data = [json.loads(line) for line in f]
    if esg_data:
        st.json(esg_data[-1])  # Display the most recent ESG report
    else:
        st.write("No ESG report available.")
except FileNotFoundError:
    st.write("No ESG report available. Run the pipeline first.")

# Display the latest news article
st.subheader("Latest News Article")
try:
    with open("esg_news.jsonl", "r") as f:
        news_data = [json.loads(line) for line in f]
    if news_data:
        st.json(news_data[-1])  # Display the most recent news article
    else:
        st.write("No news data available.")
except FileNotFoundError:
    st.write("No news data available. Run fetch_news.py first.")