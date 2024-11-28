<template>
    <div>
        <button :disabled="!ready" @click="connectBank">
            Connect a bank account
        </button>
    </div>
</template>

<script lang="ts" setup>
import axios from 'axios';
import { usePlaidLinkComposable } from '@/composables/usePlaidLinkComposable';
import { PlaidUser } from "@/types/aliases";

const { linkToken, ready, setLinkToken, openPlaidLink } = usePlaidLinkComposable();

const BASE_URL = import.meta.env.VITE_BACKEND_URL;
const PRODUCTS = import.meta.env.VITE_PLAID_PRODUCTS.split(",");

const user = {
    id: "tigran-2204",
};

async function fetchLinkToken(user: PlaidUser) {
    try {
        const response = await axios.post(`${BASE_URL}/api/create_link_token`, {
            client_name: "Tigrans Budget App",
            language: "en",
            country_codes: ["US"],
            user: { client_user_id: user.id },
            products: PRODUCTS,
        }, {
            headers: {
                'Content-Type': 'application/json',
            },
        });

        setLinkToken(response.data.link_token); // Use composable to set the token
        console.log("Fetched Link Token:", linkToken.value);
    } catch (error) {
        console.error("Error fetching link token:", error);
    }
}

async function connectBank() {
    if (ready.value) {
        console.log("Fetching link token...");
        await fetchLinkToken(user);
        if (ready.value) {
            console.error("Failed to fetch link token");
            return;
        }
    }
    openPlaidLink();
}
</script>

<style scoped>
:root {
    font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
    line-height: 1.5;
    font-weight: 400;

    color-scheme: light dark;
    color: rgba(255, 255, 255, 0.87);
    background-color: #242424;

    font-synthesis: none;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

a {
    font-weight: 500;
    color: #646cff;
    text-decoration: inherit;
}

a:hover {
    color: #535bf2;
}

body {
    margin: 0;
    display: flex;
    place-items: center;
    min-width: 320px;
    min-height: 100vh;
}

h1 {
    font-size: 3.2em;
    line-height: 1.1;
}

button {
    border-radius: 8px;
    border: 1px solid transparent;
    padding: 0.6em 1.2em;
    font-size: 1em;
    font-weight: 500;
    font-family: inherit;
    background-color: #1a1a1a;
    cursor: pointer;
    transition: border-color 0.25s;
}

button:hover {
    border-color: #646cff;
}

button:focus,
button:focus-visible {
    outline: 4px auto -webkit-focus-ring-color;
}

.card {
    padding: 2em;
}

@media (prefers-color-scheme: light) {
    :root {
        color: #213547;
        background-color: #ffffff;
    }

    a:hover {
        color: #747bff;
    }

    button {
        background-color: #f9f9f9;
    }
}
</style>
