<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSavingsStore } from '../stores/savings'
import { useConfirmDelete } from '../composables/useConfirmDelete'
import { formatVND } from '../utils/formatters'
import { percent } from '../utils/progress'
import { savedAmount as sumContributions } from '../utils/savings'
import SavingsGoalFormModal from '../components/SavingsGoalFormModal.vue'
import ContributionFormModal from '../components/ContributionFormModal.vue'
import DetailHeader from '../components/DetailHeader.vue'
import HistoryList from '../components/HistoryList.vue'
import PageShell from '../components/PageShell.vue'

const route = useRoute()
const router = useRouter()
const store = useSavingsStore()
const confirmDelete = useConfirmDelete()
const showEdit = ref(false)
const showAddContribution = ref(false)
const editingContribution = ref(null)

const goal = computed(() => store.goals.find((g) => g.id === Number(route.params.id)))
const savedAmount = computed(() => (goal.value ? sumContributions(goal.value) : 0))
const progress = computed(() => (goal.value ? percent(savedAmount.value, goal.value.target_amount) : 0))
const daysSaving = computed(() => {
  if (!goal.value) return 0
  const diff = Date.now() - new Date(goal.value.created_at).getTime()
  return Math.max(Math.floor(diff / (1000 * 60 * 60 * 24)), 0)
})

async function removeGoal() {
  const message = `Bạn có chắc chắn muốn xóa mục tiêu "${goal.value.name}"?`
  if (await confirmDelete(message, () => store.remove(goal.value.id))) {
    router.push({ name: 'savings' })
  }
}

onMounted(() => {
  if (!store.goals.length) store.fetchAll()
})
</script>

<template>
  <PageShell>
    <div v-if="goal">
      <DetailHeader @edit="showEdit = true" @remove="removeGoal" />

      <div class="bg-white rounded-2xl card-shadow p-6 text-center mb-4">
        <div class="text-4xl mb-2">{{ goal.icon }}</div>
        <div class="font-semibold text-lg">{{ goal.name }}</div>
        <div class="text-sm text-gray-900 mb-2">
          {{ formatVND(savedAmount) }} / {{ formatVND(goal.target_amount) }}
        </div>
        <div class="h-2 bg-gray-100 rounded-full overflow-hidden mb-2">
          <div class="h-full bg-green-500 rounded-full" :style="{ width: progress + '%' }"></div>
        </div>
        <div class="text-xs text-gray-900">Đã tiết kiệm được {{ daysSaving }} ngày</div>
        <div v-if="progress >= 100" class="text-green-600 text-sm mt-1">🎉 Đã đạt mục tiêu!</div>
      </div>

      <HistoryList
        title="Lịch sử nạp tiền"
        empty-text="Chưa có lần nạp nào."
        :items="goal.contributions"
        @select="editingContribution = $event"
      />

      <button
        class="sticky bottom-6 block w-full sm:max-w-md sm:mx-auto bg-green-600 text-white rounded-xl py-3 font-medium"
        @click="showAddContribution = true"
      >
        Nạp tiền
      </button>

      <SavingsGoalFormModal v-if="showEdit" :existing="goal" @close="showEdit = false" @saved="showEdit = false" />
      <ContributionFormModal
        v-if="showAddContribution"
        :goal-id="goal.id"
        :goal-name="goal.name"
        @close="showAddContribution = false"
        @saved="showAddContribution = false"
      />
      <ContributionFormModal
        v-if="editingContribution"
        :goal-id="goal.id"
        :goal-name="goal.name"
        :existing="editingContribution"
        @close="editingContribution = null"
        @saved="editingContribution = null"
      />
    </div>
  </PageShell>
</template>
