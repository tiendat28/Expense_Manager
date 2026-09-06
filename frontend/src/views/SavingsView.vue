<script setup>
import { ref, onMounted } from 'vue'
import { useSavingsStore } from '../stores/savings'
import { formatVND } from '../utils/formatters'
import SavingsGoalFormModal from '../components/SavingsGoalFormModal.vue'
import PageShell from '../components/PageShell.vue'

const store = useSavingsStore()
const showAdd = ref(false)

function savedAmount(goal) {
  return goal.contributions.reduce((s, c) => s + c.amount, 0)
}
function progress(goal) {
  return goal.target_amount > 0 ? Math.min(savedAmount(goal) / goal.target_amount, 1) * 100 : 0
}

onMounted(() => store.fetchAll())
</script>

<template>
  <PageShell>
    <template #sticky>
      <h1 class="text-xl sm:text-2xl font-bold text-green-800">Tiết kiệm</h1>
    </template>

    <p v-if="!store.goals.length" class="text-center text-gray-900 py-10 text-sm">Chưa có mục tiêu tiết kiệm nào. Nhấn + để tạo.</p>
    <div class="space-y-3">
      <router-link
        v-for="goal in store.goals" :key="goal.id" :to="`/savings/${goal.id}`"
        class="block bg-white rounded-2xl border p-4"
      >
        <div class="flex items-center mb-2">
          <span class="text-2xl mr-2">{{ goal.icon }}</span>
          <div class="flex-1">
            <div class="font-semibold">{{ goal.name }}</div>
            <div class="text-xs text-gray-900">{{ formatVND(savedAmount(goal)) }} / {{ formatVND(goal.target_amount) }}</div>
          </div>
          <span v-if="progress(goal) >= 100" class="text-green-500">✓</span>
        </div>
        <div class="h-1.5 bg-gray-100 rounded-full overflow-hidden">
          <div class="h-full bg-green-500 rounded-full" :style="{ width: progress(goal) + '%' }"></div>
        </div>
      </router-link>
    </div>

    <button @click="showAdd = true" class="fixed bottom-20 sm:bottom-6 right-6 w-14 h-14 rounded-full bg-green-600 text-white text-2xl shadow-lg">+</button>
    <SavingsGoalFormModal v-if="showAdd" @close="showAdd = false" @saved="showAdd = false" />
  </PageShell>
</template>
