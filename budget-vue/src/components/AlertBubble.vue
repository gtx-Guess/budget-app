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
    position: fixed;
    top: 80px;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 15px 25px;
    font-size: 16px;
    max-width: 500px;
    min-height: 60px;
    background: rgb(107, 155, 79);
    color: white;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    border-radius: 12px;
    z-index: 1000;
    transition: all 0.3s ease;
    font-weight: 600;
    opacity: 1;
}

html.dark aside {
    background: rgb(139, 185, 111);
    color: white;
    box-shadow: 0 4px 20px rgba(255, 255, 255, 0.1);
}

.hide {
    opacity: 0;
    transform: translateX(-50%) translateY(-20px);
    visibility: hidden;
}
</style>
