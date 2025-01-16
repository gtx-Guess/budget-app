<template>
    <div>
        <h1>Profile Page</h1>
        <h3>** this is where you will submit the airtable details **</h3>
    </div>
</template>

<script lang="ts" setup>
import { useLocalStore } from '@/stores/localStorage';
import { storeToRefs } from 'pinia';
import axios from 'axios';
const BASE_URL = import.meta.env.VITE_BACKEND_URL;

const localStore = useLocalStore();
</script>

<style scoped lang="scss">
</style>