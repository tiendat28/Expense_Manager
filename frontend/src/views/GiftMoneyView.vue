<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useGiftMoneyStore } from '../stores/giftMoney'
import { GIFT_MONEY_TYPES, giftMoneyTypeMeta } from '../utils/giftMoney'
import PageShell from '../components/PageShell.vue'
import PageTitle from '../components/PageTitle.vue'
import FabButton from '../components/FabButton.vue'
import GiftMoneyFormModal from '../components/GiftMoneyFormModal.vue'
import { formatVND } from '../utils/formatters'

const PAGE_SIZE = 10

const store = useGiftMoneyStore()
const filter = ref('all')
const page = ref(1)
const showAdd = ref(false)
const editing = ref(null)

const filterTabs = computed(() => [['all', 'Tất cả'], ...GIFT_MONEY_TYPES.map((t) => [t.value, t.label])])

const filtered = computed(() => {
  if (filter.value === 'all') return store.items
  return store.items.filter((i) => i.type === filter.value)
})

const total = computed(() => filtered.value.reduce((sum, i) => sum + Number(i.amount), 0))

const pageCount = computed(() => Math.max(1, Math.ceil(filtered.value.length / PAGE_SIZE)))
const paginated = computed(() => {
  const start = (page.value - 1) * PAGE_SIZE
  return filtered.value.slice(start, start + PAGE_SIZE).map((item, i) => ({ ...item, stt: start + i + 1 }))
})

watch(filter, () => (page.value = 1))
watch(pageCount, (count) => {
  if (page.value > count) page.value = count
})

function closeModal() {
  showAdd.value = false
  editing.value = null
}

onMounted(() => store.fetchAll())
</script>

<template>
  <PageShell>
    <template #sticky>
      <PageTitle text="Tiền mừng" />
    </template>

    <div class="flex rounded-lg overflow-hidden border bg-white text-xs">
      <button
        v-for="f in filterTabs"
        :key="f[0]"
        class="flex-1 py-1.5"
        :class="filter === f[0] ? 'bg-green-600 text-white' : ''"
        @click="filter = f[0]"
      >
        {{ f[1] }}
      </button>
    </div>

    <div class="bg-white rounded-2xl px-4 py-2.5 card-shadow flex items-center justify-between">
      <span class="text-sm text-gray-900">Tổng cộng</span>
      <span class="font-semibold text-green-700">{{ formatVND(total) }}</span>
    </div>

    <p v-if="!filtered.length" class="bg-white rounded-2xl card-shadow text-center text-gray-900 py-6 text-sm">
      Chưa có khoản tiền mừng nào.
    </p>

    <!-- Mobile: card list -->
    <div v-else class="sm:hidden space-y-2">
      <div
        v-for="item in paginated"
        :key="item.id"
        class="bg-white rounded-2xl card-shadow px-4 py-3 cursor-pointer"
        @click="editing = item"
      >
        <div class="flex items-start justify-between gap-2">
          <div>
            <div class="font-medium">{{ item.name }}</div>
            <div class="text-xs text-gray-900">{{ item.address }}</div>
          </div>
          <div class="text-right shrink-0">
            <div class="font-semibold text-green-700">{{ formatVND(item.amount) }}</div>
            <div class="text-xs text-gray-900">{{ item.date }}</div>
          </div>
        </div>
        <div class="flex items-center justify-between mt-2">
          <span class="px-1.5 py-0.5 rounded-full text-xs" :class="giftMoneyTypeMeta(item.type).color">
            {{ giftMoneyTypeMeta(item.type).label }}
          </span>
          <span v-if="item.note" class="text-xs text-gray-900 truncate ml-2">{{ item.note }}</span>
        </div>
      </div>
    </div>

    <!-- Desktop: table -->
    <div v-if="filtered.length" class="hidden sm:block bg-white rounded-2xl card-shadow overflow-x-auto">
      <table class="w-full text-xs whitespace-nowrap">
        <thead>
          <tr class="border-b text-left text-gray-900">
            <th class="px-2 py-3 font-medium">STT</th>
            <th class="px-2 py-3 font-medium">Họ và tên</th>
            <th class="px-2 py-3 font-medium">Xã/Tỉnh</th>
            <th class="px-2 py-3 font-medium">Tiền mừng</th>
            <th class="px-2 py-3 font-medium">Loại</th>
            <th class="px-2 py-3 font-medium">Thời gian</th>
            <th class="px-2 py-3 font-medium">Note</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="item in paginated"
            :key="item.id"
            class="border-b last:border-0 cursor-pointer hover:bg-gray-50"
            @click="editing = item"
          >
            <td class="px-2 py-3 text-gray-900">{{ item.stt }}</td>
            <td class="px-2 py-3 font-medium">{{ item.name }}</td>
            <td class="px-2 py-3 text-gray-900">{{ item.address }}</td>
            <td class="px-2 py-3 font-medium text-green-700">{{ formatVND(item.amount) }}</td>
            <td class="px-2 py-3">
              <span class="px-1.5 py-0.5 rounded-full text-xs" :class="giftMoneyTypeMeta(item.type).color">
                {{ giftMoneyTypeMeta(item.type).label }}
              </span>
            </td>
            <td class="px-2 py-3 text-gray-900">{{ item.date }}</td>
            <td class="px-2 py-3 text-gray-900 max-w-[140px] truncate">{{ item.note || '—' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="pageCount > 1" class="flex w-fit mx-auto items-center gap-4 text-xs bg-white rounded-2xl card-shadow px-4 py-2">
      <button class="px-2.5 py-1 rounded-lg border disabled:opacity-40" :disabled="page === 1" @click="page--">‹</button>
      <span class="text-gray-900">Trang {{ page }} / {{ pageCount }}</span>
      <button class="px-2.5 py-1 rounded-lg border disabled:opacity-40" :disabled="page === pageCount" @click="page++">›</button>
    </div>

    <FabButton @click="showAdd = true" />
    <GiftMoneyFormModal v-if="showAdd || editing" :existing="editing" @close="closeModal" @saved="closeModal" />
  </PageShell>
</template>
