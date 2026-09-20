<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useGiftMoneyStore } from '../stores/giftMoney'
import { usePagination } from '../composables/usePagination'
import { useConfirmDelete } from '../composables/useConfirmDelete'
import { GIFT_MONEY_TYPES, giftMoneyTypeMeta } from '../utils/giftMoney'
import { formatVND } from '../utils/formatters'
import PageShell from '../components/PageShell.vue'
import PageTitle from '../components/PageTitle.vue'
import FabButton from '../components/FabButton.vue'
import RowActions from '../components/RowActions.vue'
import PaginationBar from '../components/PaginationBar.vue'
import EmptyState from '../components/EmptyState.vue'
import GiftMoneyFormModal from '../components/GiftMoneyFormModal.vue'

const store = useGiftMoneyStore()
const confirmDelete = useConfirmDelete()
const filter = ref('all')
const showAdd = ref(false)
const editing = ref(null)

const filterTabs = computed(() => [['all', 'Tất cả'], ...GIFT_MONEY_TYPES.map((t) => [t.value, t.label])])

const filtered = computed(() => {
  if (filter.value === 'all') return store.items
  return store.items.filter((i) => i.type === filter.value)
})

const total = computed(() => filtered.value.reduce((sum, i) => sum + Number(i.amount), 0))

const { page, pageCount, paginated } = usePagination(filtered)

watch(filter, () => (page.value = 1))

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
    <template #sticky>
      <div class="space-y-3">
        <div class="flex items-center justify-between gap-2">
          <PageTitle text="Tiền mừng" />
          <PaginationBar v-if="pageCount > 1" v-model:page="page" :page-count="pageCount" compact class="sm:hidden" />
        </div>

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
      </div>
    </template>

    <EmptyState v-if="!filtered.length" boxed text="Chưa có khoản tiền mừng nào." />

    <div v-else>
      <!-- Mobile: card list -->
      <div class="sm:hidden space-y-2">
        <div v-for="item in paginated" :key="item.id" class="bg-white rounded-2xl card-shadow px-4 py-3">
          <div class="flex items-start justify-between gap-2">
            <div class="min-w-0">
              <div class="font-medium truncate">{{ item.name }}</div>
              <div class="text-xs text-gray-900">{{ item.address }}</div>
            </div>
            <div class="text-right shrink-0">
              <div class="font-semibold text-green-700">{{ formatVND(item.amount) }}</div>
              <div class="text-xs text-gray-900">{{ item.date }}</div>
            </div>
          </div>
          <div class="flex items-center gap-2 mt-2">
            <span class="px-1.5 py-0.5 rounded-full text-xs shrink-0" :class="giftMoneyTypeMeta(item.type).color">
              {{ giftMoneyTypeMeta(item.type).label }}
            </span>
            <span v-if="item.note" class="text-xs text-gray-900 truncate flex-1">{{ item.note }}</span>
            <RowActions class="ml-auto shrink-0" @edit="editing = item" @remove="removeItem(item)" />
          </div>
        </div>
      </div>

      <!-- Desktop: table -->
      <div class="hidden sm:block bg-white rounded-2xl card-shadow overflow-x-auto">
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
              <th class="px-2 py-3 font-medium text-center">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in paginated" :key="item.id" class="border-b last:border-0 hover:bg-gray-50">
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
              <td class="px-2 py-3">
                <RowActions class="justify-center" @edit="editing = item" @remove="removeItem(item)" />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <template v-if="pageCount > 1" #bottom>
      <PaginationBar v-model:page="page" :page-count="pageCount" class="mx-auto" />
    </template>

    <FabButton @click="showAdd = true" />
    <GiftMoneyFormModal v-if="showAdd || editing" :existing="editing" @close="closeModal" @saved="closeModal" />
  </PageShell>
</template>
