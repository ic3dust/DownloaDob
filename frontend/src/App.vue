<template>
  <main class="min-h-screen py-12 px-4">
    <VideoDownloader @loading="loading = $event" />
    <Loading v-if="loading" />
  </main>
</template>

<script setup>
import { ref } from "vue";
import VideoDownloader from "./components/VideoDownloader.vue";
import Loading from "./components/Loading.vue";

const loading = ref(false);
</script>