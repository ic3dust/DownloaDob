import { createRouter, createWebHistory } from 'vue-router';
import App from './pages/app/components/App.vue';
import VideoDownloader from './pages/home/components/VideoDownloader.vue';

const routes = [
  { path: '/getapp', component: App },
  { path: '/', component: VideoDownloader },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;