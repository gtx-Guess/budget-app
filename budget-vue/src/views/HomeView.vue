<template>
    <div class="home flex flex-col">
        <section class="dashboard-header flex justify-between items-center">
            <h2 class="text-matcha-400 font-semibold">Dashboard</h2>
            <button @click="buttonClicked" class="sync-button bg-matcha-400 text-white rounded-sm cursor-pointer transition-opacity hover-opacity">Sync Accounts</button>
        </section>
        <section class="dashboard-views-section">
            <div class="dashboard-views-controller flex flex-row justify-around bg-matcha-gray text-matcha-400 rounded-md">
                <div 
                    @click="setActiveTab('Overview')" 
                    :class="{ 'active-controller': activeTab === 'Overview' }"
                >
                    Overview
                </div>
                <div 
                    @click="setActiveTab('Quick Analysis')" 
                    :class="{ 'active-controller': activeTab === 'Quick Analysis' }"
                >
                    Quick Analysis
                </div>
                <div 
                    @click="setActiveTab('Recent Activity *')" 
                    :class="{ 'active-controller': activeTab === 'Recent Activity *' }"
                >
                    Recent Activity *
                </div>
            </div>
        </section>
        <div v-if="accounts?.data?.length" class="content-container">
            <!-- Overview -->
            <div v-if="activeTab === 'Overview'" class="accounts-grid">
                <section v-for="account in accounts.data" :key="account.id" class="account-section bg-matcha-light text-matcha-400 rounded-lg">
                <div class="account-info flex flex-col">
                    <div class="account-name font-bold text-matcha-400">{{ account["fields"]["Institution"] }}</div>
                    <div class="account-details flex">
                        <span class="account-balance font-semibold">${{ account["fields"]["USD"] }}</span>
                        <span class="account-updated text-matcha-700">{{ account["fields"]["Last Successful Update"] }}</span>
                    </div>
                </div>
                </section>
            </div>
            <!-- Quick Analysis -->
            <div v-if="activeTab === 'Quick Analysis'" class="analysis-container">
                <div class="analysis-grid">
                    <div class="account-picker bg-matcha-light rounded-lg">
                        <h3 class="text-matcha-400 font-semibold">Pick your account</h3>
                        <p class="account-explainer text-matcha-700">
                            Pick an account from the dropdown to see the last 5 transactions for that specific account.
                        </p>
                        <select 
                            v-model="selectedAccountId" 
                            @change="setSelectedAccount(selectedAccountId)"
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
                        
                        <!-- Quick Analysis Charts -->
                        <div v-if="selectedAccountId" class="quick-analysis-charts">
                            <div class="analysis-card">
                                <h4 class="text-matcha-400 font-medium">{{ getPreviousMonthName() }} Summary</h4>
                                <div class="stat-row">
                                    <span class="stat-label text-matcha-700">Total Spent:</span>
                                    <span class="stat-value font-semibold text-red-600">${{ getPreviousMonthSpending().toFixed(2) }}</span>
                                </div>
                                <div class="stat-row">
                                    <span class="stat-label text-matcha-700">Total Income:</span>
                                    <span class="stat-value font-semibold text-green-600">${{ getPreviousMonthIncome().toFixed(2) }}</span>
                                </div>
                                <div class="stat-row">
                                    <span class="stat-label text-matcha-700">Net Change:</span>
                                    <span class="stat-value font-semibold" :class="getPreviousMonthNetChange() >= 0 ? 'text-green-600' : 'text-red-600'">
                                        {{ getPreviousMonthNetChange() >= 0 ? '+' : '' }}${{ getPreviousMonthNetChange().toFixed(2) }}
                                    </span>
                                </div>
                            </div>
                            
                            <div class="analysis-card">
                                <h4 class="text-matcha-400 font-medium">Activity Breakdown</h4>
                                <div class="stat-row">
                                    <span class="stat-label text-matcha-700">{{ getPreviousMonthName() }}:</span>
                                    <span class="stat-value font-semibold text-matcha-400">{{ getPreviousMonthTransactionCount() }} transactions</span>
                                </div>
                                <div class="stat-row">
                                    <span class="stat-label text-matcha-700">Average per day:</span>
                                    <span class="stat-value font-semibold text-matcha-400">${{ getPreviousMonthAverageDaily().toFixed(2) }}</span>
                                </div>
                                <div class="stat-row">
                                    <span class="stat-label text-matcha-700">Largest expense:</span>
                                    <span class="stat-value font-semibold text-red-600">${{ getPreviousMonthLargestExpense().toFixed(2) }}</span>
                                </div>
                            </div>
                        </div>
                        
                        <div v-else class="select-account-hint text-matcha-700 text-center">
                            Select an account above to see quick analysis insights
                        </div>
                    </div>
                    
                    <div class="transactions-display bg-matcha-light rounded-lg">
                        <h3 class="text-matcha-400 font-semibold">Recent Transactions</h3>
                        <div v-if="selectedAccountId && getRecentTransactions().length" class="transactions-list">
                            <div 
                                v-for="transaction in getRecentTransactions()" 
                                :key="transaction.id"
                                class="transaction-item"
                            >
                                <div class="transaction-info">
                                    <div class="transaction-vendor font-medium text-matcha-400">{{ transaction.fields.Vendor || transaction.fields.Name }}</div>
                                    <div class="transaction-date text-matcha-700">{{ transaction.fields.Date }}</div>
                                    <div v-if="transaction.fields.Notes" class="transaction-notes text-matcha-600">{{ transaction.fields.Notes }}</div>
                                </div>
                                <div class="transaction-amount font-semibold" :class="transaction.fields.USD >= 0 ? 'text-green-600' : 'text-red-600'">
                                    ${{ Math.abs(transaction.fields.USD).toFixed(2) }}
                                </div>
                            </div>
                        </div>
                        <div v-else-if="selectedAccountId && !getRecentTransactions().length" class="no-transactions text-matcha-700 text-center">
                            No recent transactions found for this account
                        </div>
                        <div v-else class="select-account-prompt text-matcha-700 text-center">
                            Select an account to view recent transactions
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Recent Activity -->
            <div v-if="activeTab === 'Recent Activity *'" class="recent-activity-container">
                <div class="recent-activity-content bg-matcha-light rounded-lg">
                    <h3 class="text-matcha-400 font-semibold">Recent Activity</h3>
                    <p class="activity-explainer text-matcha-700">
                        Here are the last 5 transactions across all your accounts.
                    </p>
                    <div v-if="getAllRecentTransactions().length" class="transactions-list">
                        <div 
                            v-for="transaction in getAllRecentTransactions()" 
                            :key="transaction.id"
                            class="transaction-item"
                        >
                            <div class="transaction-info">
                                <div class="transaction-vendor font-medium text-matcha-400">{{ transaction.fields.Vendor || transaction.fields.Name }}</div>
                                <div class="transaction-date text-matcha-700">{{ transaction.fields.Date }}</div>
                                <div v-if="transaction.fields.Notes" class="transaction-notes text-matcha-600">{{ transaction.fields.Notes }}</div>
                            </div>
                            <div class="transaction-amount font-semibold" :class="transaction.fields.USD >= 0 ? 'text-green-600' : 'text-red-600'">
                                ${{ Math.abs(transaction.fields.USD).toFixed(2) }}
                            </div>
                        </div>
                    </div>
                    <div v-else class="no-transactions text-matcha-700 text-center">
                        No recent transactions available. Click "Sync Accounts" to load data.
                    </div>
                </div>
            </div>
        </div>
        <div v-else>
            <div class="no-accounts-section bg-matcha-light text-matcha-400 rounded-lg text-center">
                <span>No accounts loaded yet</span>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useLocalStore } from '@/stores/localStorage';
import { storeToRefs } from 'pinia';
import axios from 'axios';
axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL;

const localStore = useLocalStore();
const { accounts, transactions } = storeToRefs(localStore);
const { setAccounts, setTransactions } = localStore;

const activeTab = ref('Overview');
const selectedAccountId = ref<string>('');

const setActiveTab = (tabName: string) => {
    activeTab.value = tabName;
};

const setSelectedAccount = (accountId: string) => {
    selectedAccountId.value = accountId;
};

// Get recent transactions for selected account (last 5, newest first)
const getRecentTransactions = () => {
    if (!selectedAccountId.value || !transactions.value?.data || !accounts.value?.data) return [];
    
    // Find the selected account to get its Plaid Account ID
    const selectedAccount = accounts.value.data.find(account => account.id === selectedAccountId.value);
    if (!selectedAccount) return [];
    
    const plaidAccountId = selectedAccount.fields["Plaid Account ID"];
    
    // Filter transactions by matching account ID
    const filtered = transactions.value.data
        .filter(transaction => {
            return transaction.fields["Account ID"] === plaidAccountId;
        });
    
    // Sort by date (newest first) and take first 5
    return filtered
        .sort((a, b) => {
            const dateA = new Date(a.fields.Date);
            const dateB = new Date(b.fields.Date);
            return dateB.getTime() - dateA.getTime(); // Newest first
        })
        .slice(0, 5); // Take first 5 (newest)
};

// Get previous month name for display
const getPreviousMonthName = () => {
    const now = new Date();
    const previousMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1);
    return previousMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
};

// Get previous month spending for selected account
const getPreviousMonthSpending = () => {
    const previousMonthTransactions = getPreviousMonthTransactions();
    return previousMonthTransactions
        .filter(t => t.fields.USD < 0)
        .reduce((sum, t) => sum + Math.abs(t.fields.USD), 0);
};

// Get previous month income for selected account  
const getPreviousMonthIncome = () => {
    const previousMonthTransactions = getPreviousMonthTransactions();
    return previousMonthTransactions
        .filter(t => t.fields.USD > 0)
        .reduce((sum, t) => sum + t.fields.USD, 0);
};

// Get net change for previous month
const getPreviousMonthNetChange = () => {
    return getPreviousMonthIncome() - getPreviousMonthSpending();
};

// Get transaction count for previous month
const getPreviousMonthTransactionCount = () => {
    return getPreviousMonthTransactions().length;
};

// Get average daily spending for previous month
const getPreviousMonthAverageDaily = () => {
    const spending = getPreviousMonthSpending();
    const now = new Date();
    const previousMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1);
    const daysInPreviousMonth = new Date(previousMonth.getFullYear(), previousMonth.getMonth() + 1, 0).getDate();
    return spending / daysInPreviousMonth;
};

// Get largest expense in previous month
const getPreviousMonthLargestExpense = () => {
    const previousMonthTransactions = getPreviousMonthTransactions();
    const expenses = previousMonthTransactions.filter(t => t.fields.USD < 0);
    if (expenses.length === 0) return 0;
    return Math.max(...expenses.map(t => Math.abs(t.fields.USD)));
};

// Helper: Get all transactions for previous month for selected account
const getPreviousMonthTransactions = () => {
    if (!selectedAccountId.value || !transactions.value?.data || !accounts.value?.data) return [];
    
    const selectedAccount = accounts.value.data.find(account => account.id === selectedAccountId.value);
    if (!selectedAccount) return [];
    
    const plaidAccountId = selectedAccount.fields["Plaid Account ID"];
    const now = new Date();
    const previousMonth = now.getMonth() - 1;
    const previousYear = previousMonth < 0 ? now.getFullYear() - 1 : now.getFullYear();
    const adjustedMonth = previousMonth < 0 ? 11 : previousMonth;
    
    return transactions.value.data
        .filter(transaction => {
            const transactionDate = new Date(transaction.fields.Date);
            return transaction.fields["Account ID"] === plaidAccountId &&
                   transactionDate.getMonth() === adjustedMonth &&
                   transactionDate.getFullYear() === previousYear;
        });
};

// Get recent transactions across all accounts (last 5, newest first)
const getAllRecentTransactions = () => {
    if (!transactions.value?.data) return [];
    
    // Sort all transactions by date (newest first) and take first 5
    return transactions.value.data
        .sort((a, b) => {
            const dateA = new Date(a.fields.Date);
            const dateB = new Date(b.fields.Date);
            return dateB.getTime() - dateA.getTime(); // Newest first
        })
        .slice(0, 5); // Take first 5 (newest)
};

const buttonClicked = async () => {
    try {
        const accResponse = await axios.get(`/api/get_local_accounts`);
        setAccounts({ data: accResponse.data });
        const tranResponse = await axios.get(`/api/get_local_transactions`);
        setTransactions({ data: tranResponse.data });
    } catch (error) {
        console.error("Error fetching accounts:", error);
    };
};
</script>

<style scoped>

.dashboard-views-section {
    width: 100%;
    margin-bottom: 15px;
}

.dashboard-views-controller {
    display: flex;
    flex-direction: row;
    width: fit-content;
    min-width: 300px;
    max-width: 80%;
    justify-content: space-around;
    background: rgb(239, 239, 239);
    color: rgb(107 155 79);
    border-radius: 10px;
}

.dashboard-views-controller > * {
    padding: 15px 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    border-radius: 8px;
    white-space: nowrap;
    flex-shrink: 0;
    text-align: center;
}

.active-controller {
    background: rgb(107 155 79) !important;
    color: white !important;
}

.dashboard-header {
    margin: 20px 0;
}

.dashboard-header h2 {
    margin: 0;
    font-size: 38px;
}

.accounts-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

.full-width-container {
    width: 100%;
}

.full-width-container .accounts-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

.account-section {
    padding: 20px;
}

.account-info {
    gap: 8px;
}

.account-name {
    font-size: 24px;
}

.account-details {
    gap: 30px;
    font-size: 16px;
}



.no-accounts-section {
    padding: 20px;
}

.sync-button {
    border: none;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 500;
}


/* Responsive Design for Dashboard Views Controller */
@media (max-width: 1024px) {
    .dashboard-views-controller {
        max-width: 90%;
        min-width: 280px;
    }
}

@media (max-width: 768px) {
    .dashboard-views-controller {
        max-width: 95%;
        min-width: 250px;
    }
    
    .dashboard-views-controller > * {
        padding: 12px 15px;
        font-size: 15px;
    }
}

/* Analysis Section Styles */
.analysis-container {
    width: 100%;
}

.analysis-grid {
    display: grid;
    grid-template-columns: 30% 70%;
    gap: 20px;
    width: 100%;
}

.account-picker,
.transactions-display {
    padding: 20px;
}

.account-picker h3,
.transactions-display h3,
.recent-activity-content h3 {
    margin: 0 0 15px 0;
    font-size: 18px;
}

.account-explainer,
.activity-explainer {
    margin: 0 0 15px 0;
    font-size: 14px;
    line-height: 1.4;
}

.recent-activity-container {
    width: 100%;
}

.recent-activity-content {
    padding: 20px;
}

.quick-analysis-charts {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.analysis-card {
    background: white;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid rgb(107 155 79);
    transition: background-color 0.3s ease, border-color 0.3s ease;
}

/* Dark mode for analysis cards */
html.dark .analysis-card {
    background-color: var(--bg-secondary) !important;
    border-left-color: rgb(139, 185, 111);
}

.analysis-card h4 {
    margin: 0 0 12px 0;
    font-size: 16px;
}

.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.stat-row:last-child {
    margin-bottom: 0;
}

.stat-label {
    font-size: 14px;
}

.stat-value {
    font-size: 14px;
}

.select-account-hint {
    margin-top: 40px;
    padding: 20px;
    font-style: italic;
}

.account-select {
    width: 100%;
    padding: 12px;
    border: 2px solid rgb(107 155 79);
    border-radius: 8px;
    background: white;
    color: rgb(107 155 79);
    font-size: 14px;
    cursor: pointer;
}

.account-select:focus {
    outline: none;
    border-color: rgb(107 155 79);
    box-shadow: 0 0 0 3px rgba(107, 155, 79, 0.1);
}

.transactions-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.transaction-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    background: white;
    border-radius: 8px;
    border-left: 4px solid rgb(107 155 79);
    transition: background-color 0.3s ease, border-color 0.3s ease;
}

/* Dark mode for transaction items */
html.dark .transaction-item {
    background-color: var(--bg-secondary) !important;
    border-left-color: rgb(139, 185, 111);
}

.transaction-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.transaction-vendor {
    font-size: 14px;
}

.transaction-date {
    font-size: 12px;
}

.transaction-notes {
    font-size: 11px;
    font-style: italic;
}

.transaction-amount {
    font-size: 16px;
}

.text-green-600 {
    color: #16a34a;
}

.text-red-600 {
    color: #dc2626;
}

.no-transactions,
.select-account-prompt {
    padding: 40px 20px;
    font-style: italic;
}

@media (max-width: 768px) {
    .analysis-grid {
        grid-template-columns: 1fr;
        gap: 15px;
    }
}

@media (max-width: 600px) {
    .dashboard-views-controller {
        max-width: 98%;
        min-width: 200px;
    }
    
    .dashboard-views-controller > * {
        padding: 10px 12px;
    }
    
    .accounts-grid {
        grid-template-columns: 1fr;
    }
}
</style>