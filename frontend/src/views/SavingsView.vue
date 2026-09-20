<script setup>
import { ref, onMounted } from 'vue'
import { useSavingsStore } from '../stores/savings'
import { formatVND } from '../utils/formatters'
import { percent } from '../utils/progress'
import { savedAmount } from '../utils/savings'
import SavingsGoalFormModal from '../components/SavingsGoalFormModal.vue'
import PageShell from '../components/PageShell.vue'
import FabButton from '../components/FabButton.vue'
import PageTitle from '../components/PageTitle.vue'
import EmptyState from '../components/EmptyState.vue'

const store = useSavingsStore()
const showAdd = ref(false)

const progress = (goal) => percent(savedAmount(goal), goal.target_amount)

onMounted(() => store.fetchAll())
</script>

<template>
  <PageShell>
    <template #sticky>
      <PageTitle text="Tiết kiệm" />
    </template>

    <EmptyState v-if="!store.goals.length" text="Chưa có mục tiêu tiết kiệm nào. Nhấn + để tạo." />
    <div v-else class="space-y-3">
      <router-link
        v-for="goal in store.goals" :key="goal.id" :to="`/savings/${goal.id}`"
        class="block bg-white rounded-2xl card-shadow p-4"
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

    <FabButton @click="showAdd = true" />
    <SavingsGoalFormModal v-if="showAdd" @close="showAdd = false" @saved="showAdd = false" />
  </PageShell>
</template>
