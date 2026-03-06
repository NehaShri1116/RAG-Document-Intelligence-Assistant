# RAG Document Intelligence Assistant

This project is a **Retrieval Augmented Generation (RAG) based document assistant** that allows users to upload documents and ask questions about their content using natural language. Instead of relying only on a language model’s internal knowledge, the system retrieves relevant information from uploaded documents and uses that context to generate accurate and grounded responses.

The application processes uploaded PDF documents by splitting them into smaller semantic chunks and converting them into vector embeddings. These embeddings are stored in a **FAISS vector database**, which enables fast semantic search to find the most relevant document sections for a given query.

When a user asks a question, the system retrieves the most relevant document chunks and sends them to a locally hosted language model through **LangChain and Ollama**. The language model then generates a response using the retrieved context, making the answers more accurate and relevant to the document.

The system also includes a **Streamlit-based interface** that allows users to upload documents, interact through a chat interface, and maintain multiple chat sessions while exploring the uploaded content.

---

## Features

• Upload and analyze PDF documents
• Semantic search using vector embeddings
• Context-aware answers using Retrieval Augmented Generation
• Integration with LangChain and FAISS for document retrieval
• Local LLM inference using Ollama
• Interactive chat interface built with Streamlit
• Multi-session conversation support

---

## Tech Stack

Python
LangChain
FAISS
Ollama (Local LLM)
Streamlit
PyPDF
Sentence Transformers / Embeddings

---

## Use Cases

• Document question answering
• Knowledge base assistants
• Research paper exploration
• Enterprise document search
• AI-powered document analysis
