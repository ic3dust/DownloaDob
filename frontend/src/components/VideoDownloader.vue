<script>import { Icon } from '@iconify/vue'</script>

<template>
  <div class="downloader-container">
    <h2 class="game-title" style="cursor:default;">Ultimate media downloader</h2>

    <div class="input-group">
      <input
        v-model="mediaUrl"
        type="text"
        placeholder="Paste video, image, or audio URL here..."
        class="pixel-input"
        :disabled="loading"
      />
      <button
        @click="parseLink"
        :disabled="loading"
        class="pixel-btn primary"
        style="font-size: 28px"
      >
        {{ loading ? "Parsing..." : "Parse Link" }}
      </button>
    </div>

    <p v-if="error" class="error-message">
      <code>Error: {{ error }}</code>
    </p>

    <div v-if="apiData" class="results-layout pixel-box">
      <div class="media-banner">
        <img
  :src="`http://localhost:8000/api/thumbnail?url=${encodeURIComponent(apiData.thumbnail)}`"
  alt="Media Thumbnail"
  class="thumbnail-img"
/>
        <div class="meta-text">
          <h3>{{ apiData.title }}</h3>
          <p v-if="apiData.duration">
            Duration: {{ formatDuration(apiData.duration) }}
          </p>
        </div>
      </div>

      <div v-if="muxedStreams.length" class="streams-section">
        <h3 class="section-title">Video with Audio</h3>
        <div class="streams-grid">
          <div
            v-for="f in muxedStreams"
            :key="f.format_id"
            class="stream-card pixel-box sub-card"
          >
            <div class="stream-info">
              <div>
                <span class="pixel-badge success">{{ f.ext }}</span>
              </div>
              <span class="resolution-text">{{ f.resolution }}</span>
              <p class="size-text">Adaptive Size</p>
            </div>
            <button
              @click="downloadVideo(f.format_id, true)"
              class="pixel-btn success"
              style="  color: #ffffff !important;
  text-shadow: 1.5px 1.5px 0px #000000 !important;"
            >
              Download
            </button>
          </div>
        </div>
      </div>

      <div v-if="videoOnlyStreams.length" class="streams-section">
        <h3 class="section-title">Available Resolutions</h3>
        <div class="streams-grid">
          <div
            v-for="f in videoOnlyStreams"
            :key="f.format_id"
            class="stream-card pixel-box sub-card"
          >
            <div class="stream-info">
              <div>
                <span class="pixel-badge warning">{{ f.ext }}</span>
              </div>
              <span class="resolution-text">{{ f.resolution }}</span>
              <p class="size-text">{{ formatSize(f.filesize) }}</p>
            </div>
            <div class="btn-group">
              <button
                @click="downloadVideo(f.format_id, false)"
                class="pixel-btn silent"
              >
                Silent
              </button>
              <button
                @click="downloadVideo(f.format_id, true)"
                class="pixel-btn primary"
              >
                + Audio
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="audioStreams.length" class="streams-section">
        <h3 class="section-title">Audio Only Tracks</h3>
        <div class="streams-grid">
          <div
            v-for="f in audioStreams"
            :key="f.format_id"
            class="stream-card pixel-box sub-card"
          >
            <div class="stream-info">
              <div>
                <span class="pixel-badge danger">{{ f.ext }}</span>
              </div>
              <span class="resolution-text">{{ f.resolution }}</span>
              <p class="size-text">{{ formatSize(f.filesize) }} {{ f.note }}</p>
            </div>
            <button
              @click="downloadAudio(f.format_id)"
              class="pixel-btn danger"
              style="  color: #ffffff !important;
  text-shadow: 1.5px 1.5px 0px #000000 !important;"
            >
              Download Audio
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="socials">
    <h2 class="game-title socials-title" style="color:var(--text); background:var(--accent-bg); width:100%; cursor:default;">Free no watermark Video & Audio downloader - DOWNLOADOB (no redirects)</h2>
    <div class="socials-icons">
      <div class="scol1">
        <Icon icon="logos:youtube-icon" width="100" height="100"/>
        <h4 class="game-title">YouTube</h4>
      </div>
      <div class="scol2">
        <Icon icon="logos:tiktok-icon" width="100" height="100"/>
        <h4 class="game-title">TikTok</h4>
      </div>
      <div class="scol3">
        <Icon icon="dinkie-icons:twitter-alt" width="100" height="100"/>
        <h4 class="game-title">X</h4>
      </div>
      <div class="scol4">
        <Icon icon="skill-icons:instagram" width="100" height="100"/>
        <h4 class="game-title">Instagram</h4>
      </div>
      <div class="scol5">
        <Icon icon="pixel:pinterest" width="100" height="100"/>
        <h4 class="game-title">Pinterest</h4>
      </div>
    </div>
  </div>
</template>

<script setup>

import { ref, computed } from "vue";

const API = "http://127.0.0.1:8000/api";

const mediaUrl = ref("");
const loading = ref(false);
const apiData = ref(null);
const error = ref(null);

const emit = defineEmits(["loading"]);

const parseLink = async () => {
  if (!mediaUrl.value) return;

  loading.value = true;
  emit("loading", true);
  error.value = null;
  apiData.value = null;

  try {
    const response = await fetch(`${API}/parse`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: mediaUrl.value }),
    });

    const data = await response.json();

    if (!response.ok || data.error) {
      error.value = data.error || "Failed to parse media.";
      return;
    }

    apiData.value = data;

  } catch (e) {
    error.value = "Could not connect to backend Python API.";
  } finally {
    loading.value = false;
    emit("loading", false);
  }
};

const muxedStreams = computed(
  () => apiData.value?.formats.filter((f) => f.type === "muxed") ?? [],
);
const videoOnlyStreams = computed(
  () => apiData.value?.formats.filter((f) => f.type === "video_only") ?? [],
);
const audioStreams = computed(
  () => apiData.value?.formats.filter((f) => f.type === "audio_only") ?? [],
);

const formatSize = (bytes) => {
  if (!bytes) return "Adaptive Size";
  return `~ ${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

const formatDuration = (seconds) => {
  if (!seconds) return "00:00";
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, "0")}`;
};

const downloadVideo = (formatId, withAudio) => {
  const params = new URLSearchParams({
    url: apiData.value.url,
    format_id: formatId,
    with_audio: withAudio,
  });

  window.open(`${API}/video?${params}`, "_blank");
};

const downloadAudio = (formatId) => {
  const params = new URLSearchParams({
    url: apiData.value.url,
    format_id: formatId,
  });

  window.open(`${API}/audio?${params}`, "_blank");
};
</script>

<style scoped>
.downloader-container {
  width: 100%;
  max-width: 800px;
  margin: 40px auto;
  padding: 0 16px;
}

.game-title {
  font-size: 38px;
  text-align: center;
  color: #ffffff; /* Crisp retro gold */
  text-shadow: 3px 3px 0px #000000; /* Flat, crisp black drop shadow */
  margin-bottom: 54px;
}

.input-group {
  display: flex;
  gap: 22px;
  margin-bottom: 24px;
}

@media (max-width: 600px) {
  .input-group {
    flex-direction: column;
  }
}

/* FIXED: Explicitly stripping browser input profiles */
.pixel-input {
  width: 100%;
  padding: 12px 16px;
  background: var(--code-bg);
  color: var(--text-h);
  border: 3px solid #ffffff;
  border-radius: 0px !important;
  outline: none;
  font-size: 22px;
  box-sizing: border-box;
}

.pixel-input:focus {
  background: var(--bg);
  border-color: var(--accent);
}

/* High Resolution Game Buttons Base */
.pixel-btn {
  all: unset;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 24px;
  border: 3px solid #ffffff; /* Clean layout framing */
  border-radius: 0px !important;
  cursor: pointer;
  box-shadow: var(
    --pixel-shadow
  ); /* This is the block shadow that makes it look like a game block */
  white-space: nowrap;
  box-sizing: border-box;
  transition:
    transform 0.05s,
    box-shadow 0.05s;
  outline: none !important;
}

/* Hover and Click mechanics (Feels like an arcade machine button) */
.pixel-btn:hover {
  transform: translate(-1px, -1px);
  box-shadow: 4px 4px 0px 0px var(--hover);
}

.pixel-btn:active {
  transform: translate(1px, 1px);
  box-shadow: none !important;
}

/* High Contrast Button Color Profiles */
.pixel-btn.primary {
  background: var(--accent);
  color: #ffffff !important; /* Solid white text on purple accent — no text shadows needed! */
  text-shadow: 1.5px 1.5px 0px #000000 !important; /* Flat, crisp black drop shadow */
}
.pixel-btn.primary:hover {
  background: var(--accent-hover) !important;
}

.pixel-btn.success {
  background: var(--pixel-success);
  color: #000000; /* Dark text on bright green for crisp readability */
}

.pixel-btn.danger {
  background: var(--pixel-error);
  color: #ffffff; /* Solid white text on red */
}

.pixel-btn.silent {
  background: var(--code-bg);
  color: var(--text-h);
}

/* Disabled state when analyzing */
.pixel-btn:disabled {
  background: var(--accent-hover) !important;
  color: #94a3b8 !important;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: var(--pixel-shadow) !important;
}
.pixel-btn:disabled:hover {
  background: var(--accent) !important;
}

/* Main game container layouts */
.pixel-box {
  background: var(--code-bg);
  border: 3px solid var(--border);
  box-shadow: var(--pixel-shadow);
  padding: 24px;
  border-radius: 0px !important;
}

.sub-card {
  background: var(--bg);
  padding: 16px;
  margin-bottom: 12px;
}

/* Media Banner details */
.media-banner {
  display: flex;
  gap: 20px;
  border-bottom: 3px solid var(--border);
  padding-bottom: 20px;
  margin-bottom: 24px;
}

@media (max-width: 600px) {
  .media-banner {
    flex-direction: column;
  }
}

.thumbnail-img {
  width: 160px;
  height: auto;
  object-fit: cover;
  border: 3px solid var(--border);
  image-rendering: pixelated;
  border-radius: 0px;
}

.meta-text h3 {
  margin: 0 0 8px 0;
  font-size: 26px;
  color: var(--text-h);
}

/* Streams structural grid mapping */
.streams-section {
  margin-bottom: 24px;
}
.section-title {
  font-size: 24px;
  color: var(--accent);
  margin-bottom: 12px;
  text-align: left;
}

.streams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.stream-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  text-align: left;
}

.stream-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* Crisp Pixel UI Badges */
.pixel-badge {
  display: inline-block;
  padding: 2px 10px;
  border: 2px solid var(--border);
  font-size: 16px;
  color: #000;
  font-weight: bold;
  border-radius: 0px;
}
.pixel-badge.success {
  background: var(--pixel-success);
}
.pixel-badge.warning {
  background: var(--pixel-warning);
}
.pixel-badge.danger {
  background: var(--pixel-error);
  color: #fff;
}

.resolution-text {
  font-size: 22px;
  color: var(--text-h);
}
.size-text {
  font-size: 18px;
  color: var(--text);
  margin: 0;
  white-space: pre-line;
}
.error-message {
  color: var(--pixel-error);
  font-size: 22px;
}
.btn-group {
  display: flex;
  gap: 8px;
}
.pixel-title-shadow {
  color: var(--accent) !important; /* Uses your theme's purple accent */
  text-shadow: 3px 3px 0px var(--black); /* Clean pixel drop shadow matching your layout lines */
}




.socials{
  align-items: center;
  justify-content: center;
  display: flex;
  flex-direction: column;
  gap:10px;  
  width: 100%;
  margin-top: 125px;
}
.socials h4{
  font-size: 26px;
}
.socials-icons {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: max-content;
  gap:100px;
}


</style>
