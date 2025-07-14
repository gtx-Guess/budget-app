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
                            @change="setSelectedAccountId(selectedAccountId)"
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
                            <div v-if="isLoadingMetrics" class="loading-state">
                                <div class="loading-spinner"></div>
                                <span class="text-matcha-700">Calculating metrics...</span>
                            </div>
                            <template v-else>
                                <div class="analysis-card">
                                    <h4 class="text-matcha-400 font-medium flex items-center gap-2">
                                        <span class="chart-icon">📊</span>
                                        {{ getPreviousMonthName() }} Summary
                                    </h4>
                                    <div class="stat-row">
                                        <span class="stat-label text-matcha-700">💸 Total Spent:</span>
                                        <div class="stat-value-container">
                                            <span class="stat-value font-semibold text-red-600">${{ getPreviousMonthSpending().toFixed(2) }}</span>
                                            <div class="progress-bar">
                                                <div class="progress-fill expense" :style="{ width: getSpendingPercentage() + '%' }"></div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="stat-row">
                                        <span class="stat-label text-matcha-700">💰 Total Income:</span>
                                        <div class="stat-value-container">
                                            <span class="stat-value font-semibold text-green-600">${{ getPreviousMonthIncome().toFixed(2) }}</span>
                                            <div class="progress-bar">
                                                <div class="progress-fill income" :style="{ width: getIncomePercentage() + '%' }"></div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="stat-row">
                                        <span class="stat-label text-matcha-700">📈 Net Change:</span>
                                        <span class="stat-value font-semibold" :class="getPreviousMonthNetChange() >= 0 ? 'text-green-600' : 'text-red-600'">
                                            {{ getPreviousMonthNetChange() >= 0 ? '+' : '' }}${{ getPreviousMonthNetChange().toFixed(2) }}
                                        </span>
                                    </div>
                                </div>
                                
                                <div class="analysis-card">
                                    <h4 class="text-matcha-400 font-medium flex items-center gap-2">
                                        <span class="chart-icon">🔍</span>
                                        Activity Breakdown
                                    </h4>
                                    <div class="stat-row">
                                        <span class="stat-label text-matcha-700">📅 {{ getPreviousMonthName() }}:</span>
                                        <span class="stat-value font-semibold text-matcha-400">{{ getPreviousMonthTransactionCount() }} transactions</span>
                                    </div>
                                    <div class="stat-row">
                                        <span class="stat-label text-matcha-700">📊 Average per day:</span>
                                        <span class="stat-value font-semibold text-matcha-400">${{ getPreviousMonthAverageDaily().toFixed(2) }}</span>
                                    </div>
                                    <div class="stat-row">
                                        <span class="stat-label text-matcha-700">🔥 Largest expense:</span>
                                        <span class="stat-value font-semibold text-red-600">${{ getPreviousMonthLargestExpense().toFixed(2) }}</span>
                                    </div>
                                    <div class="stat-row">
                                        <span class="stat-label text-matcha-700">🏪 Most frequent vendor:</span>
                                        <span class="stat-value font-semibold text-matcha-400">{{ getMostFrequentVendor() }}</span>
                                    </div>
                                </div>
                                
                                <div class="analysis-card">
                                    <h4 class="text-matcha-400 font-medium flex items-center gap-2">
                                        <span class="chart-icon">📈</span>
                                        Spending Trends
                                    </h4>
                                    <div class="stat-row">
                                        <span class="stat-label text-matcha-700">📊 {{ getTwoMonthsAgoName() }} vs {{ getPreviousMonthName() }}:</span>
                                        <span class="stat-value font-semibold" :class="getSpendingTrend() >= 0 ? 'text-red-600' : 'text-green-600'">
                                            {{ getSpendingTrend() >= 0 ? '+' : '' }}{{ getSpendingTrend().toFixed(1) }}%
                                        </span>
                                    </div>
                                    <div class="stat-row">
                                        <span class="stat-label text-matcha-700">💳 Transaction frequency:</span>
                                        <span class="stat-value font-semibold" :class="getTransactionTrend() >= 0 ? 'text-matcha-400' : 'text-red-600'">
                                            {{ getTransactionTrend() >= 0 ? '+' : '' }}{{ getTransactionTrend().toFixed(1) }}%
                                        </span>
                                    </div>
                                </div>
                            </template>
                        </div>
                        
                        <div v-else class="select-account-hint text-matcha-700 text-center">
                            Select an account above to see quick analysis insights
                        </div>
                    </div>
                    
                    <div class="transactions-display bg-matcha-light rounded-lg">
                        <h3 class="text-matcha-400 font-semibold">5 Recent Transactions for {{ selectedAccount || "N/A" }}</h3>
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
import { ref, watch } from 'vue';
import { useLocalStore } from '@/stores/localStorage';
import { storeToRefs } from 'pinia';
import axios from 'axios';
axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL;

const localStore = useLocalStore();
const { accounts, transactions } = storeToRefs(localStore);
const { setAccounts, setTransactions } = localStore;

const activeTab = ref('Overview');
const selectedAccountId = ref<string>('');
const selectedAccount = ref<string>('');
const isLoadingMetrics = ref(false);

const setActiveTab = (tabName: string) => {
    activeTab.value = tabName;
};

const setSelectedAccountId = (accountId: string) => {
    selectedAccountId.value = accountId;
    if (accountId) {
        isLoadingMetrics.value = true;
        // Simulate brief loading time for UX
        setTimeout(() => {
            isLoadingMetrics.value = false;
        }, 500);
    }
};

const setSelectedAccount = (account: string) => {
    selectedAccount.value = account;
};

// Get recent transactions for selected account (last 5, newest first)
const getRecentTransactions = () => {
    if (!selectedAccountId.value || !transactions.value?.data || !accounts.value?.data) return [];
    
    // Find the selected account to get its Plaid Account ID
    const selectedAccount = accounts.value.data.find(account => account.id === selectedAccountId.value);
    if (!selectedAccount) return [];
    setSelectedAccount(selectedAccount.fields["Institution"]);
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

// Get previous month name for display (1 month ago)
const getPreviousMonthName = () => {
    const now = new Date();
    const previousMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1);
    return previousMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
};

// Get two months ago name for comparison
const getTwoMonthsAgoName = () => {
    const now = new Date();
    const twoMonthsAgo = new Date(now.getFullYear(), now.getMonth() - 2, 1);
    return twoMonthsAgo.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
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
    const previousMonth = new Date(now.getFullYear(), now.getMonth() - 1, 1); // 1 month ago
    const daysInPreviousMonth = new Date(previousMonth.getFullYear(), previousMonth.getMonth() + 1, 0).getDate();
    return spending / daysInPreviousMonth;
};

// Get most frequent vendor from previous month
const getMostFrequentVendor = () => {
    const previousMonthTransactions = getPreviousMonthTransactions();
    if (previousMonthTransactions.length === 0) return 'N/A';
    
    const vendorCounts: Record<string, number> = {};
    previousMonthTransactions.forEach(transaction => {
        const vendor = transaction.fields.Vendor || transaction.fields.Name || 'Unknown';
        vendorCounts[vendor] = (vendorCounts[vendor] || 0) + 1;
    });
    
    const mostFrequent = Object.entries(vendorCounts)
        .sort(([,a], [,b]) => b - a)[0];
    
    return mostFrequent ? mostFrequent[0] : 'N/A';
};

// Get spending trend percentage (comparing two months ago to previous month)
const getSpendingTrend = () => {
    const twoMonthsAgoTransactions = getTwoMonthsAgoTransactions();
    const previousMonthTransactions = getPreviousMonthTransactions();
    
    const twoMonthsAgoSpending = twoMonthsAgoTransactions
        .filter(t => t.fields.USD < 0)
        .reduce((sum, t) => sum + Math.abs(t.fields.USD), 0);
    
    const previousMonthSpending = previousMonthTransactions
        .filter(t => t.fields.USD < 0)
        .reduce((sum, t) => sum + Math.abs(t.fields.USD), 0);
    
    if (twoMonthsAgoSpending === 0) return 0;
    
    return ((previousMonthSpending - twoMonthsAgoSpending) / twoMonthsAgoSpending) * 100;
};

// Get transaction frequency trend
const getTransactionTrend = () => {
    const twoMonthsAgoCount = getTwoMonthsAgoTransactions().length;
    const previousMonthCount = getPreviousMonthTransactions().length;
    
    if (twoMonthsAgoCount === 0) return 0;
    
    return ((previousMonthCount - twoMonthsAgoCount) / twoMonthsAgoCount) * 100;
};

// Get spending percentage for progress bar
const getSpendingPercentage = () => {
    const spending = getPreviousMonthSpending();
    const income = getPreviousMonthIncome();
    const total = spending + income;
    return total > 0 ? (spending / total) * 100 : 0;
};

// Get income percentage for progress bar
const getIncomePercentage = () => {
    const spending = getPreviousMonthSpending();
    const income = getPreviousMonthIncome();
    const total = spending + income;
    return total > 0 ? (income / total) * 100 : 0;
};

// Get largest expense in previous month
const getPreviousMonthLargestExpense = () => {
    const previousMonthTransactions = getPreviousMonthTransactions();
    const expenses = previousMonthTransactions.filter(t => t.fields.USD < 0);
    if (expenses.length === 0) return 0;
    return Math.max(...expenses.map(t => Math.abs(t.fields.USD)));
};

// Helper: Get all transactions for previous month for selected account (1 month ago)
const getPreviousMonthTransactions = () => {
    if (!selectedAccountId.value || !transactions.value?.data || !accounts.value?.data) return [];
    
    const selectedAccount = accounts.value.data.find(account => account.id === selectedAccountId.value);
    if (!selectedAccount) return [];
    
    const plaidAccountId = selectedAccount.fields["Plaid Account ID"];
    const now = new Date();
    const previousMonth = now.getMonth() - 1; // 1 month ago
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

// Helper: Get all transactions for two months ago for comparison
const getTwoMonthsAgoTransactions = () => {
    if (!selectedAccountId.value || !transactions.value?.data || !accounts.value?.data) return [];
    
    const selectedAccount = accounts.value.data.find(account => account.id === selectedAccountId.value);
    if (!selectedAccount) return [];
    
    const plaidAccountId = selectedAccount.fields["Plaid Account ID"];
    const now = new Date();
    const twoMonthsAgo = now.getMonth() - 2; // 2 months ago
    const twoMonthsAgoYear = twoMonthsAgo < 0 ? now.getFullYear() - 1 : now.getFullYear();
    const adjustedMonth = twoMonthsAgo < 0 ? 12 + twoMonthsAgo : twoMonthsAgo;
    
    return transactions.value.data
        .filter(transaction => {
            const transactionDate = new Date(transaction.fields.Date);
            return transaction.fields["Account ID"] === plaidAccountId &&
                   transactionDate.getMonth() === adjustedMonth &&
                   transactionDate.getFullYear() === twoMonthsAgoYear;
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

/* Loading State Styles */
.loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
    gap: 15px;
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(107, 155, 79, 0.3);
    border-top: 3px solid rgb(107, 155, 79);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

html.dark .loading-spinner {
    border: 3px solid rgba(139, 185, 111, 0.3);
    border-top: 3px solid rgb(139, 185, 111);
}

/* Progress Bar Styles */
.stat-value-container {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 4px;
}

.progress-bar {
    width: 80px;
    height: 4px;
    background-color: rgba(107, 155, 79, 0.2);
    border-radius: 2px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.3s ease;
}

.progress-fill.expense {
    background-color: #dc2626;
}

.progress-fill.income {
    background-color: #16a34a;
}

html.dark .progress-bar {
    background-color: rgba(139, 185, 111, 0.2);
}

/* Icon Styles */
.chart-icon {
    font-size: 16px;
}

.flex {
    display: flex;
}

.items-center {
    align-items: center;
}

.gap-2 {
    gap: 8px;
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