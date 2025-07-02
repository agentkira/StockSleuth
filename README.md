# 💸 StockSleuth

**StockSleuth** is an AI-powered financial market assistant that allows users to ask questions about stocks, upload PDFs, and explore financial trends. It leverages a Retrieval-Augmented Generation (RAG) architecture backed by a FastAPI backend and a sleek TailwindCSS + React frontend.

---

## 🚀 Features

- 🔎 Ask questions like _"Is AAPL a good buy?"_
- 📄 Upload PDF documents for contextual question-answering
- 💬 View full conversation history
- 🔄 Live typing effect for responses
- 🌙 Dark mode toggle
- 🧠 Local vector store using ChromaDB with HuggingFace embeddings

---

## 🧰 Tech Stack

| Component      | Technology                              |
|----------------|------------------------------------------|
| Frontend       | React, TailwindCSS                       |
| Backend        | FastAPI                                  |
| Embeddings     | HuggingFace (`all-MiniLM-L6-v2`)         |
| Vector Store   | ChromaDB                                 |
| Database       | PostgreSQL                               |
| LLM Backbone   | Gemini API                               |
| Data Sources   | yFinance, Wikipedia, NewsAPI             |
| PDF Parsing    | PyPDF / pdfplumber                       |




