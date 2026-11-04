<script setup>
import { ref } from 'vue'
import client from '../api/client'
import { useConfirmStore } from '../stores/confirm'
import { downloadBlob } from '../utils/download'
import PageShell from '../components/PageShell.vue'

const confirm = useConfirmStore()
const importMessage = ref('')

async function exportBackup() {
  const { data } = await client.get('/backup/export')
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  downloadBlob(blob, `backup_fivedream_${Date.now()}.json`)
}

async function importBackup(e) {
  const file = e.target.files[0]
  e.target.value = ''
  if (!file) return

  importMessage.value = ''
  let data
  try {
    data = JSON.parse(await file.text())
  } catch {
    importMessage.value = 'File không hợp lệ hoặc sai định dạng JSON.'
    return
  }

  const ok = await confirm.ask({
    title: 'Khôi phục từ file backup',
    message:
      'Toàn bộ dữ liệu hiện tại (giao dịch, khoản nợ, tiết kiệm, hóa đơn, ngân sách, tiền mừng) ' +
      'sẽ bị xóa và thay bằng nội dung file. Không thể hoàn tác. ' +
      'Hệ thống sẽ tự tải một file backup của dữ liệu hiện tại trước khi ghi đè.',
    confirmText: 'Khôi phục ngay',
  })
  if (!ok) return

  try {
    await exportBackup()
  } catch {
    importMessage.value = 'Không tải được bản sao lưu dự phòng nên đã dừng, chưa thay đổi gì.'
    return
  }

  try {
    await client.post('/backup/import', data)
    importMessage.value = 'Đã khôi phục dữ liệu thành công!'
  } catch (err) {
    importMessage.value = err.response?.data?.detail || 'Import thất bại, vui lòng thử lại.'
  }
}

async function exportCSV() {
  const now = new Date()
  const response = await client.get('/backup/export-csv', {
    params: { scope: 'month', year: now.getFullYear(), month: now.getMonth() + 1 },
    responseType: 'blob',
  })
  downloadBlob(response.data, `fivedream_giaodich_${now.getFullYear()}_${now.getMonth() + 1}.csv`)
}
</script>

<template>
  <PageShell>
    <div class="max-w-3xl mx-auto space-y-6">
      <!-- Card 1: Sao lưu & Khôi phục -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/90 dark:border-slate-800 p-6 sm:p-7 card-shadow space-y-4 transition-colors">
        <div class="flex items-center gap-3 pb-3 border-b border-slate-100 dark:border-slate-800">
          <div class="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400 flex items-center justify-center text-lg">
            <i class="fa-solid fa-cloud-arrow-down"></i>
          </div>
          <div>
            <h2 class="font-display font-bold text-base text-slate-900 dark:text-white">Sao lưu & Khôi phục dữ liệu</h2>
            <p class="text-xs text-slate-400">Toàn bộ dữ liệu tài chính của bạn được đóng gói an toàn</p>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
          <button
            @click="exportBackup"
            class="py-3 px-4 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 font-semibold text-xs text-slate-700 dark:text-slate-200 transition flex items-center justify-center gap-2 cursor-pointer"
          >
            <i class="fa-solid fa-file-arrow-down text-emerald-600 dark:text-emerald-400"></i>
            <span>Xuất file backup (.json)</span>
          </button>

          <label class="py-3 px-4 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 font-semibold text-xs text-slate-700 dark:text-slate-200 transition flex items-center justify-center gap-2 cursor-pointer">
            <i class="fa-solid fa-file-arrow-up text-emerald-500"></i>
            <span>Nhập từ file backup</span>
            <input type="file" accept=".json" class="hidden" @change="importBackup" />
          </label>
        </div>

        <p class="text-[11px] text-slate-400 leading-relaxed bg-slate-50 dark:bg-slate-800/40 p-3 rounded-xl border border-slate-100 dark:border-slate-800">
          <i class="fa-solid fa-shield-halved text-emerald-600 dark:text-emerald-400 mr-1"></i>
          Khi khôi phục, hệ thống sẽ tự động tải trước một file dự phòng của dữ liệu hiện tại để đảm bảo an toàn tuyệt đối.
        </p>

        <p v-if="importMessage" class="text-xs font-semibold" :class="importMessage.includes('thành công') ? 'text-emerald-600' : 'text-rose-600'">
          {{ importMessage }}
        </p>
      </div>

      <!-- Card 2: Xuất báo cáo Excel -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/90 dark:border-slate-800 p-6 sm:p-7 card-shadow space-y-4 transition-colors">
        <div class="flex items-center gap-3 pb-3 border-b border-slate-100 dark:border-slate-800">
          <div class="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400 flex items-center justify-center text-lg">
            <i class="fa-solid fa-file-excel"></i>
          </div>
          <div>
            <h2 class="font-display font-bold text-base text-slate-900 dark:text-white">Xuất báo cáo Excel (.CSV)</h2>
            <p class="text-xs text-slate-400">Xuất dữ liệu giao dịch mở trực tiếp bằng Microsoft Excel, Google Sheets</p>
          </div>
        </div>

        <button
          @click="exportCSV"
          class="w-full py-3 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-700 font-semibold text-xs text-white transition flex items-center justify-center gap-2 cursor-pointer shadow-sm shadow-emerald-600/20"
        >
          <i class="fa-solid fa-download"></i>
          <span>Tải file Excel giao dịch tháng hiện tại</span>
        </button>
      </div>
    </div>
  </PageShell>
</template>
