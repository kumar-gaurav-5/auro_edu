<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      <router-link class="navbar-brand" to="/">AI Flashcards</router-link>
      <div class="navbar-nav">
        <router-link class="nav-link" to="/decks">Decks</router-link>
        <router-link class="nav-link" to="/review">Review</router-link>
        <router-link class="nav-link" to="/qa">Q&A</router-link>
      </div>
    </div>
  </nav>
  <router-view/>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>