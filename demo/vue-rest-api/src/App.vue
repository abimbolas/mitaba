<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'app'
}
</script>

<style>

@import url('https://fonts.googleapis.com/css?family=Alegreya+Sans:300,400|PT+Mono');

#app {
  font-family: 'Alegreya Sans', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}

code {
  font-family: PT Mono;
  background-color: ghostwhite;
  font-size: 75%;
  padding: 3px 0px;
  word-break: break-word;
}
</style>
