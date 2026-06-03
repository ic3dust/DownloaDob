<template>
  <main class="min-h-screen py-12 px-4">
    <Header></Header>
    <router-view @loading="loading = $event" />
    <Loading v-if="loading" />
  </main>
</template>

<script setup>
import { ref } from "vue";
import Header from "./pages/home/components/Header.vue";
import Loading from "./pages/Loading.vue";

const loading = ref(false);
</script>