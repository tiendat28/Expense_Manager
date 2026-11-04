<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { navTabs as tabs, isTabActive } from '../navTabs'
import { useAuthStore } from '../stores/auth'
import { useSidebar } from '../composables/useSidebar'
import { useTransactionsStore } from '../stores/transactions'
import { useDebtsStore } from '../stores/debts'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const sidebar = useSidebar()
const txStore = useTransactionsStore()
const debtsStore = useDebtsStore()

const userInitials = computed(() => {
  const name = auth.user?.name || auth.user?.email || 'User'
  const parts = name.trim().split(/\s+/)
  if (parts.length >= 2) {
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
  }
  return name.slice(0, 2).toUpperCase()
})

const badgeCount = (tabName) => {
  if (tabName === 'transactions') {
    return txStore.items.length ? `${txStore.items.length}` : null
  }
  if (tabName === 'debts') {
    const unsettled = debtsStore.unsettledList.length
    return unsettled > 0 ? `${unsettled} cần theo dõi` : null
  }
  return null
}

function handleNav(tabName) {
  sidebar.close()
  router.push({ name: tabName })
}

function logout() {
  auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <!-- Mobile Backdrop -->
  <div
    v-if="sidebar.isOpen.value"
    class="fixed inset-0 bg-slate-900/60 backdrop-blur-xs z-40 lg:hidden"
    @click="sidebar.close"
  ></div>

  <!-- Sidebar -->
  <aside
    :class="[
      'fixed inset-y-0 left-0 z-50 w-72 bg-white dark:bg-slate-900 border-r border-slate-200/80 dark:border-slate-800 flex flex-col justify-between transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static',
      sidebar.isOpen.value ? 'translate-x-0' : '-translate-x-full',
    ]"
  >
    <!-- Top Brand & Menu -->
    <div class="flex-1 flex flex-col min-h-0">
      <!-- Brand Header -->
      <div class="h-16 sm:h-20 px-5 sm:px-6 flex items-center justify-between border-b border-slate-100 dark:border-slate-800/80 shrink-0">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-600 via-emerald-500 to-green-500 flex items-center justify-center text-white shadow-lg shadow-emerald-500/30">
            <i class="fa-solid fa-chart-pie text-lg"></i>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="font-display font-extrabold text-xl tracking-tight bg-gradient-to-r from-emerald-600 to-green-500 bg-clip-text text-transparent">FiveDream</span>
              <span class="text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400 border border-emerald-200/60 dark:border-emerald-800">PRO</span>
            </div>
            <p class="text-xs text-slate-400 dark:text-slate-500">Quản trị tài chính cá nhân</p>
          </div>
        </div>
        <button
          @click="sidebar.close"
          class="lg:hidden text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1.5 rounded-lg"
          aria-label="Đóng menu"
        >
          <i class="fa-solid fa-xmark text-lg"></i>
        </button>
      </div>

      <!-- Navigation Menu -->
      <div class="p-4 space-y-1.5 overflow-y-auto flex-1">
        <p class="px-3 text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-2">Phân hệ quản lý</p>

        <button
          v-for="tab in tabs"
          :key="tab.name"
          @click="handleNav(tab.name)"
          class="w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm transition-all cursor-pointer"
          :class="[
            isTabActive(tab.name, route.name)
              ? 'font-semibold bg-emerald-600 text-white shadow-md shadow-emerald-600/25'
              : 'font-medium text-slate-600 dark:text-slate-400 hover:bg-emerald-50/70 hover:text-emerald-700 dark:hover:bg-slate-800/70 dark:hover:text-emerald-400',
          ]"
        >
          <div class="flex items-center gap-3">
            <i :class="[tab.icon, 'w-5 text-center text-sm']"></i>
            <span>{{ tab.label }}</span>
          </div>
          <span
            v-if="tab.badge || badgeCount(tab.name)"
            class="text-[11px] px-2 py-0.5 rounded-full font-semibold"
            :class="[
              isTabActive(tab.name, route.name)
                ? 'bg-white/20 text-white'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300',
            ]"
          >
            {{ badgeCount(tab.name) || tab.badge }}
          </span>
        </button>

        <div class="pt-2">
          <p class="px-3 text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-2">Hệ thống</p>
          <button
            @click="handleNav('settings')"
            class="w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm transition-all cursor-pointer"
            :class="[
              isTabActive('settings', route.name)
                ? 'font-semibold bg-emerald-600 text-white shadow-md shadow-emerald-600/25'
                : 'font-medium text-slate-600 dark:text-slate-400 hover:bg-emerald-50/70 hover:text-emerald-700 dark:hover:bg-slate-800/70 dark:hover:text-emerald-400',
            ]"
          >
            <div class="flex items-center gap-3">
              <i class="fa-solid fa-gear w-5 text-center text-sm"></i>
              <span>Cài đặt & Sao lưu</span>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Bottom Health Box & User Profile -->
    <div class="p-4 border-t border-slate-200/80 dark:border-slate-800 space-y-3 shrink-0">
      <div class="p-3.5 rounded-2xl bg-gradient-to-br from-slate-900 via-emerald-950 to-slate-900 text-white shadow-lg relative overflow-hidden">
        <div class="absolute -right-6 -bottom-6 w-24 h-24 rounded-full bg-emerald-500/20 blur-xl"></div>
        <div class="flex items-center justify-between text-xs text-emerald-200 mb-1">
          <span>Sức khỏe tài chính</span>
          <span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-semibold border border-emerald-400/30">Tốt</span>
        </div>
        <p class="text-xs text-slate-300 leading-relaxed">Quản lý dòng tiền thông minh, cập nhật thời gian thực.</p>
      </div>

      <div class="flex items-center justify-between px-1 pt-1">
        <div class="flex items-center gap-2.5 min-w-0">
          <div class="w-9 h-9 rounded-full bg-gradient-to-tr from-emerald-600 to-green-500 flex items-center justify-center text-white font-bold text-sm shadow-sm shadow-emerald-600/25 shrink-0">
            {{ userInitials }}
          </div>
          <div class="min-w-0">
            <p class="text-xs font-bold text-slate-800 dark:text-slate-100 truncate">{{ auth.user?.name || 'Người dùng' }}</p>
            <p class="text-[11px] text-slate-400 truncate">{{ auth.user?.email || 'VNĐ' }}</p>
          </div>
        </div>
        <button
          @click="logout"
          title="Đăng xuất"
          class="text-xs text-slate-400 hover:text-rose-600 dark:hover:text-rose-400 p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition"
        >
          <i class="fa-solid fa-arrow-right-from-bracket"></i>
        </button>
      </div>
    </div>
  </aside>
</template>
