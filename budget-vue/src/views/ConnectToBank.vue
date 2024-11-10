<template>
    <div>
        <button :disabled="ready" @click="fetchLinkToken(user)">
            Connect a bank account
        </button>
    </div>
</template>

<script lang="ts" setup>
import { ref, computed, watch } from 'vue';
import axios from 'axios';
import { usePlaidLink } from '@jcss/vue-plaid-link';
import { PlaidUser } from "@/types/aliases";

// Set BASE_URL to the FastAPI backend URL
const BASE_URL = import.meta.env.VITE_BACKEND_URL;
const PRODUCTS = import.meta.env.VITE_PLAID_PRODUCTS.split(",");

// Reactive variable to store the link token and ready state
const linkToken = ref('');
const ready = ref(false);

const user = {
    "id": "tigran-2204"
};

// Function to fetch link token
async function fetchLinkToken(user: PlaidUser) {
    console.log(user.id)
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

        linkToken.value = response.data.link_token;
        ready.value = true; // Enable the button for connecting
        console.log("Fetched Link Token:", linkToken.value); // Log to verify token

    } catch (error) {
        console.error('Error fetching link token:', error);
    }
}

// Plaid configuration
const onSuccess = async (publicToken: string, metadata: unknown) => {
    try {
        // Exchange public token for access token
        const response = await axios.post(`${BASE_URL}/api/exchange_public_token`, {
            public_token: publicToken,
        });

        const accessToken = response.data.access_token;

        // Fetch transactions
        const transactionsResponse = await axios.post(`${BASE_URL}/api/get_transactions`, {
            access_token: accessToken,
        });

        console.log("Transactions:", transactionsResponse.data.transactions);

    } catch (error) {
        console.error("Error fetching transactions:", error);
    }
};


const config = computed(() => ({
    token: linkToken.value,
    onSuccess,
}));

const { open } = usePlaidLink(config);

// Watcher to open Plaid Link modal when linkToken is set
watch(linkToken, (newToken) => {
    if (newToken) {
        open(); // Open the modal when the linkToken is populated
    }
});

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
