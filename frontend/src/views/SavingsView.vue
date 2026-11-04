<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSavingsStore } from '../stores/savings'
import { formatVND } from '../utils/formatters'
import { percent } from '../utils/progress'
import { savedAmount } from '../utils/savings'
import SavingsGoalFormModal from '../components/SavingsGoalFormModal.vue'
import ContributionFormModal from '../components/ContributionFormModal.vue'
import PageShell from '../components/PageShell.vue'
import FabButton from '../components/FabButton.vue'
import EmptyState from '../components/EmptyState.vue'

const router = useRouter()
const store = useSavingsStore()
const showAdd = ref(false)
const contributingGoal = ref(null)

const progress = (goal) => percent(savedAmount(goal), goal.target_amount)

const totalSaved = computed(() =>
  store.goals.reduce((s, g) => s + savedAmount(g), 0)
)
const totalTarget = computed(() =>
  store.goals.reduce((s, g) => s + Number(g.target_amount), 0)
)
const totalPercent = computed(() =>
  totalTarget.value > 0 ? Math.round((totalSaved.value / totalTarget.value) * 100) : 0
)

onMounted(() => store.fetchAll())
</script>

<template>
  <PageShell>
    <!-- Top Summary Banner Matching FinFlow -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-5">
      <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow transition-colors">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Tổng tiền đã tích lũy</span>
          <span class="w-9 h-9 rounded-xl bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
            <i class="fa-solid fa-piggy-bank"></i>
          </span>
        </div>
        <h3 class="font-display font-extrabold text-2xl text-emerald-600 dark:text-emerald-400">
          {{ formatVND(totalSaved) }}
        </h3>
        <p class="text-xs text-slate-400 mt-1">Tổng cộng các quỹ mục tiêu</p>
      </div>

      <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow transition-colors">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Tổng hạn mức mục tiêu</span>
          <span class="w-9 h-9 rounded-xl bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
            <i class="fa-solid fa-bullseye"></i>
          </span>
        </div>
        <h3 class="font-display font-extrabold text-2xl text-slate-900 dark:text-white">
          {{ formatVND(totalTarget) }}
        </h3>
        <p class="text-xs text-slate-400 mt-1">Đã hoàn thành {{ totalPercent }}% kế hoạch</p>
      </div>

      <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow transition-colors">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Số lượng quỹ mục tiêu</span>
          <span class="w-9 h-9 rounded-xl bg-amber-50 dark:bg-amber-950/80 text-amber-500 flex items-center justify-center">
            <i class="fa-solid fa-shield-heart"></i>
          </span>
        </div>
        <h3 class="font-display font-extrabold text-2xl text-emerald-600 dark:text-emerald-400">
          {{ store.goals.length }} mục tiêu
        </h3>
        <p class="text-xs text-slate-400 mt-1">Đang chủ động kế hoạch tài chính</p>
      </div>
    </div>

    <!-- Header Actions -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div>
        <h3 class="font-display font-bold text-lg text-slate-900 dark:text-white flex items-center gap-2">
          <i class="fa-solid fa-bullseye text-emerald-600 dark:text-emerald-400"></i> Mục tiêu tích lũy cá nhân (Saving Goals)
        </h3>
        <p class="text-xs text-slate-400">Chia nhỏ dòng tiền vào các quỹ mục tiêu để chủ động kế hoạch tài chính</p>
      </div>
      <button
        @click="showAdd = true"
        class="hidden md:flex px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold items-center gap-2 self-start sm:self-auto transition cursor-pointer shadow-sm shadow-emerald-600/20"
      >
        <i class="fa-solid fa-plus"></i> Tạo mục tiêu mới
      </button>
    </div>

    <!-- Empty State -->
    <EmptyState v-if="!store.goals.length" boxed text="Chưa có mục tiêu tiết kiệm nào. Nhấn '+' hoặc 'Tạo mục tiêu mới' để bắt đầu." />

    <!-- Saving Goals Grid Matching FinFlow HTML -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">
      <div
        v-for="(goal, idx) in store.goals"
        :key="goal.id"
        class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow flex flex-col justify-between space-y-4 hover:border-emerald-400 dark:hover:border-emerald-700 transition cursor-pointer"
        @click="router.push(`/savings/${goal.id}`)"
      >
        <div>
          <!-- Top Icon & Percentage Badge -->
          <div class="flex items-center justify-between mb-3">
            <div class="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400 flex items-center justify-center text-lg">
              <span>{{ goal.icon || '🎯' }}</span>
            </div>
            <span
              class="text-xs font-extrabold px-2.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400"
            >
              {{ Math.round(progress(goal)) }}%
            </span>
          </div>

          <!-- Goal Info -->
          <h4 class="font-display font-bold text-sm sm:text-base text-slate-900 dark:text-white truncate">
            {{ goal.name }}
          </h4>
          <p class="text-[11px] text-slate-400 mt-1">
            {{ goal.contributions?.length || 0 }} lần nạp tích lũy
          </p>

          <!-- Progress Bar & Amounts -->
          <div class="mt-4">
            <div class="flex items-baseline justify-between text-xs mb-1.5">
              <strong class="text-slate-900 dark:text-white font-bold">{{ formatVND(savedAmount(goal)) }}</strong>
              <span class="text-slate-400">/ {{ formatVND(goal.target_amount) }}</span>
            </div>
            <div class="w-full h-2.5 rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden">
              <div
                class="h-full rounded-full progress-bar-fill bg-emerald-500"
                :style="{ width: Math.min(100, progress(goal)) + '%' }"
              ></div>
            </div>
          </div>
        </div>

        <!-- Action Button -->
        <button
          type="button"
          @click.stop="contributingGoal = goal"
          class="w-full py-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-emerald-600 hover:text-white text-slate-700 dark:text-slate-200 text-xs font-semibold transition cursor-pointer"
        >
          <i class="fa-solid fa-plus mr-1"></i> Nạp thêm tích lũy
        </button>
      </div>
    </div>

    <!-- Modals -->
    <FabButton @click="showAdd = true" />
    <SavingsGoalFormModal v-if="showAdd" @close="showAdd = false" @saved="showAdd = false; store.fetchAll()" />
    <ContributionFormModal
      v-if="contributingGoal"
      :goal-id="contributingGoal.id"
      :goal-name="contributingGoal.name"
      @close="contributingGoal = null"
      @saved="contributingGoal = null; store.fetchAll()"
    />
  </PageShell>
</template>
