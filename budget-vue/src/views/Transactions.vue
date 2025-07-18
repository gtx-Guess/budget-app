<template>
    <div class="transactions flex flex-col">
        <section class="transactions-header flex justify-between items-center">
            <h2 class="text-matcha-400 font-semibold">Transactions</h2>
            <button @click="loadData" class="sync-button bg-matcha-400 text-white rounded-sm cursor-pointer transition-opacity hover-opacity">Summon Transactions</button>
        </section>
        
        <div v-if="accounts?.data?.length" class="content-container">
            <!-- Account Selection -->
            <div class="account-selection-container bg-matcha-light rounded-lg">
                <h3 class="text-matcha-400 font-semibold">Select Account</h3>
                <p class="account-explainer text-matcha-700">
                    Choose an account to summon all transactions. Results are paginated with 25 transactions per page.
                </p>
                <select 
                    v-model="selectedAccountId" 
                    @change="handleAccountChange"
                    class="account-select"
                >
                    <option value="">Select an account...</option>
                    <option 
                        v-for="account in accounts.data" 
                        :key="account.id"
                        :value="account.id"
                    >
                        {{ account["fields"]["Institution"] }} - ${{ account["fields"]["USD"] }}
                    </option>
                </select>
            </div>
            
            <!-- Transactions Display -->
            <div v-if="selectedAccountId" class="transactions-container">
                <div class="transactions-header-info">
                    <h3 class="text-matcha-400 font-semibold">
                        {{ getSelectedAccountName() }} Transactions
                    </h3>
                    <p class="transactions-count text-matcha-700">
                        Showing {{ paginatedTransactions.length }} of {{ filteredTransactions.length }} transactions
                        (Page {{ currentPage }} of {{ totalPages }})
                    </p>
                </div>
                
                <!-- Transaction Cards -->
                <div v-if="paginatedTransactions.length" class="transactions-list">
                    <div 
                        v-for="transaction in paginatedTransactions" 
                        :key="transaction.id"
                        class="transaction-card bg-matcha-light rounded-lg"
                    >
                        <div class="transaction-main-info">
                            <div class="transaction-primary">
                                <div class="transaction-vendor font-semibold text-matcha-400">
                                    {{ transaction.fields.Vendor || transaction.fields.Name }}
                                </div>
                                <div class="transaction-amount font-bold" :class="transaction.fields.USD >= 0 ? 'text-green-600' : 'text-red-600'">
                                    {{ transaction.fields.USD >= 0 ? '+' : '' }}${{ Math.abs(transaction.fields.USD).toFixed(2) }}
                                </div>
                            </div>
                            <div class="transaction-secondary">
                                <div class="transaction-date text-matcha-700">{{ formatDate(transaction.fields.Date) }}</div>
                                <div v-if="transaction.fields.Name && transaction.fields.Name !== transaction.fields.Vendor" 
                                     class="transaction-name text-matcha-600">
                                    {{ transaction.fields.Name }}
                                </div>
                            </div>
                        </div>
                        <div v-if="transaction.fields.Notes" class="transaction-notes text-matcha-600">
                            {{ transaction.fields.Notes }}
                        </div>
                    </div>
                </div>
                
                <!-- No Transactions Message -->
                <div v-else class="no-transactions bg-matcha-light rounded-lg text-center text-matcha-700">
                    No transactions found for this account
                </div>
                
                <!-- Pagination Controls -->
                <div v-if="totalPages > 1" class="pagination-controls">
                    <button 
                        @click="goToPage(currentPage - 1)"
                        :disabled="currentPage <= 1"
                        class="pagination-btn"
                        :class="{ 'disabled': currentPage <= 1 }"
                    >
                        Previous
                    </button>
                    
                    <div class="page-numbers">
                        <button 
                            v-for="page in visiblePageNumbers" 
                            :key="page"
                            @click="goToPage(Number(page))"
                            class="page-number-btn"
                            :class="{ 'active': page === currentPage }"
                        >
                            {{ page }}
                        </button>
                    </div>
                    
                    <button 
                        @click="goToPage(currentPage + 1)"
                        :disabled="currentPage >= totalPages"
                        class="pagination-btn"
                        :class="{ 'disabled': currentPage >= totalPages }"
                    >
                        Next
                    </button>
                </div>
            </div>
            
            <!-- Select Account Prompt -->
            <div v-else class="select-account-prompt bg-matcha-light rounded-lg text-center text-matcha-700">
                Select an account above to summon transactions
            </div>
        </div>
        
        <!-- No Accounts Message -->
        <div v-else class="no-accounts-section bg-matcha-light text-matcha-400 rounded-lg text-center">
            <span>No accounts summoned yet. Click "Summon Transactions" to get started.</span>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import { useLocalStore } from '@/stores/localStorage';
import { storeToRefs } from 'pinia';
import { useRoute } from 'vue-router';
import axios from 'axios';

const localStore = useLocalStore();
const { accounts, transactions } = storeToRefs(localStore);
const { setAccounts, setTransactions } = localStore;
const route = useRoute();

const selectedAccountId = ref<string>('');
const currentPage = ref<number>(1);
const transactionsPerPage = 25;

// Load both accounts and transactions
const loadData = async () => {
    try {
        const [accResponse, tranResponse] = await Promise.all([
            axios.get(`/api/get_local_accounts`),
            axios.get(`/api/get_local_transactions`)
        ]);
        setAccounts({ data: accResponse.data });
        setTransactions({ data: tranResponse.data });
        
        // Auto-select account if accountId query parameter exists
        const accountId = route.query.accountId as string;
        if (accountId && accResponse.data.some((acc: any) => acc.id === accountId)) {
            selectedAccountId.value = accountId;
        }
    } catch (error) {
        console.error("Error fetching data:", error);
    }
};

// Check for accountId query parameter on component mount
onMounted(async () => {
    const accountId = route.query.accountId as string;
    
    // If we have an accountId query parameter, auto-load data
    if (accountId) {
        // If data isn't already loaded, load it first
        if (!accounts.value?.data?.length || !transactions.value?.data?.length) {
            await loadData();
        } else {
            // Data is already loaded, just select the account
            if (accounts.value.data.some((acc: any) => acc.id === accountId)) {
                selectedAccountId.value = accountId;
            }
        }
    }
});

// Handle account selection change
const handleAccountChange = () => {
    currentPage.value = 1; // Reset to first page when account changes
};

// Get selected account name for display
const getSelectedAccountName = () => {
    if (!selectedAccountId.value || !accounts.value?.data) return '';
    const account = accounts.value.data.find(acc => acc.id === selectedAccountId.value);
    return account?.fields?.Institution || '';
};

// Filter transactions by selected account
const filteredTransactions = computed(() => {
    if (!selectedAccountId.value || !transactions.value?.data || !accounts.value?.data) return [];
    
    const selectedAccount = accounts.value.data.find(account => account.id === selectedAccountId.value);
    if (!selectedAccount) return [];
    
    const plaidAccountId = selectedAccount.fields["Plaid Account ID"];
    
    return transactions.value.data
        .filter(transaction => transaction.fields["Account ID"] === plaidAccountId)
        .sort((a, b) => {
            const dateA = new Date(a.fields.Date);
            const dateB = new Date(b.fields.Date);
            return dateB.getTime() - dateA.getTime(); // Newest first
        });
});

// Paginated transactions
const paginatedTransactions = computed(() => {
    const startIndex = (currentPage.value - 1) * transactionsPerPage;
    const endIndex = startIndex + transactionsPerPage;
    return filteredTransactions.value.slice(startIndex, endIndex);
});

// Total pages
const totalPages = computed(() => {
    return Math.ceil(filteredTransactions.value.length / transactionsPerPage);
});

// Visible page numbers for pagination
const visiblePageNumbers = computed(() => {
    const pages = [];
    const total = totalPages.value;
    const current = currentPage.value;
    
    if (total <= 7) {
        // Show all pages if 7 or fewer
        for (let i = 1; i <= total; i++) {
            pages.push(i);
        }
    } else {
        // Always show first page
        pages.push(1);
        
        if (current > 4) {
            pages.push('...');
        }
        
        // Show pages around current page
        const start = Math.max(2, current - 1);
        const end = Math.min(total - 1, current + 1);
        
        for (let i = start; i <= end; i++) {
            if (!pages.includes(i)) {
                pages.push(i);
            }
        }
        
        if (current < total - 3) {
            pages.push('...');
        }
        
        // Always show last page
        if (!pages.includes(total)) {
            pages.push(total);
        }
    }
    
    return pages;
});

// Custom smooth scroll function
const smoothScrollToTop = () => {
    const currentScroll = document.documentElement.scrollTop || document.body.scrollTop;
    if (currentScroll > 1) { // Stop when we're very close to top
        requestAnimationFrame(smoothScrollToTop);
        const scrollStep = Math.max(currentScroll / 8, 1); // Ensure we always move at least 1px
        document.documentElement.scrollTop = currentScroll - scrollStep;
        document.body.scrollTop = currentScroll - scrollStep;
    } else {
        // Make sure we're exactly at the top
        document.documentElement.scrollTop = 0;
        document.body.scrollTop = 0;
    }
};

// Navigate to specific page and scroll to top
const goToPage = (page: number) => {
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page;
        
        // Use setTimeout to ensure DOM has fully updated
        setTimeout(() => {
            smoothScrollToTop();
        }, 50);
    }
};

// Format date for display
const formatDate = (dateStr: string) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
};
</script>

<style scoped>
.transactions-header {
    margin: 20px 0;
}

.transactions-header h2 {
    margin: 0;
    font-size: 38px;
}

.sync-button {
    border: none;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 500;
    color: white !important;
}

.content-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 100%;
}

.account-selection-container {
    padding: 20px;
}

.account-selection-container h3 {
    margin: 0 0 15px 0;
    font-size: 18px;
}

.account-explainer {
    margin: 0 0 15px 0;
    font-size: 14px;
    line-height: 1.4;
}

.account-select {
    width: 100%;
    max-width: 400px;
    padding: 12px;
    border: 2px solid rgb(107 155 79);
    border-radius: 8px;
    background: white;
    color: rgb(107 155 79);
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.account-select:focus {
    outline: none;
    border-color: rgb(107 155 79);
    box-shadow: 0 0 0 3px rgba(107, 155, 79, 0.1);
}

html.dark .account-select {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border-color: rgb(139, 185, 111);
}

html.dark .account-select:focus {
    border-color: rgb(139, 185, 111);
    box-shadow: 0 0 0 3px rgba(139, 185, 111, 0.1);
}

.transactions-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-bottom: 60px;
}

.transactions-header-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
}

.transactions-header-info h3 {
    margin: 0;
    font-size: 20px;
}

.transactions-count {
    font-size: 14px;
}

.transactions-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.transaction-card {
    padding: 20px;
    width: 100%;
    box-sizing: border-box;
    border-left: 4px solid rgb(107 155 79);
}

.transaction-main-info {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 8px;
}

.transaction-primary {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.transaction-vendor {
    font-size: 16px;
    flex: 1;
}

.transaction-amount {
    font-size: 18px;
    white-space: nowrap;
}

.transaction-secondary {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}

.transaction-date {
    font-size: 14px;
}

.transaction-name {
    font-size: 13px;
    text-align: right;
    flex-shrink: 0;
}

.transaction-notes {
    font-size: 12px;
    font-style: italic;
    padding-top: 8px;
    border-top: 1px solid rgba(107, 155, 79, 0.1);
}

.text-green-600 {
    color: #16a34a;
}

.text-red-600 {
    color: #dc2626;
}

.no-transactions,
.select-account-prompt,
.no-accounts-section {
    padding: 40px 20px;
    font-style: italic;
}

/* Pagination Styles */
.pagination-controls {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    margin: 40px 0 60px 0;
    flex-wrap: wrap;
}

.pagination-btn,
.page-number-btn {
    padding: 8px 12px;
    border: 2px solid rgb(107 155 79);
    background: white;
    color: rgb(107 155 79);
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease;
}

.pagination-btn:hover:not(.disabled),
.page-number-btn:hover {
    background: rgb(107 155 79);
    color: white;
}

.pagination-btn.disabled {
    background: #f5f5f5;
    color: #9ca3af;
    border-color: #e5e7eb;
    cursor: not-allowed;
}

.page-number-btn.active {
    background: rgb(107 155 79);
    color: white;
}

.page-numbers {
    display: flex;
    gap: 5px;
    align-items: center;
}

/* Responsive Design */
@media (max-width: 768px) {
    .transactions-header h2 {
        font-size: 32px;
        align-self: center;
    }
    
    .transactions-header {
        flex-direction: column;
        gap: 15px;
        align-items: stretch;
    }
    
    .sync-button {
        padding: 10px 20px;
        font-size: 13px;
    }
    
    .account-selection-container {
        padding: 15px;
    }
    
    .transactions-header-info {
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
    }
    
    .transaction-primary {
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
    }
    
    .transaction-amount {
        align-self: flex-end;
    }
    
    .transaction-secondary {
        flex-direction: column;
        align-items: flex-start;
        gap: 4px;
    }
    
    .transaction-name {
        text-align: left;
    }
    
    .pagination-controls {
        gap: 5px;
    }
    
    .pagination-btn,
    .page-number-btn {
        padding: 6px 10px;
        font-size: 13px;
    }
}

@media (max-width: 480px) {
    .transactions-header h2 {
        font-size: 24px;
    }
    
    .sync-button {
        width: 100%;
        text-align: center;
    }
    
    .account-selection-container {
        padding: 12px;
    }
    
    .transaction-card {
        padding: 12px;
    }
    
    .account-select {
        max-width: 100%;
    }
    
    .page-numbers {
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .transactions-header-info h3 {
        font-size: 18px;
    }
}

/* Enable smooth scrolling globally */
html {
    scroll-behavior: smooth;
}
</style>