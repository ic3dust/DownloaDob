<template>
  <div class="overlay">
    <div class="ring">
      <div class="dot d1"></div>
      <div class="dot d2"></div>
      <div class="dot d3"></div>
      <div class="dot d4"></div>
      <div class="dot d5"></div>
      <div class="dot d6"></div>
      <div class="dot d7"></div>
      <div class="dot d8"></div>
    </div>

    <p class="text">
      {{ loadingText }}
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";

const loadingText = ref("Parsing");

const states = [
  "Parsing",
  "Parsing.",
  "Parsing..",
  "Parsing..."
];

let index = 0;
let interval;

onMounted(() => {
  interval = setInterval(() => {
    index = (index + 1) % states.length;
    loadingText.value = states[index];
  }, 250);
});

onBeforeUnmount(() => {
  clearInterval(interval);
});
</script>

<style scoped>
/* -------------------------
   FULLSCREEN OVERLAY
------------------------- */
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(4px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

/* -------------------------
   ROTATING RING
------------------------- */
.ring {
  width: 50px;
  height: 50px;
  position: relative;
  animation: spin 1.4s linear infinite;
}

/* -------------------------
   PIXEL DOTS
------------------------- */
.dot {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 6px;
  height: 6px;
  background: white;
  opacity: 0.2;
  transform-origin: 0 0;
}

.d1 { transform: rotate(0deg) translate(22px); }
.d2 { transform: rotate(45deg) translate(22px); }
.d3 { transform: rotate(90deg) translate(22px); }
.d4 { transform: rotate(135deg) translate(22px); }
.d5 { transform: rotate(180deg) translate(22px); }
.d6 { transform: rotate(225deg) translate(22px); }
.d7 { transform: rotate(270deg) translate(22px); }
.d8 { transform: rotate(315deg) translate(22px); }

/* -------------------------
   ROTATION
------------------------- */
@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}

/* -------------------------
   OPACITY PULSE
------------------------- */
.dot {
  animation: fade 1.2s infinite ease-in-out;
}

.d1 { animation-delay: 0s; }
.d2 { animation-delay: 0.15s; }
.d3 { animation-delay: 0.3s; }
.d4 { animation-delay: 0.45s; }
.d5 { animation-delay: 0.6s; }
.d6 { animation-delay: 0.75s; }
.d7 { animation-delay: 0.9s; }
.d8 { animation-delay: 1.05s; }

@keyframes fade {
  0%, 100% { opacity: 0.15; }
  50% { opacity: 1; }
}

/* -------------------------
   TEXT
------------------------- */
.text {

  text-align: center;
  margin-top: 20px;
  color: white;
  font-size: 20px;
  opacity: 0.8;
  letter-spacing: 1px;
}
</style>