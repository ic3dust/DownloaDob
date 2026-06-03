<template>
  <div class="results-layout pixel-box">
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
            @click="$emit('downloadVideo', f.format_id, true)"
            class="pixel-btn success"
            style="color: #ffffff !important; text-shadow: 1.5px 1.5px 0px #000000 !important;"
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
              @click="$emit('downloadVideo', f.format_id, false)"
              class="pixel-btn silent"
            >
              Silent
            </button>
            <button
              @click="$emit('downloadVideo', f.format_id, true)"
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
            @click="$emit('downloadAudio', f.format_id)"
            class="pixel-btn danger"
            style="color: #ffffff !important; text-shadow: 1.5px 1.5px 0px #000000 !important;"
          >
            Download Audio
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  apiData: Object,
  muxedStreams: Array,
  videoOnlyStreams: Array,
  audioStreams: Array
});

defineEmits(["downloadVideo", "downloadAudio"]);

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
</script>

<style scoped>
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
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  width: 100%;
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
.btn-group {
  display: flex;
  gap: 8px;
}
.pixel-btn {
  all: unset;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 24px;
  border: 3px solid #ffffff; 
  border-radius: 0px !important;
  cursor: pointer;
  box-shadow: var(--pixel-shadow); 
  white-space: nowrap;
  box-sizing: border-box;
  transition: transform 0.05s, box-shadow 0.05s;
  outline: none !important;
}

.pixel-btn:hover {
  transform: translate(-1px, -1px);
  box-shadow: 4px 4px 0px 0px var(--hover);
}

.pixel-btn:active {
  transform: translate(1px, 1px);
  box-shadow: none !important;
}

.pixel-btn.primary {
  background: var(--accent);
  color: #ffffff !important; 
  text-shadow: 1.5px 1.5px 0px #000000 !important; 
}
.pixel-btn.primary:hover {
  background: var(--accent-hover) !important;
}

.pixel-btn.success {
  background: var(--pixel-success);
  color: #000000; 
}

.pixel-btn.danger {
  background: var(--pixel-error);
  color: #ffffff; 
}

.pixel-btn.silent {
  background: var(--code-bg);
  color: var(--text-h);
}
</style>