<template>
    <div class="home">
        <div v-if="accounts?.data?.length">
            <table>
                <thead>
                    <tr>
                        <th>Account Type</th>
                        <th>Balance</th>
                        <th>Last Updated</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="account in accounts.data">
                        <td>{{ account["fields"]["Institution"] }}</td>
                        <td>${{ account["fields"]["USD"] }}</td>
                        <td>{{ account["fields"]["Last Successful Update"] }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else>
            No accounts loaded yet (length: {{ accounts?.data?.length }})
        </div>
    </div>
    <button @click="buttonClicked">Click this button</button>
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

<style scoped lang="scss">
</style>