# ChatbotPro – Retrieval-Augmented Generation (RAG) System
Step 1:
## Overview
This project implements a Retrieval-Augmented Generation (RAG) pipeline using LangChain.
The system retrieves relevant information from a document knowledge base (PDFs) and uses
a Large Language Model (LLM) to generate accurate, context-aware answers with citations.

The project demonstrates:
- Document ingestion and chunking
- Vector database creation using embeddings
- Multi-query retrieval for improved recall
- Strict prompt-based hallucination control
- A simple frontend interface for interaction


## Technologies Used
- Python 3.12
- LangChain
- ChromaDB (vector database)
- FastEmbed (embeddings)
- Groq LLM (LLaMA 3.1 – 8B)
- Streamlit (frontend)

All library versions are listed in `requirements.txt`.

---

## Project Structure


Step :2

Install required libraries

Install all dependencies using:

pip install -r requirements.txt




Step 3: Set the API key

Create a file named .env in the project root folder.

Add the following line:

GROQ_API_KEY=api_key_here



Replace api_key_here with  actual Groq API key.

Place PDF files inside the data/ folder

Only PDF files are supported

multiple research papers or textbook chapters can be added.



After adding or changing PDF files, run:

python build_kb.py



This will:

Load all PDFs from the data/ folder

Split documents into smaller text chunks

Generate embeddings

Store them in the chroma_db/ folder





To start the chatbot in the terminal, run:

python rag_chatbot.py



Running the Web Interface (Streamlit)
streamlit run app.py






# Final commands:--

source venv/bin/activate
python build_kb.py
python rag_chatbot.py
streamlit run app.py
