<template>
  <div class="overlay">
    <div class="dna">
      <div class="strand s1">
        <div class="dot d1"></div>
        <div class="dot d2"></div>
        <div class="dot d3"></div>
        <div class="dot d4"></div>
        <div class="dot d5"></div>
        <div class="dot d6"></div>
        <div class="dot d7"></div>
        <div class="dot d8"></div>
      </div>
      <div class="strand s2">
        <div class="dot d1"></div>
        <div class="dot d2"></div>
        <div class="dot d3"></div>
        <div class="dot d4"></div>
        <div class="dot d5"></div>
        <div class="dot d6"></div>
        <div class="dot d7"></div>
        <div class="dot d8"></div>
      </div>
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

.dna {
  position: relative;
  width: 120px;
  height: 40px;
  display: flex;
  justify-content: space-between;
}

.strand {
  position: absolute;
  inset: 0;
  display: flex;
  justify-content: space-between;
}

.dot {
  width: 6px;
  height: 6px;
  background: white;
  animation: dna-spin 1.6s infinite ease-in-out;
}

.s2 .dot {
  animation-delay: -0.8s;
  background: rgba(250, 250, 250, 0.7);
}

.d1 { animation-delay: calc(0.0s); }
.d2 { animation-delay: calc(-0.15s); }
.d3 { animation-delay: calc(-0.3s); }
.d4 { animation-delay: calc(-0.45s); }
.d5 { animation-delay: calc(-0.6s); }
.d6 { animation-delay: calc(-0.75s); }
.d7 { animation-delay: calc(-0.9s); }
.d8 { animation-delay: calc(-1.05s); }

.s2 .d1 { animation-delay: calc(0.0s - 0.8s); }
.s2 .d2 { animation-delay: calc(-0.15s - 0.8s); }
.s2 .d3 { animation-delay: calc(-0.3s - 0.8s); }
.s2 .d4 { animation-delay: calc(-0.45s - 0.8s); }
.s2 .d5 { animation-delay: calc(-0.6s - 0.8s); }
.s2 .d6 { animation-delay: calc(-0.75s - 0.8s); }
.s2 .d7 { animation-delay: calc(-0.9s - 0.8s); }
.s2 .d8 { animation-delay: calc(-1.05s - 0.8s); }

@keyframes dna-spin {
  0%, 100% {
    transform: translateY(-20px) scale(1.3);
    z-index: 2;
  }
  50% {
    transform: translateY(20px) scale(0.7);
    z-index: 1;
    opacity: 0.5;
  }
}

.text {
  text-align: center;
  margin-top: 30px;
  color: white;
  font-size: 24px;
  opacity: 0.8;
  letter-spacing: 1px;
}
</style>