# esg-rag-app
A Real-Time ESG RAG Application built with Pathway for the hackathon. Ingests ESG and news data, uses a RAG pipeline with Pathway and LangGraph, and provides a Streamlit UI and FastAPI API for real-time insights in the financial domain.

# Real-Time ESG RAG Application Using Pathway

## Project Overview
The **Real-Time ESG RAG Application** is a hackathon project designed to meet the requirements of the problem statement "Build a Real-Time Retrieval-Augmented Generation (RAG) App with Pathway." This application focuses on the financial domain, specifically processing ESG (Environmental, Social, and Governance) data in real-time to provide up-to-date insights for applications like compliance and asset management.

The system leverages **Pathway**, a Python data processing framework, to ingest, index, and retrieve ESG and news data in real-time. It integrates a Retrieval-Augmented Generation (RAG) pipeline with an agentic AI component using **LangGraph** for autonomous query processing. The application is deployed via a **FastAPI** REST API and features a user-friendly **Streamlit** interface to demonstrate real-time updates.

### Key Features
- **Real-Time Data Ingestion**: Ingests ESG and news data in streaming mode using Pathway.
- **Vector Store Setup**: Indexes data with embeddings using Pathway for efficient retrieval.
- **RAG Pipeline**: Combines hybrid retrieval (keyword + vector scoring) with an LLM (Ollama with Phi3) for answer generation.
- **Agentic AI**: Uses LangGraph to preprocess queries, enhancing autonomy by checking ESG relevance.
- **REST API**: Exposes the RAG pipeline via a FastAPI endpoint.
- **User Interface**: A Streamlit app for querying the system and observing real-time updates.
- **Domain Focus**: Focuses on ESG data in the financial domain, suitable for compliance and asset management.

This project is original, built from scratch for the hackathon, and is open-source under the MIT License.

## System Architecture
The application consists of the following components:
1. **Data Ingestion and Indexing** (`rag_app.py`): Uses Pathway to ingest ESG and news data in real-time and index it with embeddings.
2. **RAG Pipeline** (`rag_app.py`): Retrieves relevant context and generates answers using an LLM.
3. **Agentic AI** (`rag_app.py`): Enhances queries with LangGraph for better ESG relevance.
4. **REST API** (`rag_app.py`): Exposes the RAG pipeline via FastAPI.
5. **User Interface** (`app.py`): A Streamlit app for querying and viewing real-time updates.

**Flow**:  
Data Sources (JSONLines files) → Pathway Pipeline (ingestion, indexing) → Agentic Workflow (LangGraph) → RAG Pipeline (retrieval, generation) → REST API (FastAPI) → UI (Streamlit)

## Integration with LLMs
The application integrates with an LLM (Ollama with the Phi3 model) for the generation step in the RAG pipeline:
- **Retrieval**: Pathway retrieves the top 3 relevant contexts using a hybrid scoring mechanism (vector distance + keyword matching).
- **Prompt Creation**: The retrieved context is combined with the user query into a prompt.
- **Generation**: The prompt is sent to the Phi3 model (running locally via Ollama) to generate a response.
- **Real-Time Updates**: The pipeline ensures answers reflect the latest ingested data, demonstrating Pathway’s real-time capabilities.

## Folder Structure
esg_rag_app/
│
├── app.py              # Streamlit web app for the user interface
├── rag_app.py          # Pathway pipeline, RAG pipeline, LangGraph agent, and FastAPI server
├── simulate_data.py    # Script to simulate real-time data ingestion
├── requirements.txt    # List of Python dependencies
└── README.md           # Project documentation (this file)


**Note**: Data files like `esg_stream_output.jsonl` and `esg_news.jsonl` are not included in the repository. Instructions to create them are provided below.

## Setup Instructions
Follow these steps to set up and run the application on your local machine.

### Prerequisites
- Python 3.8 or higher
- Git
- Docker (optional, for running Ollama)

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Code-with-pranav/esg-rag-app.git
   cd esg_rag_app
2. **Set Up a Virtual Environment:**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
4. **Install Ollama**:
   - Follow the instructions at https://ollama.ai/ to install Ollama.
   - Pull the Phi3 model: ollama pull phi3
5. **Prepare Data Files**:
   - Create esg_stream_output.jsonl with sample ESG data, e.g.:
     ```bash
     {"company": "CoalCo", "emissions": 177, "date": "2025-03-28"}
   - Create esg_news.jsonl with sample news data, e.g.:
     ```bash
     {"title": "Streit um 'grüne Fonds': Deutsche-Bank-Tochter DWS zahlt Millionen wegen Greenwashing", "description": "..."}
   - Place these files in the esg_rag_app/ directory.
### Running the Application
1. Start the Data Simulation (Optional): This script adds a new ESG report every 2 minutes to simulate real-time data.
   ```bash
   python simulate_data.py
2. Start the FastAPI Server: This runs the Pathway pipeline and exposes the RAG endpoint.
   ```bash
   python rag_app.py
   The server will run on http://localhost:8000
3. Start the Streamlit App: This launches the user interface.
   ```bash
   streamlit run app.py
   Open your browser and go to http://localhost:8501
### Testing the Application
- In the Streamlit app, enter a query (e.g., "What is ESG?") and submit.
- View the answer, context, and metadata in the UI.
- Check the "Latest ESG Data Updates" section to see real-time updates.
- Test non-ESG queries (e.g., "What is machine learning?") to observe the agentic workflow in action.
- Test the API directly:
  ```bash
  curl -X POST http://localhost:8000/rag -H "Content-Type: application/json" -d '{"query": "What is ESG?"}'
### Usage
- UI: Use the Streamlit app at http://localhost:8501 to input queries and view responses with real-time updates.
- API: Query the FastAPI endpoint at http://localhost:8000/rag with a POST request containing a JSON payload (e.g., {"query": "What is ESG?"}).
### Limitations and Future Improvements
- Embeddings: Currently uses a simple hash-based embedding function. A proper embedding model (e.g., Sentence Transformers) could improve retrieval accuracy.
- Real-Time Data Source: Uses JSONLines files to simulate real-time ingestion. Could be replaced with a streaming API.
- Agentic Features: The agentic workflow could be expanded with more complex logic (e.g., external tool calls).
- Visualizations: The UI could include charts to visualize ESG data.

### Conclusion
The Real-Time ESG RAG Application demonstrates a robust solution for real-time ESG data processing in the financial domain. It meets all hackathon requirements, including real-time data ingestion, RAG pipeline implementation, REST API deployment, and a user-friendly UI, while adding an agentic AI component for bonus points. The project is well-structured, original, and open-source, making it a strong contender for the hackathon.

## Author
- Name: Pranav Roy
- GitHub: Code-with-pranav
- Email: pranavroy1098@gmail.com
