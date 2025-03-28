<template>
    <div class="container mt-4">
      <h1>My Decks</h1>
      <div class="mb-3">
        <button class="btn btn-primary" @click="showCreateModal = true">Create New Deck</button>
      </div>
      
      <div class="list-group">
        <router-link 
          v-for="deck in store.decks" 
          :key="deck.id" 
          :to="`/decks/${deck.id}`"
          class="list-group-item list-group-item-action"
        >
          {{ deck.title }}
        </router-link>
      </div>
  
      <div v-if="showCreateModal" class="modal" tabindex="-1" style="display: block; background: rgba(0,0,0,0.5)">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Create New Deck</h5>
              <button type="button" class="btn-close" @click="showCreateModal = false"></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">Deck Title</label>
                <input v-model="newDeck.title" type="text" class="form-control">
              </div>
              <div class="mb-3">
                <label class="form-label">Description (Optional)</label>
                <textarea v-model="newDeck.description" class="form-control"></textarea>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="showCreateModal = false">Cancel</button>
              <button type="button" class="btn btn-primary" @click="createDeck">Create</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useFlashcardStore } from '@/stores/flashcards'
  
  const store = useFlashcardStore()
  const showCreateModal = ref(false)
  const newDeck = ref({
    title: '',
    description: ''
  })
  
  onMounted(async () => {
    await store.fetchDecks()
  })
  
  const createDeck = async () => {
    await store.createDeck(newDeck.value)
    showCreateModal.value = false
    newDeck.value = { title: '', description: '' }
  }
  </script>