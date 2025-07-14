<template>
    <aside id="alert" :class="{ hide: !visible }">{{ alertText }}</aside>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
    alertText: {
        type: String,
        required: true
    },
    visible: {
        type: Boolean,
        default: false
    }
});
</script>

<style scoped>
.hide {
    visibility: hidden;
}

aside {
    position: absolute;
    transform: translate(135%, -70%);
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
    font-size: 25px;
    width: 400px;
    height: 100px;
    background: var(--matcha-green);
    color: var(--text-primary);
    box-shadow: 0 0 5px 5px rgba(0, 0, 0, 0.3);
    border-radius: 25px;
    animation: borderAnimation 1s linear infinite;
    transition: background-color 0.3s ease, color 0.3s ease;
}

:root.dark aside {
    background: var(--dark-bg-secondary);
    color: var(--dark-text-primary);
    box-shadow: 0 0 5px 5px rgba(255, 255, 255, 0.1);
}

@keyframes borderAnimation {
    0% {
        border: 3px solid transparent;
    }
    50% {
        border: 3px solid var(--matcha-green-dark);
    }
    100% {
        border: 3px solid transparent;
    }
}

:root.dark aside {
    animation: borderAnimationDark 1s linear infinite;
}

@keyframes borderAnimationDark {
    0% {
        border: 3px solid transparent;
    }
    50% {
        border: 3px solid var(--dark-accent);
    }
    100% {
        border: 3px solid transparent;
    }
}
</style>
