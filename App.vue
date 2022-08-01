<template>
<div>
  <h2>{{ count }} </h2>
  <button v-on:click="count = count + 1">Increment</button>
  <button v-on:click="count = count - 1">Decrement</button>
</div>
</template>

<script>


export default {
  name: 'App',
  data() {
    return{
      count: 0
    };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>