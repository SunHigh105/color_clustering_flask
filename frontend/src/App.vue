<template>
  <div id="app">
    <header>
      <h2>Image Color Clustering</h2>
      <nav>
        <ul>
          <router-link tag="li" to="/upload"><a>Upload</a></router-link>
          <router-link tag="li" to="/list"><a>File List</a></router-link>
        </ul>
      </nav>
    </header>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
