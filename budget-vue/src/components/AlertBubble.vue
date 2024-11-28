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
    background: #ffabe4;
    box-shadow: 0 0 5px 5px rgba(0, 0, 0, 0.3);
    border-radius: 25px;
    animation: borderAnimation 1s linear infinite;
}

@keyframes borderAnimation {
    0% {
        border: 3px solid transparent;
    }
    50% {
        border: 3px solid blue;
    }
    100% {
        border: 3px solid transparent;
    }
}
</style>
