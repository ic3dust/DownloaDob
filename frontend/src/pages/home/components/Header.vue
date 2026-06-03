<template>
    <div class="H-container">
        <h2 class="H-game-title">DOWNLOADOB</h2>

        <div class="H-comps">
            <router-link to="/">Home</router-link>
            <router-link to="/getapp">Install app</router-link>
            <a href="#help-sect">Help</a>
            <div class="dropdown-wrapper" v-blur-dropdown="closeDropdown">
                <button class="dropdown-trigger" @click="toggleDropdown">
                    <span :class="`fi fi-${currentLanguage.flagClass} flag-icon`"></span>
                    <span class="lang-text">{{ currentLanguage.name }}</span>
                    <span class="arrow-triangle" :class="{ open: isOpen }"></span>
                </button>

                <ul v-if="isOpen" class="dropdown-menu">
                    <li 
                        v-for="lang in languages" 
                        :key="lang.code"
                        @click="selectLanguage(lang)"
                        class="dropdown-item"
                        :class="{ active: lang.code === currentLanguage.code }"
                    >
                        <span :class="`fi fi-${lang.flagClass} flag-icon`"></span>
                        {{ lang.name }}
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

onMounted(() => {
  if (!document.getElementById('flag-icons-cdn')) {
    const link = document.createElement('link');
    link.id = 'flag-icons-cdn';
    link.rel = 'stylesheet';
    link.href = 'https://cdn.jsdelivr.net/gh/lipis/flag-icons@7.2.3/css/flag-icons.min.css';
    document.head.appendChild(link);
  }
});

const isOpen = ref(false);

const languages = ref([
  { code: 'en', name: 'English', flagClass: 'us' },
  { code: 'es', name: 'Español', flagClass: 'es' },
  { code: 'fr', name: 'Français', flagClass: 'fr' },
  { code: 'de', name: 'Deutsch', flagClass: 'de' },
]);

const currentLanguage = ref(languages.value[0]);

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

const selectLanguage = (lang) => {
  currentLanguage.value = lang;
  isOpen.value = false;
};

const closeDropdown = () => {
  isOpen.value = false;
};

const vBlurDropdown = {
  mounted(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value();
      }
    };
    document.addEventListener('click', el.clickOutsideEvent);
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent);
  }
};
</script>

<style scoped>
.H-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    height: 75px;
    background: 
        repeating-conic-gradient(rgba(0,0,0,0) 0% 25%, rgba(0,0,0,0.25) 0% 50%) 0 0 / 6px 6px,
        
        linear-gradient(
            to bottom,
            rgba(0, 0, 0, 0) 0%,
            rgba(7, 6, 26, 0.3) 30%,
            rgba(7, 6, 26, 0.7) 70%,
            #07061a 100%
        ),
        
        linear-gradient(
            to bottom,
            var(--hover) 0%,
            #3d1469 10%, 
            #1d0b33 55%, 
            #07061a 100%
        );

    image-rendering: pixelated;
    
}
.H-comps{
    display:grid;
    grid-auto-flow: column;
    grid-auto-columns: max-content;
    justify-content: center;
    align-items: center;
    margin: 0;
    padding: 0 40px;
    box-sizing: border-box;
    gap:40px;
}
.H-comps span, .H-comps a{
    text-align: center;
    font-size: 24px;
    cursor:default;
    transform: scale(1);
    transition: all 0.3s ease;
    color: var(--text);
    text-decoration: none;
}
.H-comps span:hover, .H-comps a:hover{
    transition: all 0.3s ease;
    transform: scale(1.05);
    color: white;
}
.H-game-title {
    text-align: center; 
    display: inline-block;
    padding: 0px 40px;
    line-height:1;
    margin:0;
    font-size: 38px;
    color: var(--text); 
    text-shadow: 3px 3px 0px #000000; 
    z-index: 1;
    cursor: default;
}

.dropdown-wrapper {
    position: relative;
    display: inline-block;
}

.dropdown-trigger {
    background: transparent;
    border: none;
    padding: 0;
    margin: 0;
    font-family: inherit;
    display: flex;
    align-items: center;
    cursor: default;
    gap: 10px;
}

.dropdown-trigger .flag-icon,
.dropdown-trigger .lang-text {
    transform: scale(1);
    transition: all 0.3s ease;
}

.dropdown-trigger:hover .flag-icon,
.dropdown-trigger:hover .lang-text {
    transform: scale(1.05);
    color: white;
}

/* Adjusted to scale closely down into the text font sizing context nicely */
.flag-icon {
    display: inline-block;
    width: 18px;
    height: 13.5px;
    line-height: 1;
    box-shadow: 1px 1px 0px #000000;
}

/* Custom CSS-drawn mini triangle styling */
.arrow-triangle {
    display: inline-block;
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid var(--text);
    opacity: 0;
    transform-origin: center 3px;
    transition: opacity 0.3s ease, transform 0.3s ease, border-top-color 0.3s ease !important;
}

.dropdown-trigger:hover .arrow-triangle {
    opacity: 1;
    border-top-color: white;
}

.arrow-triangle.open {
    opacity: 1;
    border-top-color: white;
    transform: rotate(180deg) scale(1.05) !important;
}

.dropdown-menu {
    position: absolute;
    top: calc(100% + 10px);
    right: 0;
    background: #1d0b33;
    border: 2px solid #3d1469;
    box-shadow: 4px 4px 0px #000000;
    padding: 5px 0;
    margin: 0;
    list-style: none;
    min-width: 160px;
    z-index: 100;
}

.dropdown-item {
    font-size: 20px;
    color: var(--text);
    padding: 10px 15px;
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: default;
    white-space: nowrap;
    transition: all 0.2s ease;
}

.dropdown-item .flag-icon,
.dropdown-item {
    transition: all 0.3s ease;
}

.dropdown-item:hover {
    background: #501986;
    color: white;
}

.dropdown-item:hover .flag-icon {
    transform: scale(1.05);
}

.dropdown-item.active {
    color: #ffd700;
}
</style>