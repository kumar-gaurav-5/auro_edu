<template>
    <div class="container mt-4">
      <h1>Document Q&A</h1>
      
      <div class="mb-3">
        <select v-model="selectedDoc" class="form-select">
          <option v-for="doc in documents" :key="doc.id" :value="doc.id">
            {{ doc.title }}
          </option>
        </select>
        <button class="btn btn-primary mt-2" @click="processDocument">Process Document</button>
      </div>
      
      <div class="mb-3">
        <textarea v-model="question" class="form-control" placeholder="Ask a question"></textarea>
        <button class="btn btn-primary mt-2" @click="askQuestion">Ask</button>
      </div>
      
      <div v-if="answer" class="card">
        <div class="card-body">
          <h5 class="card-title">Answer</h5>
          <p class="card-text">{{ answer }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  
  const documents = ref([])
  const selectedDoc = ref(null)
  const question = ref('')
  const answer = ref('')
  
  onMounted(async () => {
    const response = await axios.get('http://localhost:5000/api/documents')
    documents.value = response.data
  })
  
  const processDocument = async () => {
    await axios.post(`http://localhost:5000/api/documents/${selectedDoc.value}/embed`)
    alert('Document processed for Q&A!')
  }
  
  const askQuestion = async () => {
    const response = await axios.post('http://localhost:5000/api/qa', {
      question: question.value,
      doc_id: selectedDoc.value
    })
    answer.value = response.data.answer
  }
  </script>