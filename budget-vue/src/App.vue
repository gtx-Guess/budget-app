<template>
    <div id="app">
        <header class="border-matcha"  v-if="$route.meta.showNavbar">
            <nav class="base-margins-width flex flex-row items-center justify-between" style="margin-top: 0 !important;">
                <router-link to="/" class="nav-brand text-matcha-400 items-center cursor-default">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 6px;"><line x1="18" x2="18" y1="20" y2="10"></line><line x1="12" x2="12" y1="20" y2="4"></line><line x1="6" x2="6" y1="20" y2="14"></line></svg>
                    <span class="brand-text" style="font-weight: bold; font-size: 15pt;">Finance Tracker</span>
                </router-link>
                
                <div class="nav-links flex items-center">
                    <router-link to="/" class="nav-link text-matcha-600 transition-color items-center rounded-md transition-all cursor-pointer">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="nav-icon flex-shrink-0"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9,22 9,12 15,12 15,22"></polyline></svg>
                        <span class="nav-text">Home</span>
                    </router-link>
                    <router-link to="/transactions" class="nav-link text-matcha-600 transition-color items-center rounded-md transition-all cursor-pointer">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="nav-icon flex-shrink-0"><line x1="8" x2="21" y1="6" y2="6"></line><line x1="8" x2="21" y1="12" y2="12"></line><line x1="8" x2="21" y1="18" y2="18"></line><line x1="3" x2="3.01" y1="6" y2="6"></line><line x1="3" x2="3.01" y1="12" y2="12"></line><line x1="3" x2="3.01" y1="18" y2="18"></line></svg>
                        <span class="nav-text">Transactions</span>
                    </router-link>
                    <router-link to="/analytics" class="nav-link text-matcha-600 transition-color items-center rounded-md transition-all cursor-pointer">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="nav-icon flex-shrink-0"><line x1="18" x2="18" y1="20" y2="10"></line><line x1="12" x2="12" y1="20" y2="4"></line><line x1="6" x2="6" y1="20" y2="14"></line></svg>
                        <span class="nav-text">Analytics</span>
                    </router-link>
                    <router-link to="/profile" class="nav-link text-matcha-600 transition-color items-center rounded-md transition-all cursor-pointer">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="nav-icon flex-shrink-0"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                        <span class="nav-text">Profile</span>
                    </router-link>
                    <router-link to="/login" @click="logout" class="nav-link text-matcha-600 transition-color items-center rounded-md transition-all cursor-pointer">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="nav-icon flex-shrink-0"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16,17 21,12 16,7"></polyline><line x1="21" x2="9" y1="12" y2="12"></line></svg>
                        <span class="nav-text">Logout</span>
                    </router-link>
                </div>
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
    width: 100%;
    height: 60px;
}

.nav-links {
    gap: 10px;
}

.nav-link {
    text-decoration: none;
    background: none;
    padding: 8px;
    display: inline-flex;
    gap: 6px;
    font-size: 14pt;
    height: 40px;
    box-sizing: border-box;
}

.nav-brand {
    display: inline-flex;
    text-decoration: none;
    background: none;
    padding: 8px;
    height: 40px;
    box-sizing: border-box;
}

.nav-brand {
    color: rgb(107 155 79) !important;
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

.nav-link:hover {
    background: white;
}

.nav-icon {
    flex-shrink: 0;
}

/* Responsive Navigation */
@media (max-width: 846px) {
    .brand-text {
        font-size: 14pt !important;
    }
    
    .nav-text {
        display: none;
    }
    
    .nav-link {
        padding: 8px;
        min-width: 40px;
        justify-content: center;
    }
    
    .nav-links {
        gap: 5px;
    }
}

@media (max-width: 480px) {
    .brand-text {
        font-size: 14pt !important;
    }
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
