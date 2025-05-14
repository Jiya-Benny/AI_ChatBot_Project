# 🛐 OCMS Chatbot – AI-Powered Church Management Assistant

![Screenshot 2025-05-14 215430](https://github.com/user-attachments/assets/d8b4b733-4347-428a-8e00-548bb1db2482)

## 📌 Project Overview

**OCMS Chatbot** is an AI-integrated chatbot designed to assist users in managing and retrieving information related to a Church Management System. It intelligently processes queries and responds using SQL database mapping and RAG (Retrieval-Augmented Generation), providing human-friendly, precise answers.

> ✨ Backend: Python (FastAPI)  
> ✨ Frontend: React.js  
> ✨ AI: HuggingFace Transformers, Groq API (LLaMA3), Sentence Transformers, Qdrant

---

## 🧠 Features

- 🔍 Flexible SQL querying using sentence transformer (`all-MiniLM-L6-v2`)
- 🧾 RAG implementation using **Qdrant + LlamaIndex**
- 🤖 LLaMA3 model from **Groq API** for natural, human-friendly responses
- 🧠 Hybrid logic: combines SQL intent mapping with RAG fallback
- 💬 Interactive chatbot UI (pop-up window) built in **React**
- 📁 Scroll, loading animation, and formatted markdown responses

---

## 🧱 Tech Stack

| Area       | Technology                     |
|------------|--------------------------------|
| Frontend   | React, CSS                     |
| Backend    | FastAPI (Python)               |
| Database   | SQL Server                     |
| Vector DB  | Qdrant (via Docker)            |
| AI Models  | Sentence Transformers, LLaMA3  |
| Hosting    | Localhost / Azure (optional)   |

---

## 📂 Folder Structure
/ocms-chatbot
│
├── backend/
│ ├── main.py
│ ├── query_handler.py
│ └── llm_engine.py
│
├── frontend/
│ ├── public/
│ ├── src/
│ │ ├── ChatbotPopup.js
│ │ ├── ChatWindow.js
│ │ └── styles.css
│
├── embeddings/
│ ├── phrase_embeddings.npy
│ ├── query_keys.npy
│ └── query_values.npy
│
└── README.md


---

## 🚀 Getting Started

### 📦 Backend Setup (FastAPI)

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn sentence-transformers qdrant-client numpy
   ```

3. **Run FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```


---

## 💻 Frontend Setup (React)

To set up and run the frontend of the OCMS chatbot, follow these steps:

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install the required dependencies**:
   ```bash
   npm install
   ```

3. **Start the React development server**:
   ```bash
   npm run dev
   ```

4.**Open your browser and go to**:
   ```bash
   http://localhost:3000
   ```


---

## 📈 Future Enhancements

- 🌐 Add multilingual (language translation) support
- 🧠 Improve LLM response accuracy using user feedback
- 🎙️ Integrate voice-based chat input
- 📊 Admin dashboard for monitoring chatbot logs and performance
