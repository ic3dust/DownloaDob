<template>
  <div class="downloader-container">
    <h2>Ultimate Link Downloader</h2>

    <div class="input-group">
      <input
        v-model="mediaUrl"
        type="text"
        placeholder="Paste video, image, or audio URL here..."
        class="custom-input"
        :disabled="loading"
      />
      <button @click="parseLink" :disabled="loading" class="counter">
        {{ loading ? "Analyzing..." : "Parse Link" }}
      </button>
    </div>

    <p v-if="error" class="error-message">
      <code>Error: {{ error }}</code>
    </p>

    <div v-if="apiData" class="results-layout">
      <div class="media-banner">
        <img
          :src="apiData.thumbnail"
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
        <h3>Video with Audio</h3>
        <div class="streams-grid">
          <div v-for="f in muxedStreams" :key="f.format_id" class="stream-card">
            <div class="stream-info">
              <span class="ext-badge">{{ f.ext }}</span>
              <span class="resolution-text">{{ f.resolution }}</span>
              <p class="size-text">{{ formatSize(f.filesize) }}</p>
            </div>
            <!-- Only this button changes, in the muxed section -->
            <button
              @click="downloadVideo(f.format_id, true)"
              class="download-action-btn"
            >
              Download
            </button>
          </div>
        </div>
      </div>

      <div v-if="videoOnlyStreams.length" class="streams-section">
        <h3>Available Resolutions</h3>
        <div class="streams-grid">
          <div
            v-for="f in videoOnlyStreams"
            :key="f.format_id"
            class="stream-card"
          >
            <div class="stream-info">
              <span class="ext-badge">{{ f.ext }}</span>
              <span class="resolution-text">{{ f.resolution }}</span>
              <p class="size-text">{{ formatSize(f.filesize) }}</p>
            </div>
            <div class="btn-group">
              <button
                @click="downloadVideo(f.format_id, false)"
                class="download-action-btn silent-btn"
                title="Download without audio"
              >
                Silent
              </button>
              <button
                @click="downloadVideo(f.format_id, true)"
                class="download-action-btn"
                title="Download with best audio merged"
              >
                + Audio
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="audioStreams.length" class="streams-section">
        <h3>Audio Only Tracks</h3>
        <div class="streams-grid">
          <div v-for="f in audioStreams" :key="f.format_id" class="stream-card">
            <div class="stream-info">
              <span class="ext-badge audio-badge">{{ f.ext }}</span>
              <span class="resolution-text">{{ f.resolution }}</span>
              <p class="size-text">{{ formatSize(f.filesize) }} {{ f.note }}</p>
            </div>
            <button
              @click="downloadAudio(f.format_id)"
              class="download-action-btn"
            >
              Download Audio
            </button>
          </div>
        </div>
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

const parseLink = async () => {
  if (!mediaUrl.value) return;
  loading.value = true;
  error.value = null;
  apiData.value = null;

  try {
    const response = await fetch(`${API}/parse`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: mediaUrl.value }),
    });
    const data = await response.json();
    if (data.error) {
      error.value = data.error;
    } else {
      apiData.value = data;
    }
  } catch {
    error.value = "Could not connect to backend Python API.";
  } finally {
    loading.value = false;
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
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

const formatDuration = (seconds) => {
  if (!seconds) return "00:00";
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, "0")}`;
};

// Always use apiData.url (the original page URL) — never per-format stream URLs
const downloadVideo = (formatId, withAudio) => {
  const params = new URLSearchParams({
    url: apiData.value.url,
    format_id: formatId,
    with_audio: withAudio,
  });
  window.open(`${API}/download-video?${params}`, "_blank");
};

const downloadAudio = (formatId) => {
  const params = new URLSearchParams({
    url: apiData.value.url,
    format_id: formatId,
  });
  window.open(`${API}/download-audio?${params}`, "_blank");
};
</script>

<style scoped>
.downloader-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
  box-sizing: border-box;
}

.input-group {
  display: flex;
  gap: 12px;
  margin-top: 16px;
  margin-bottom: 24px;
}

@media (max-width: 600px) {
  .input-group {
    flex-direction: column;
  }
}

.custom-input {
  flex: 1;
  font-family: var(--sans);
  font-size: 16px;
  padding: 12px 16px;
  background: var(--code-bg);
  color: var(--text-h);
  border: 1px solid var(--border);
  border-radius: 6px;
  outline: none;
}

.custom-input:focus {
  border-color: var(--accent);
}

.counter {
  margin-bottom: 0;
  cursor: pointer;
  align-items: center;
  justify-content: center;
}

.error-message {
  margin: 16px 0;
  color: #ef4444;
}

.results-layout {
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 24px;
  text-align: left;
  background: var(--bg);
  box-shadow: var(--shadow);
}

.media-banner {
  display: flex;
  gap: 20px;
  border-bottom: 1px solid var(--border);
  padding-bottom: 20px;
  margin-bottom: 24px;
}

@media (max-width: 600px) {
  .media-banner {
    flex-direction: column;
  }
}

.thumbnail-img {
  width: 180px;
  height: auto;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid var(--border);
}

.meta-text h3 {
  margin: 0 0 6px 0;
  font-size: 20px;
  color: var(--text-h);
}

.streams-section {
  margin-bottom: 28px;
}

.streams-section h3 {
  font-size: 16px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text);
  margin-bottom: 12px;
}

.streams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 12px;
}

.stream-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px;
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 6px;
}

.ext-badge {
  font-family: var(--mono);
  font-size: 11px;
  font-weight: bold;
  padding: 2px 6px;
  background: var(--accent-bg);
  color: var(--accent);
  border: 1px solid var(--accent-border);
  border-radius: 4px;
  text-transform: uppercase;
  margin-right: 8px;
}

.audio-badge {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  border-color: rgba(59, 130, 246, 0.4);
}

.resolution-text {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-h);
}

.size-text {
  font-size: 12px;
  color: var(--text);
  margin: 4px 0 0 0;
}

.btn-group {
  display: flex;
  gap: 6px;
  flex-shrink: 0;
}

.download-action-btn {
  font-family: var(--sans);
  font-size: 13px;
  font-weight: 500;
  padding: 8px 14px;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: opacity 0.2s;
  white-space: nowrap;
}

.download-action-btn:hover {
  opacity: 0.9;
}

.silent-btn {
  background: var(--code-bg);
  color: var(--text);
  border: 1px solid var(--border);
}

.silent-btn:hover {
  opacity: 0.8;
}
</style>
