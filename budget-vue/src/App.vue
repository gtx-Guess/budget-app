<template>
    <div id="app">
        <header class="border-matcha"  v-if="$route.meta.showNavbar">
            <nav class="base-margins-width" style="margin-top: 0 !important;">
                <ul class="nav-ul">
                    <router-link to="/" class="nav-brand text-matcha-400">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 6px;"><line x1="18" x2="18" y1="20" y2="10"></line><line x1="12" x2="12" y1="20" y2="4"></line><line x1="6" x2="6" y1="20" y2="14"></line></svg>
                        <span style="font-weight: bold; font-size: 14pt;">Finance Tracker</span>
                    </router-link>
                    <router-link to="/" class="nav-link">Home</router-link>
                    <router-link to="/connect" class="nav-link">Analytics</router-link>
                    <router-link to="/transactions" class="nav-link">Transactions</router-link>
                    <router-link to="/profile" class="nav-link">Profile</router-link>
                    <router-link to="/login" @click="logout" class="nav-link">Logout</router-link>
                </ul>
            </nav>
        </header>
        <main class="base-margins-width">
            <router-view />
        </main>
    </div>
</template>

<script lang="ts" setup>
import { RouterLink } from 'vue-router';
import axios from 'axios';

const logout = async () => {
    await axios.post(`/api/logout`, {}, {
        headers: {
            'Content-Type': 'application/json',
        },
    });
};
</script>

<style>
nav {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: left;
    width: 100%;
    height: 60px;
}

.nav-ul {
    margin: 0;
    padding: 0;
    list-style: none;
}

.nav-ul > * {
    text-decoration: none;
    list-style: none;
    background: none;
    margin: 10px;
    padding: 8px;
    display: inline-flex;
    font-size: 14pt;
    height: 40px;
    box-sizing: border-box;
}

.nav-brand {
    color: rgb(107 155 79) !important;
    transform: translateY(4px);
}

.nav-brand:hover {
    background: none !important;
    cursor: default;
}

.nav-link {
    color: rgba(107, 155, 79, 0.6);
    transition: color 0.2s ease;
}

.nav-link.router-link-active {
    color: rgb(107 155 79);
}

.nav-ul > *:hover {
    cursor: pointer;
    background: white;
    border-radius: 10px;
}

body {
    margin: 0;
    padding: 0;
}

header.border-matcha {
    background: rgb(225 233 219);
    width: 100%;
    padding: 0;
    margin: 0;
}
</style>
