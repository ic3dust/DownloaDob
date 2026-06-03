<template>
  <div class="downloader-container">
    <div class="top">
      <h2 class="game-title">Ultimate media downloader</h2>
    </div>

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
  </div>

  <MediaFetch
    v-if="apiData"
    :api-data="apiData"
    :muxed-streams="muxedStreams"
    :video-only-streams="videoOnlyStreams"
    :audio-streams="audioStreams"
    @download-video="downloadVideo"
    @download-audio="downloadAudio"
  />

  <div class="socials">
    <h2 class="game-title socials-title" style="color:var(--text); background:var(--accent-bg); width:100%; cursor:default; font-size:36px!important;">Free no watermark Video & Audio downloader - DOWNLOADOB (no redirects)</h2>
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

  <HelpFaq />
</template>

<script setup>
import { ref, computed } from "vue";
import { Icon } from '@iconify/vue';
import MediaFetch from "./MediaFetch.vue";
import HelpFaq from "./HelpFaq.vue";

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
  height: 550px;
  background: linear-gradient(
    180deg,
    #16171d00 0%,   
    #16171dcc 50%,   
    #16171dff 100%   
  ), 
  url("/back.png") center top / cover no-repeat;
  box-sizing: border-box;
}

.top {
  width: 100%;
  max-width: 800px;  
  margin: 0 auto;    
  min-height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 40px; 
}

.input-group {
  display: flex;
  gap: 22px;
  max-width: 800px;
  margin: 0 auto 24px auto; 
  padding: 0 16px;
  box-sizing: border-box;
}

.game-title {
  position: relative;
  font-size: 42px;
  text-align: center;
  color: #ffffff; 
  text-shadow: 3px 3px 0px #000000; 
  margin-bottom: 54px;
  z-index: 1;
  cursor: default;
}

@media (max-width: 600px) {
  .input-group {
    flex-direction: column;
  }
}

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

.error-message {
  color: var(--pixel-error);
  font-size: 22px;
}

.socials{
  align-items: center;
  justify-content: center;
  vertical-align: top;
  display: flex;
  flex-direction: column;
  gap:10px;  
  width: 100%;
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