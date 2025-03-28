import { defineStore } from 'pinia'
import axios from 'axios'

export const useFlashcardStore = defineStore('flashcards', {
  state: () => ({
    decks: [],
    currentDeck: null,
    reviewCards: []
  }),
  actions: {
    async fetchDecks() {
      const response = await axios.get('http://localhost:5000/api/decks')
      this.decks = response.data
    },
    async createDeck(deck) {
      await axios.post('http://localhost:5000/api/decks', deck)
      await this.fetchDecks()
    },
    async createFlashcard(flashcard) {
      await axios.post('http://localhost:5000/api/flashcards', flashcard)
    },
    async fetchReviewCards() {
      const response = await axios.get('http://localhost:5000/api/flashcards/review')
      this.reviewCards = response.data
    },
    async submitReview(cardId, rating) {
      await axios.post(`http://localhost:5000/api/flashcards/${cardId}/review`, { rating })
      await this.fetchReviewCards()
    }
  }
})