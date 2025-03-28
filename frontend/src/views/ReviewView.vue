<template>
    <div class="container mt-4">
      <h1>Review Flashcards</h1>
      
      <div v-if="store.reviewCards.length === 0" class="alert alert-info">
        No cards to review right now. Check back later!
      </div>
  
      <div v-else class="card mb-3">
        <div class="card-body">
          <h5 class="card-title">{{ currentCard.front }}</h5>
          <p v-if="showBack" class="card-text">{{ currentCard.back }}</p>
          <button v-else class="btn btn-primary" @click="showBack = true">Show Answer</button>
          
          <div v-if="showBack" class="mt-3">
            <h6>How well did you know this?</h6>
            <div class="btn-group">
              <button 
                v-for="rating in [1, 2, 3, 4, 5]" 
                :key="rating" 
                class="btn btn-outline-primary"
                @click="submitReview(rating)"
              >
                {{ rating }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useFlashcardStore } from '@/stores/flashcards'
  
  const store = useFlashcardStore()
  const showBack = ref(false)
  
  onMounted(async () => {
    await store.fetchReviewCards()
  })
  
  const currentCard = computed(() => {
    return store.reviewCards.length > 0 ? store.reviewCards[0] : null
  })
  
  const submitReview = async (rating) => {
    await store.submitReview(currentCard.value.id, rating)
    showBack.value = false
  }
  </script>