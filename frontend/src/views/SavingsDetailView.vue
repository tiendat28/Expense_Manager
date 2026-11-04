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
    <div v-if="goal" class="space-y-6 max-w-3xl mx-auto">
      <DetailHeader @edit="showEdit = true" @remove="removeGoal" />

      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/90 dark:border-slate-800 p-6 sm:p-8 text-center card-shadow transition-colors">
        <div class="text-4xl mb-3">{{ goal.icon || '🎯' }}</div>
        <h2 class="font-display font-bold text-xl text-slate-900 dark:text-white">{{ goal.name }}</h2>

        <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 mt-4 mb-4 max-w-md mx-auto space-y-2">
          <div class="flex justify-between text-xs text-slate-500 dark:text-slate-400">
            <span>Đã tích lũy: <strong class="text-emerald-600 dark:text-emerald-400 font-bold">{{ formatVND(savedAmount) }}</strong></span>
            <span>Mục tiêu: <strong class="text-slate-800 dark:text-slate-200 font-bold">{{ formatVND(goal.target_amount) }}</strong></span>
          </div>

          <div class="h-2.5 bg-slate-200/80 dark:bg-slate-700 rounded-full overflow-hidden">
            <div
              class="h-full rounded-full progress-bar-fill bg-emerald-500"
              :style="{ width: Math.min(100, progress) + '%' }"
            ></div>
          </div>

          <div class="flex justify-between items-center text-xs pt-1">
            <span class="text-slate-400">Đã tiết kiệm được {{ daysSaving }} ngày</span>
            <span class="font-bold text-emerald-600 dark:text-emerald-400">{{ Math.round(progress) }}%</span>
          </div>
        </div>

        <div v-if="progress >= 100" class="text-emerald-600 dark:text-emerald-400 text-sm font-semibold">
          🎉 Chúc mừng! Bạn đã hoàn thành mục tiêu tích lũy này!
        </div>
      </div>

      <HistoryList
        title="Lịch sử nạp tiền"
        empty-text="Chưa có lần nạp nào."
        :items="goal.contributions"
        @select="editingContribution = $event"
      />

      <button
        class="block w-full sm:max-w-md sm:mx-auto bg-gradient-to-r from-emerald-600 to-green-500 hover:from-emerald-700 hover:to-green-600 text-white rounded-xl py-3 font-semibold text-sm shadow-md shadow-emerald-500/20 transition cursor-pointer"
        @click="showAddContribution = true"
      >
        <i class="fa-solid fa-plus mr-1.5"></i> Nạp thêm tích lũy
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
