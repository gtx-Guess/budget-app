import { ref, computed, watch } from 'vue';
import { usePlaidLink } from '@jcss/vue-plaid-link';
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_BACKEND_URL;

const linkToken = ref('');
const ready = ref(false); // Default to not ready

const config = computed(() => ({
    token: linkToken.value,
    onSuccess: async (publicToken: string) => {
        try {
            console.log(`Making request to: ${`${BASE_URL}/api/exchange_public_token`}`)
            const response = await axios.post(`${BASE_URL}/api/exchange_public_token`, {
                public_token: publicToken,
            });
            const accessToken = response.data.access_token;

            const transactionsResponse = await axios.post(`${BASE_URL}/api/get_transactions`, {
                access_token: accessToken,
                start_date: '2024-12-01',
                end_date: '2024-12-02'
            });

            console.log("Transactions:", transactionsResponse.data.transactions);
        } catch (error) {
            console.error("Error fetching transactions:", error);
        }
    },
    onExit: (error: any) => {
        if (error) {
            console.error("Plaid Link exited with an error:", error);
        } else {
            console.log("Plaid Link exited gracefully");
        }
    },
}));

// Initialize Plaid Link with the computed config
const { open } = usePlaidLink(config);

function setLinkToken(token: string) {
    linkToken.value = token;
    ready.value = true; // Set ready to true when token is available
}

function openPlaidLink() {
    if (ready.value) {
        open(); // Open Plaid Link if ready
    } else {
        console.error("Plaid Link is not ready yet");
    }
}

// Debugging: Watch config for changes
watch(config, (newConfig) => {
    console.log("Plaid config updated:", newConfig);
});

export function usePlaidLinkComposable() {
    return { linkToken, ready, setLinkToken, openPlaidLink };
}
