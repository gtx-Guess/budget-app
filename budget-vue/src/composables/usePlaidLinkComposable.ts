import { ref, computed } from 'vue';
import { usePlaidLink } from '@jcss/vue-plaid-link';
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_BACKEND_URL;

const linkToken = ref('');
const ready = ref(true);

const config = computed(() => ({
    token: linkToken.value,
    onSuccess: async (publicToken: string) => {
        try {
            const response = await axios.post(`${BASE_URL}/api/exchange_public_token`, {
                public_token: publicToken,
            });

            const accessToken = response.data.access_token;

            const transactionsResponse = await axios.post(`${BASE_URL}/api/get_transactions`, {
                access_token: accessToken,
            });

            console.log("Transactions:", transactionsResponse.data.transactions);
        } catch (error) {
            console.error("Error fetching transactions:", error);
        }
    },
}));

const { open } = usePlaidLink(config);

function setLinkToken(token: string) {
    linkToken.value = token;
    ready.value = false; // Ready to open the modal
}

function openPlaidLink() {
    if (!ready.value) open();
}

export function usePlaidLinkComposable() {
    return { linkToken, ready, setLinkToken, openPlaidLink };
}
