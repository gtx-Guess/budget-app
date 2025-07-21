<template>
  <div class="chart-container">
    <div class="chart-title">Monthly Income vs Expenses Trends</div>
    <Line
      :data="chartData"
      :options="chartOptions"
      v-if="chartData.datasets[0].data.length > 0"
    />
    <div v-else class="no-data">
      No transaction data available
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import { useLocalStore } from '@/stores/localStorage'

const localStore = useLocalStore()

const chartData = computed(() => {
  if (!localStore.transactions.data || localStore.transactions.data.length === 0) {
    return { labels: [], datasets: [{ data: [] }, { data: [] }] }
  }

  // Group transactions by month
  const monthlyData = localStore.transactions.data.reduce((acc, transaction) => {
    const date = new Date(transaction.fields.Date)
    const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
    
    if (!acc[monthKey]) {
      acc[monthKey] = { income: 0, expenses: 0 }
    }
    
    if (transaction.fields.USD > 0) {
      acc[monthKey].income += transaction.fields.USD
    } else {
      acc[monthKey].expenses += Math.abs(transaction.fields.USD)
    }
    
    return acc
  }, {} as Record<string, { income: number, expenses: number }>)

  // Sort months and create labels
  const sortedMonths = Object.keys(monthlyData).sort()
  const labels = sortedMonths.map(month => {
    const [year, monthNum] = month.split('-')
    const date = new Date(parseInt(year), parseInt(monthNum) - 1)
    return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
  })

  const expensesData = sortedMonths.map(month => monthlyData[month].expenses)
  const incomeData = sortedMonths.map(month => monthlyData[month].income)

  return {
    labels,
    datasets: [
      {
        label: 'Monthly Expenses',
        data: expensesData,
        borderColor: '#FF6384',
        backgroundColor: '#FF6384',
        fill: false,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6
      },
      {
        label: 'Monthly Income',
        data: incomeData,
        borderColor: '#36A2EB',
        backgroundColor: '#36A2EB',
        fill: false,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6
      }
    ]
  }
})

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const,
      labels: {
        padding: 20
      }
    },
    tooltip: {
      callbacks: {
        label: function(context: any) {
          return context.dataset.label + ': $' + context.parsed.y.toFixed(2)
        }
      }
    }
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Month'
      }
    },
    y: {
      title: {
        display: true,
        text: 'Amount ($)'
      },
      ticks: {
        callback: function(value: any) {
          return '$' + value.toLocaleString()
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