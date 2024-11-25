<template>
    <div class="home">
        this is the home view
        {{ user }}
    </div>
</template>

<script lang="ts" setup>
import { useLocalStore } from '@/stores/localStorage';

// Access the store instance
const localStore = useLocalStore();

// Destructure state and methods for convenience
const { user, setUser } = localStore;
</script>

<style scoped lang="scss">
</style>