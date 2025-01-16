<template>
    <div>
        <div v-if="transactions?.data?.length">
            <table class="table-of-transactions">
                <thead>
                    <tr>
                        <th style="width: 400px;">Transaction Name</th>
                        <th style="width: 70px;">Amount</th>
                        <th>Date</th>
                        <th>Vendor</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="transaction in sortedTransactions" :key="transaction.id">
                        <td>{{ transaction["fields"]["Name"] }}</td>
                        <td style="text-align: right; position: relative;">
                            <span style="position: absolute; left: 8px;">$</span>
                            <span>{{ transaction["fields"]["USD"] }}</span>
                        </td>
                        <td style="text-align: center;">{{ transaction["fields"]["Date"] }}</td>
                        <td style="text-align: center;">{{ transaction["fields"]["Vendor"] }}</td>
                        <td style="text-align: center;">{{ transaction["fields"]["Notes"] }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else>
            No transactions loaded yet (length: {{ transactions?.data?.length }})
        </div>
    </div>
    <button @click="buttonClicked">Click this button</button>
</template>

<script lang="ts" setup>
import { useLocalStore } from '@/stores/localStorage';
import { storeToRefs } from 'pinia';
import { computed } from 'vue';
import axios from 'axios';
const BASE_URL = import.meta.env.VITE_BACKEND_URL;

const localStore = useLocalStore();
const { transactions } = storeToRefs(localStore);
const { setTransactions } = localStore;

const buttonClicked = async () => {
    try {
        const response = await axios.get(`${BASE_URL}/api/get_airtable_data/transactions`);
        setTransactions({ data: response.data });
    } catch (error) {
        console.error("Error fetching transactions:", error);
    }
}

const sortedTransactions = computed(() => {
  return [...transactions.value.data].sort((a, b) => {
    const dateA = new Date(a.fields.Date);
    const dateB = new Date(b.fields.Date);
    return dateB.getTime() - dateA.getTime()  // Descending (newest first)
  })
})

</script>

<style scoped>


.table-of-transactions thead {
    text-align: center;
}

</style>