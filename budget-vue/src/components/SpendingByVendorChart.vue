<template>
  <div class="chart-container">
    <div class="chart-title">Top 10 Spending by Vendor</div>
    <Doughnut
      :data="chartData"
      :options="chartOptions"
      v-if="chartData.datasets[0].data.length > 0"
    />
    <div v-else class="no-data">
      No spending data available
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { useLocalStore } from '@/stores/localStorage'

const localStore = useLocalStore()

const chartData = computed(() => {
  if (!localStore.transactions.data || localStore.transactions.data.length === 0) {
    return { labels: [], datasets: [{ data: [], backgroundColor: [] }] }
  }

  // Group spending by vendor (only negative amounts)
  const vendorTotals = localStore.transactions.data
    .filter(transaction => transaction.fields.USD < 0) // Only expenses
    .reduce((acc, transaction) => {
      const vendor = transaction.fields.Vendor || 'Unknown'
      acc[vendor] = (acc[vendor] || 0) + Math.abs(transaction.fields.USD)
      return acc
    }, {} as Record<string, number>)

  // Sort by amount and take top 10
  const sortedVendors = Object.entries(vendorTotals)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 10)

  const labels = sortedVendors.map(([vendor]) => vendor)
  const data = sortedVendors.map(([, amount]) => amount)

  const colors = [
    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
    '#FF9F40', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'
  ]

  return {
    labels,
    datasets: [{
      data,
      backgroundColor: colors.slice(0, data.length),
      borderWidth: 2,
      borderColor: '#ffffff'
    }]
  }
})

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: {
        padding: 20
      }
    },
    tooltip: {
      callbacks: {
        label: function(context: any) {
          return context.label + ': $' + context.parsed.toFixed(2)
        }
      }
    }
  }
}))
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
}

.chart-title {
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #333;
}

.no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
  color: #666;
  font-size: 16px;
}
</style>