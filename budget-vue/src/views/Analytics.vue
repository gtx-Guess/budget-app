<template>
  <div class="analytics-container">
    <div class="analytics-header">
      <h1>Budget Analytics</h1>
      <p class="subtitle">Insights into your spending patterns and financial trends</p>
    </div>

    <div class="charts-grid">
      <!-- Spending by Vendor Chart -->
      <div class="chart-card">
        <SpendingByVendorChart />
      </div>

      <!-- Monthly Trends Chart -->
      <div class="chart-card">
        <MonthlySpendingTrendsChart />
      </div>

      <!-- Income vs Expenses Chart -->
      <div class="chart-card">
        <IncomeVsExpensesChart />
      </div>
    </div>

    <!-- Summary Stats -->
    <div class="summary-stats" v-if="summaryStats">
      <div class="stat-card">
        <h3>Total Transactions</h3>
        <p class="stat-value">{{ summaryStats.totalTransactions }}</p>
      </div>
      <div class="stat-card">
        <h3>Total Income</h3>
        <p class="stat-value positive">${{ summaryStats.totalIncome.toFixed(2) }}</p>
      </div>
      <div class="stat-card">
        <h3>Total Expenses</h3>
        <p class="stat-value negative">${{ summaryStats.totalExpenses.toFixed(2) }}</p>
      </div>
      <div class="stat-card">
        <h3>Net Income</h3>
        <p class="stat-value" :class="summaryStats.netIncome >= 0 ? 'positive' : 'negative'">
          ${{ summaryStats.netIncome.toFixed(2) }}
        </p>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { useLocalStore } from '@/stores/localStorage'
import SpendingByVendorChart from '@/components/SpendingByVendorChart.vue'
import MonthlySpendingTrendsChart from '@/components/MonthlySpendingTrendsChart.vue'
import IncomeVsExpensesChart from '@/components/IncomeVsExpensesChart.vue'

const localStore = useLocalStore()

const summaryStats = computed(() => {
  if (!localStore.transactions.data || localStore.transactions.data.length === 0) {
    return null
  }

  const totalTransactions = localStore.transactions.data.length
  const totalIncome = localStore.transactions.data
    .filter(t => t.fields.USD > 0)
    .reduce((sum, t) => sum + t.fields.USD, 0)
  const totalExpenses = localStore.transactions.data
    .filter(t => t.fields.USD < 0)
    .reduce((sum, t) => sum + Math.abs(t.fields.USD), 0)
  const netIncome = totalIncome - totalExpenses

  return {
    totalTransactions,
    totalIncome,
    totalExpenses,
    netIncome
  }
})
</script>

<style scoped>
.analytics-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.analytics-header {
  text-align: center;
  margin-bottom: 40px;
}

.analytics-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: #333;
}

.subtitle {
  font-size: 1.1rem;
  color: #666;
  margin: 0;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 40px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}

.stat-card h3 {
  margin: 0 0 10px 0;
  font-size: 1rem;
  color: #666;
  font-weight: 500;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
  color: #333;
}

.stat-value.positive {
  color: #059669;
}

.stat-value.negative {
  color: #dc2626;
}

@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-card {
    padding: 15px;
  }
  
  .analytics-header h1 {
    font-size: 2rem;
  }
  
  .stat-value {
    font-size: 1.5rem;
  }
}
</style>
