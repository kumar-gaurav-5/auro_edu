from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, User, Deck, Flashcard, Document
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

# Helper function for spaced repetition
def calculate_next_review(card, performance_rating):
    if performance_rating >= 3:  # Good response
        if card.repetitions == 0:
            card.interval = 1
        elif card.repetitions == 1:
            card.interval = 6
        else:
            card.interval = int(card.interval * card.ease_factor)
        
        card.ease_factor = max(1.3, card.ease_factor + 0.1 - (5 - performance_rating) * (0.08 + (5 - performance_rating) * 0.02))
    else:  # Poor response
        card.interval = 1
        card.ease_factor = max(1.3, card.ease_factor - 0.2)
    
    card.repetitions += 1
    card.next_review = datetime.now() + timedelta(days=card.interval)
    return card

# Flashcard API
@app.route('/api/decks', methods=['GET', 'POST'])
def decks():
    if request.method == 'POST':
        data = request.json
        new_deck = Deck(title=data['title'], description=data.get('description'), user_id=1)  # Hardcoded user for now
        db.session.add(new_deck)
        db.session.commit()
        return jsonify({'id': new_deck.id}), 201
    else:
        decks = Deck.query.filter_by(user_id=1).all()  # Hardcoded user for now
        return jsonify([{'id': deck.id, 'title': deck.title} for deck in decks])

@app.route('/api/flashcards', methods=['POST'])
def create_flashcard():
    data = request.json
    new_card = Flashcard(
        front=data['front'],
        back=data['back'],
        deck_id=data['deck_id'],
        next_review=datetime.now()
    )
    db.session.add(new_card)
    db.session.commit()
    return jsonify({'id': new_card.id}), 201

@app.route('/api/flashcards/review', methods=['GET'])
def get_review_cards():
    cards = Flashcard.query.filter(
        Flashcard.next_review <= datetime.now()
    ).limit(10).all()
    return jsonify([{
        'id': card.id,
        'front': card.front,
        'back': card.back,
        'deck_id': card.deck_id
    } for card in cards])

@app.route('/api/flashcards/<int:card_id>/review', methods=['POST'])
def submit_review(card_id):
    data = request.json
    card = Flashcard.query.get_or_404(card_id)
    card = calculate_next_review(card, data['rating'])
    db.session.commit()
    return jsonify({'message': 'Review submitted'})

# Document API
@app.route('/api/documents', methods=['POST'])
def upload_document():
    data = request.json
    new_doc = Document(
        title=data['title'],
        content=data['content'],
        user_id=1  # Hardcoded user for now
    )
    db.session.add(new_doc)
    db.session.commit()
    return jsonify({'id': new_doc.id}), 201


from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# Initialize model
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.route('/api/documents/<int:doc_id>/embed', methods=['POST'])
def generate_embeddings(doc_id):
    doc = Document.query.get_or_404(doc_id)
    # Split content into chunks (simple implementation)
    chunks = [doc.content[i:i+500] for i in range(0, len(doc.content), 500)]
    embeddings = model.encode(chunks)
    doc.embeddings = {
        'chunks': chunks,
        'embeddings': embeddings.tolist()
    }
    db.session.commit()
    return jsonify({'message': 'Embeddings generated'})

@app.route('/api/qa', methods=['POST'])
def answer_question():
    data = request.json
    question = data['question']
    doc_id = data.get('doc_id')
    
    if doc_id:
        doc = Document.query.get_or_404(doc_id)
        if not doc.embeddings:
            return jsonify({'error': 'Document not processed'}), 400
            
        # Convert to numpy arrays
        chunks = doc.embeddings['chunks']
        embeddings = np.array(doc.embeddings['embeddings'])
        
        # Create FAISS index
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        
        # Search for similar chunks
        question_embedding = model.encode([question])
        k = 3
        distances, indices = index.search(question_embedding, k)
        
        # Simple "generation" - just return the most relevant chunks
        relevant_chunks = [chunks[i] for i in indices[0]]
        return jsonify({
            'answer': "Here's what I found:\n\n" + "\n\n".join(relevant_chunks)
        })
    else:
        return jsonify({'error': 'Document ID required'}), 400


if __name__ == '__main__':
    app.run(debug=True)