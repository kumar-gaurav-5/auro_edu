# AI-Powered Document Management & Flashcard Learning System

![App Screenshot](screenshot.png) <!-- Add screenshot later -->

## 📌 Project Overview
A full-stack application combining:
1. **Document Management with RAG-based Q&A**
2. **AI-Powered Flashcard Learning System**

Built with:
- **Frontend**: Vue.js 3 + Pinia
- **Backend**: Flask + SQLAlchemy
- **Database**: PostgreSQL (with SQLite fallback)
- **AI**: Sentence Transformers + FAISS for RAG

## 📋 Features

### Document Management System
- ✅ Document upload & storage
- ✅ Embedding generation using MiniLM-L6-v2
- ✅ Retrieval-Augmented Generation (RAG) Q&A
- ✅ Document selection for context-aware answers

### Flashcard System
- 🃏 Spaced repetition algorithm (SRS)
- 📊 Performance tracking & analytics
- 🤖 AI-generated flashcard suggestions
- 📚 Deck management system

## 🛠️ Tech Stack

| Component       | Technology                          |
|-----------------|-------------------------------------|
| Frontend        | Vue 3, Pinia, Bootstrap 5           |
| Backend         | Flask, Flask-SQLAlchemy             |
| Database        | PostgreSQL (primary), SQLite (fallback) |
| AI/ML           | Sentence Transformers, FAISS        |
| APIs            | RESTful with JSON                   |

## 🚀 Installation

### Prerequisites
- Python 3.10+
- Node.js 16+
- PostgreSQL 15+
- (Optional) Redis for caching

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Initialize database
flask db upgrade
flask run
