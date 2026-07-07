# Research Insights Chatbot using RAG

The Research Insights Chatbot is an AI-powered application that enables users to interact with academic research papers using natural language. The system implements Retrieval-Augmented Generation (RAG) to retrieve relevant information from PDF documents and generate accurate, context-aware, citation-backed answers using the Groq Llama 3 model.

Research papers are processed by extracting text, splitting it into meaningful chunks, generating embeddings using HuggingFace models, and storing them in ChromaDB for efficient semantic retrieval. When a user submits a query, the system retrieves the most relevant document sections and uses the Groq LLM to generate responses based only on the retrieved context, reducing hallucinations and improving answer reliability.

The application also includes a secure authentication system with user registration, login, and logout functionality, along with a role-based admin panel. Administrators can view registered users, monitor user count, block or unblock users, and delete user accounts.

## Key Features

* Retrieval-Augmented Generation (RAG)
* Semantic search across research papers
* Citation-backed answers with paper title and page number
* Groq Llama 3 integration
* ChromaDB vector database
* HuggingFace embeddings
* PDF ingestion and text chunking
* Secure user registration, login, and logout
* Role-based admin dashboard
* User management (view, block, unblock, delete users)
* Streamlit-based interactive interface

## Tech Stack

* Python
* Streamlit
* LangChain
* ChromaDB
* Groq API (Llama 3)
* HuggingFace Sentence Transformers
* PyPDF
* SQLite
