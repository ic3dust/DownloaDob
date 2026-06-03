<template>
  <div id="help-sect" class="faq-container">
    <h2 class="game-title faq-main-title">Help & FAQ</h2>
    
    <div class="faq-list">
      <div 
        v-for="(item, index) in faqItems" 
        :key="index" 
        class="faq-item pixel-box"
        :class="{ 'is-active': activeFaq === index }"
      >
        <div class="faq-trigger" @click="toggleFaq(index)">
          <span class="faq-question">
            <span class="faq-prefix">{{ item.prefix }}</span> {{ item.question }}
          </span>
          <span class="faq-arrow">▼</span>
        </div>
        
        <div v-show="activeFaq === index" class="faq-content">
          <p>{{ item.answer }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const activeFaq = ref(null);

const faqItems = ref([
  { 
    prefix: "Question 1:",
    question: "How do I download a video using DOWNLOADOB?", 
    answer: "Simply paste the media link into the input field at the top of the page, click 'Parse', choose your preferred quality and format stream from the generated options, and hit download button." 
  },
  { 
    prefix: "Question 2:",
    question: "Does this tool add watermarks to downloaded media?", 
    answer: "No, all media parsed and saved through our platform is completely free and completely free of watermarks." 
  },
  { 
    prefix: "Question 3:",
    question: "Can I extract just the audio file from a YouTube video?", 
    answer: "Yes! After parsing your link, scroll down to the 'Audio Only Tracks' section, choose your format configuration, and click 'Download Audio'." 
  },
  { 
    prefix: "Question 4:",
    question: "What types of websites/platforms are supported?", 
    answer: "We offer support for prominent video and image media hubs including YouTube, TikTok, X (Twitter), Instagram, and Pinterest." 
  }
]);

const toggleFaq = (index) => {
  activeFaq.value = activeFaq.value === index ? null : index;
};
</script>

<style scoped>
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

.faq-container {
  max-width: 800px;
  margin: 60px auto 100px auto;
  padding: 0 16px;
  box-sizing: border-box;
}

.faq-main-title {
  margin-bottom: 40px !important;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 16px; 
}

.faq-item {
  padding: 0 !important; 
  overflow: hidden;
  transition: border-color 0.2s;
}

.faq-trigger {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  cursor: pointer;
  user-select: none;
  background: var(--code-bg);
  transition: background 0.1s;
}

.faq-trigger:hover {
  background: var(--bg);
}

.faq-question {
  font-size: 22px;
  font-weight: bold;
  color: var(--text);
  text-align: left;
}

.faq-arrow {
  font-size: 18px;
  color: var(--accent);
  transition: transform 0.2s ease;
  display: inline-block;
}

.faq-item.is-active {
  border-color: var(--accent);
}

.faq-item.is-active .faq-arrow {
  transform: rotate(180deg);
}

.faq-content {
  padding: 20px 24px;
  background: var(--bg);
  border-top: 3px solid var(--border);
  text-align: left;
  font-size: 18px;
  line-height: 1.6;
  color: var(--text);
}

.faq-prefix {
  color: var(--accent); 
  margin-right: 6px;    
}

.pixel-box {
  background: var(--code-bg);
  border: 3px solid var(--border);
  box-shadow: var(--pixel-shadow);
  padding: 24px;
  border-radius: 0px !important;
}
</style>