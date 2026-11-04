<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useGiftMoneyStore } from '../stores/giftMoney'
import { usePagination } from '../composables/usePagination'
import { useConfirmDelete } from '../composables/useConfirmDelete'
import { GIFT_MONEY_TYPES, giftMoneyTypeMeta } from '../utils/giftMoney'
import { formatVND } from '../utils/formatters'
import PageShell from '../components/PageShell.vue'
import FabButton from '../components/FabButton.vue'
import RowActions from '../components/RowActions.vue'
import PaginationBar from '../components/PaginationBar.vue'
import EmptyState from '../components/EmptyState.vue'
import GiftMoneyFormModal from '../components/GiftMoneyFormModal.vue'

const store = useGiftMoneyStore()
const confirmDelete = useConfirmDelete()

const filter = ref('all')
const search = ref('')
const showAdd = ref(false)
const editing = ref(null)

const filterTabs = computed(() => [['all', 'Tất cả'], ...GIFT_MONEY_TYPES.map((t) => [t.value, t.label])])

const filtered = computed(() => {
  return store.items.filter((i) => {
    if (filter.value !== 'all' && i.type !== filter.value) return false
    if (search.value) {
      const kw = search.value.toLowerCase().trim()
      const nameMatch = (i.name || '').toLowerCase().includes(kw)
      const addrMatch = (i.address || '').toLowerCase().includes(kw)
      const noteMatch = (i.note || '').toLowerCase().includes(kw)
      if (!nameMatch && !addrMatch && !noteMatch) return false
    }
    return true
  })
})

const totalAmount = computed(() => store.items.reduce((sum, i) => sum + Number(i.amount), 0))
const weddingTotal = computed(() =>
  store.items.filter((i) => i.type === 'wedding').reduce((sum, i) => sum + Number(i.amount), 0)
)
const filteredTotal = computed(() => filtered.value.reduce((sum, i) => sum + Number(i.amount), 0))

const { page, pageCount, paginated } = usePagination(filtered)

watch([filter, search], () => (page.value = 1))

function closeModal() {
  showAdd.value = false
  editing.value = null
}

function removeItem(item) {
  return confirmDelete(`Bạn có chắc chắn muốn xóa khoản tiền mừng của "${item.name}"?`, () => store.remove(item.id))
}

onMounted(() => store.fetchAll())
</script>

<template>
  <PageShell>
    <!-- Top Stats Banner Matching FinFlow -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-5">
      <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow transition-colors">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Tổng tiền mừng lưu sổ</span>
          <span class="w-9 h-9 rounded-xl bg-emerald-50 dark:bg-emerald-950/80 text-emerald-500 flex items-center justify-center">
            <i class="fa-solid fa-envelope-open-text"></i>
          </span>
        </div>
        <h3 class="font-display font-extrabold text-2xl text-emerald-600 dark:text-emerald-400">
          {{ formatVND(totalAmount) }}
        </h3>
        <p class="text-xs text-slate-400 mt-1">Toàn bộ các dịp sự kiện</p>
      </div>

      <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow transition-colors">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Tiền cưới hỏi</span>
          <span class="w-9 h-9 rounded-xl bg-rose-50 dark:bg-rose-950/80 text-rose-500 flex items-center justify-center">
            <i class="fa-solid fa-heart"></i>
          </span>
        </div>
        <h3 class="font-display font-extrabold text-2xl text-slate-900 dark:text-white">
          {{ formatVND(weddingTotal) }}
        </h3>
        <p class="text-xs text-slate-400 mt-1">Chiếm tỷ trọng lớn nhất</p>
      </div>

      <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow transition-colors">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">Tổng sự kiện lưu sổ</span>
          <span class="w-9 h-9 rounded-xl bg-amber-50 dark:bg-amber-950/80 text-amber-500 flex items-center justify-center">
            <i class="fa-solid fa-book-bookmark"></i>
          </span>
        </div>
        <h3 class="font-display font-extrabold text-2xl text-emerald-600 dark:text-emerald-400">
          {{ store.items.length }} sự kiện
        </h3>
        <p class="text-xs text-slate-400 mt-1">Tra cứu nhanh lịch sử có đi có lại</p>
      </div>
    </div>

    <!-- Search & Group Filter Bar Matching FinFlow -->
    <div class="bg-white dark:bg-slate-900 p-4 sm:p-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow flex flex-col lg:flex-row lg:items-center justify-between gap-4 transition-colors">
      <div class="flex flex-wrap items-center gap-3 flex-1">
        <!-- Search Input -->
        <div class="relative flex-1 min-w-[200px]">
          <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
          <input
            v-model="search"
            type="text"
            placeholder="Tra cứu nhanh tên bạn bè, địa chỉ, ghi chú..."
            class="w-full pl-9 pr-4 py-2.5 text-xs rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200/70 dark:border-slate-700 text-slate-800 dark:text-slate-100 focus:outline-none focus:border-emerald-500"
          />
        </div>

        <!-- Filter Segmented Tabs -->
        <div class="inline-flex flex-wrap p-1 rounded-xl bg-slate-100 dark:bg-slate-800">
          <button
            v-for="f in filterTabs"
            :key="f[0]"
            type="button"
            class="px-3 sm:px-3.5 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer"
            :class="filter === f[0] ? 'bg-white dark:bg-slate-900 text-emerald-600 dark:text-emerald-400 shadow-2xs' : 'text-slate-600 dark:text-slate-400'"
            @click="filter = f[0]"
          >
            {{ f[1] }}
          </button>
        </div>
      </div>

      <button
        @click="showAdd = true"
        class="hidden md:flex px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold items-center gap-2 self-start lg:self-auto transition cursor-pointer shadow-sm shadow-emerald-600/20"
      >
        <i class="fa-solid fa-plus"></i> Ghi tiền mừng
      </button>
    </div>

    <!-- Empty State -->
    <EmptyState v-if="!filtered.length" boxed text="Chưa có khoản tiền mừng nào khớp với bộ lọc." />

    <!-- List & Table -->
    <div v-else class="space-y-4">
      <!-- Mobile: Card List -->
      <div class="sm:hidden space-y-3">
        <div
          v-for="item in paginated"
          :key="item.id"
          class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/90 dark:border-slate-800 p-4 card-shadow space-y-3"
        >
          <div class="flex items-start justify-between gap-2">
            <div>
              <h4 class="font-bold text-sm text-slate-900 dark:text-white">{{ item.name }}</h4>
              <p class="text-xs text-slate-400">{{ item.address || 'Không ghi địa chỉ' }}</p>
            </div>
            <span class="font-bold text-sm text-emerald-600 dark:text-emerald-400">
              {{ formatVND(item.amount) }}
            </span>
          </div>

          <div class="flex items-center justify-between pt-2 border-t border-slate-100 dark:border-slate-800 text-xs">
            <span
              class="px-2 py-0.5 rounded-md font-semibold text-[11px]"
              :class="item.type === 'wedding' ? 'bg-rose-50 dark:bg-rose-950/80 text-rose-600 dark:text-rose-400' : 'bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400'"
            >
              {{ giftMoneyTypeMeta(item.type).label }}
            </span>
            <span class="text-slate-400">{{ item.date }}</span>
            <RowActions @edit="editing = item" @remove="removeItem(item)" />
          </div>
        </div>
      </div>

      <!-- Desktop/iPad: Table Matching FinFlow -->
      <div class="hidden sm:block bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/90 dark:border-slate-800 card-shadow overflow-hidden transition-colors">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b border-slate-200/80 dark:border-slate-800 text-[11px] font-bold uppercase tracking-wider text-slate-400 bg-slate-50/50 dark:bg-slate-800/40">
                <th class="py-3.5 px-5">Tên khách / Bạn bè</th>
                <th class="py-3.5 px-5">Địa chỉ / Quê quán</th>
                <th class="py-3.5 px-5 text-center">Dịp sự kiện</th>
                <th class="py-3.5 px-5">Thời gian</th>
                <th class="py-3.5 px-5 text-right">Tiền mừng</th>
                <th class="py-3.5 px-5">Ghi chú</th>
                <th class="py-3.5 px-5 text-center">Thao tác</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800/70 text-sm">
              <tr
                v-for="item in paginated"
                :key="item.id"
                class="hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition"
              >
                <td class="py-3.5 px-5 font-bold text-xs sm:text-sm text-slate-900 dark:text-white">
                  {{ item.name }}
                </td>
                <td class="py-3.5 px-5 text-xs text-slate-600 dark:text-slate-300">
                  <span v-if="item.address" class="px-2 py-1 rounded-lg bg-slate-100 dark:bg-slate-800">
                    {{ item.address }}
                  </span>
                  <span v-else class="text-slate-400">—</span>
                </td>
                <td class="py-3.5 px-5 text-center whitespace-nowrap">
                  <span
                    class="text-[11px] font-semibold px-2.5 py-1 rounded-md"
                    :class="item.type === 'wedding' ? 'bg-rose-50 dark:bg-rose-950/80 text-rose-600 dark:text-rose-400' : 'bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400'"
                  >
                    {{ giftMoneyTypeMeta(item.type).label }}
                  </span>
                </td>
                <td class="py-3.5 px-5 text-xs text-slate-500 dark:text-slate-400 whitespace-nowrap">{{ item.date }}</td>
                <td class="py-3.5 px-5 text-right font-bold text-xs sm:text-sm text-emerald-600 dark:text-emerald-400 whitespace-nowrap">
                  {{ formatVND(item.amount) }}
                </td>
                <td class="py-3.5 px-5 text-xs text-slate-500 dark:text-slate-400 max-w-[200px] truncate">
                  {{ item.note || '—' }}
                </td>
                <td class="py-3.5 px-5 text-center whitespace-nowrap">
                  <RowActions class="justify-center" @edit="editing = item" @remove="removeItem(item)" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Bottom Pagination -->
    <template v-if="pageCount > 1" #bottom>
      <div class="flex justify-center">
        <PaginationBar v-model:page="page" :page-count="pageCount" />
      </div>
    </template>

    <FabButton @click="showAdd = true" />
    <GiftMoneyFormModal v-if="showAdd || editing" :existing="editing" @close="closeModal" @saved="closeModal" />
  </PageShell>
</template>
