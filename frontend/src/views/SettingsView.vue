<script setup>
import { ref } from 'vue'
import client from '../api/client'
import PageShell from '../components/PageShell.vue'

const importMessage = ref('')

async function exportBackup() {
  const { data } = await client.get('/backup/export')
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `backup_chitieu_${Date.now()}.json`
  a.click()
  URL.revokeObjectURL(url)
}

async function importBackup(e) {
  const file = e.target.files[0]
  if (!file) return
  let data
  try {
    data = JSON.parse(await file.text())
  } catch {
    importMessage.value = 'File không hợp lệ.'
    return
  }
  try {
    await client.post('/backup/import', data)
    importMessage.value = 'Đã khôi phục dữ liệu thành công.'
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
  const url = URL.createObjectURL(response.data)
  const a = document.createElement('a')
  a.href = url
  a.download = 'giao_dich.csv'
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<template>
  <PageShell>
    <div class="bg-white rounded-2xl p-5 shadow-sm space-y-2">
      <h2 class="font-semibold">Sao lưu dữ liệu</h2>
      <button @click="exportBackup" class="w-full border rounded-lg py-2 text-sm">Xuất file backup (.json)</button>
      <label class="w-full border rounded-lg py-2 text-sm block text-center cursor-pointer">
        Nhập từ file backup
        <input type="file" accept=".json" class="hidden" @change="importBackup" />
      </label>
      <p v-if="importMessage" class="text-xs text-gray-900">{{ importMessage }}</p>
    </div>

    <div class="bg-white rounded-2xl p-5 shadow-sm space-y-2">
      <h2 class="font-semibold">Xuất báo cáo Excel</h2>
      <button @click="exportCSV" class="w-full border rounded-lg py-2 text-sm">Xuất file Excel (.csv) — tháng này</button>
      <p class="text-xs text-gray-900">File .csv mở trực tiếp được bằng Excel, Numbers, Google Sheets.</p>
    </div>
  </PageShell>
</template>
