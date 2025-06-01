<template>
    <div id="app">
        <header class="base-margins-width" v-if="$route.meta.showNavbar">
            <nav>
                <ul class="nav-ul">
                    <router-link to="/">Home</router-link>
                    <router-link to="/connect">Connect Bank</router-link>
                    <router-link to="/profile">Profile</router-link>
                    <router-link to="/transactions">Transactions</router-link>
                    <router-link to="/login" @click="logout">Logout</router-link>
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
axios.defaults.withCredentials = true;

const BASE_URL = import.meta.env.VITE_BACKEND_URL;

const logout = async () => {
    await axios.post(`${BASE_URL}/api/logout`, {}, {
        headers: {
            'Content-Type': 'application/json',
        },
    });
};
</script>

<style>
.nav-ul > * {
    text-decoration: none;
    list-style: none;
    background: none;
    margin: 10px;
    padding: 8px;
    color: inherit;
    display: inline-block;
    font-size: 14pt;
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

.base-margins-width {
    width: 95%;
    margin-left: auto;
    margin-right: auto;
    margin-top: 10px;
}

header {
    background: rgb(115, 253, 216);
    border-radius: 10px;
}

nav {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 60px;
    margin-right: auto;
    margin-left: auto;
}

</style>
