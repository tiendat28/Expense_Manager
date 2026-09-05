<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSavingsStore } from '../stores/savings'
import { formatVND } from '../utils/formatters'
import SavingsGoalFormModal from '../components/SavingsGoalFormModal.vue'
import ContributionFormModal from '../components/ContributionFormModal.vue'
import PageShell from '../components/PageShell.vue'

const route = useRoute()
const router = useRouter()
const store = useSavingsStore()
const showEdit = ref(false)
const showAddContribution = ref(false)
const editingContribution = ref(null)

const goal = computed(() => store.goals.find((g) => g.id === Number(route.params.id)))
const savedAmount = computed(() => (goal.value ? goal.value.contributions.reduce((s, c) => s + c.amount, 0) : 0))
const progress = computed(() =>
  goal.value && goal.value.target_amount > 0 ? Math.min(savedAmount.value / goal.value.target_amount, 1) * 100 : 0
)
const sortedContributions = computed(() =>
  goal.value ? [...goal.value.contributions].sort((a, b) => new Date(b.date) - new Date(a.date)) : []
)
const daysSaving = computed(() => {
  if (!goal.value) return 0
  const diff = Date.now() - new Date(goal.value.created_at).getTime()
  return Math.max(Math.floor(diff / (1000 * 60 * 60 * 24)), 0)
})

async function removeGoal() {
  await store.remove(goal.value.id)
  router.push({ name: 'savings' })
}

onMounted(() => {
  if (!store.goals.length) store.fetchAll()
})
</script>

<template>
  <PageShell>
  <div v-if="goal">
    <div class="flex items-center justify-between mb-3">
      <button @click="router.back()" class="text-gray-900">‹ Quay lại</button>
      <div class="flex gap-3 text-sm">
        <button @click="showEdit = true" class="text-green-600">Sửa</button>
        <button @click="removeGoal" class="text-red-500">Xóa</button>
      </div>
    </div>

    <div class="bg-white rounded-2xl p-6 text-center mb-4">
      <div class="text-4xl mb-2">{{ goal.icon }}</div>
      <div class="font-semibold text-lg">{{ goal.name }}</div>
      <div class="text-sm text-gray-900 mb-2">{{ formatVND(savedAmount) }} / {{ formatVND(goal.target_amount) }}</div>
      <div class="h-2 bg-gray-100 rounded-full overflow-hidden mb-2">
        <div class="h-full bg-green-500 rounded-full" :style="{ width: progress + '%' }"></div>
      </div>
      <div class="text-xs text-gray-900">Đã tiết kiệm được {{ daysSaving }} ngày</div>
      <div v-if="progress >= 100" class="text-green-600 text-sm mt-1">🎉 Đã đạt mục tiêu!</div>
    </div>

    <h3 class="font-semibold mb-2 text-sm text-gray-900">Lịch sử nạp tiền</h3>
    <div class="bg-white rounded-2xl divide-y mb-24">
      <p v-if="!sortedContributions.length" class="text-center text-gray-900 py-6 text-sm">Chưa có lần nạp nào.</p>
      <div
        v-for="c in sortedContributions" :key="c.id"
        class="flex items-center justify-between px-4 py-3 cursor-pointer"
        @click="editingContribution = c"
      >
        <div>
          <div>{{ formatVND(c.amount) }}</div>
          <div class="text-xs text-gray-900">{{ new Date(c.date).toLocaleString('vi-VN') }}</div>
        </div>
        <span class="text-gray-300">›</span>
      </div>
    </div>

    <button
      @click="showAddContribution = true"
      class="sticky bottom-6 block w-full sm:max-w-md sm:mx-auto bg-green-600 text-white rounded-xl py-3 font-medium"
    >
      Nạp tiền
    </button>

    <SavingsGoalFormModal v-if="showEdit" :existing="goal" @close="showEdit = false" @saved="showEdit = false" />
    <ContributionFormModal v-if="showAddContribution" :goal-id="goal.id" :goal-name="goal.name" @close="showAddContribution = false" @saved="showAddContribution = false" />
    <ContributionFormModal
      v-if="editingContribution" :goal-id="goal.id" :goal-name="goal.name" :existing="editingContribution"
      @close="editingContribution = null" @saved="editingContribution = null"
    />
  </div>
  </PageShell>
</template>
