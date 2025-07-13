<template>
    <div class="home">
        <div class="dashboard-header">
            <h2>Dashboard</h2>
            <button @click="buttonClicked" class="sync-button">Sync Accounts</button>
        </div>
        
        <div v-if="accounts?.data?.length" class="accounts-grid">
            <section v-for="account in accounts.data" :key="account.id" class="account-section">
                <div class="account-info">
                    <div class="account-name">{{ account["fields"]["Institution"] }}</div>
                    <div class="account-details">
                        <span class="account-balance">${{ account["fields"]["USD"] }}</span>
                        <span class="account-updated">{{ account["fields"]["Last Successful Update"] }}</span>
                    </div>
                </div>
            </section>
        </div>
        <div v-else>
            <div class="no-accounts-section">
                <span>No accounts loaded yet</span>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { useLocalStore } from '@/stores/localStorage';
import { storeToRefs } from 'pinia';
import axios from 'axios';
axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL;

const localStore = useLocalStore();
const { accounts } = storeToRefs(localStore);
const { setAccounts } = localStore;

const buttonClicked = async () => {
    try {
        const response = await axios.get(`/api/get_local_accounts`);
        setAccounts({ data: response.data });
    } catch (error) {
        console.error("Error fetching accounts:", error);
    };
};
</script>

<style scoped>
.home {
    display: flex;
    flex-direction: column;
}

.dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.accounts-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

.dashboard-header h2 {
    color: rgb(107 155 79);
    margin: 0;
    font-size: 24px;
    font-weight: 600;
}

.account-section {
    background: rgb(225 233 219);
    color: rgb(107 155 79);
    padding: 20px;
    border-radius: 12px;
}

.account-info {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.account-name {
    font-size: 18px;
    font-weight: bold;
    color: rgb(107 155 79);
}

.account-details {
    display: flex;
    gap: 30px;
    font-size: 14px;
}

.account-balance {
    font-weight: 600;
}

.account-updated {
    color: rgba(107, 155, 79, 0.7);
}

.no-accounts-section {
    background: rgb(225 233 219);
    color: rgb(107 155 79);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}

.sync-button {
    background: rgb(107 155 79);
    color: rgb(248 250 247);
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: opacity 0.2s ease;
}

.sync-button:hover {
    opacity: 0.8;
}
</style>