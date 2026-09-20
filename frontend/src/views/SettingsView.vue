<script setup>
import { ref } from 'vue'
import client from '../api/client'
import { useConfirmStore } from '../stores/confirm'
import { downloadBlob } from '../utils/download'
import PageShell from '../components/PageShell.vue'
import PageTitle from '../components/PageTitle.vue'

const confirm = useConfirmStore()
const importMessage = ref('')

/** Tải toàn bộ dữ liệu hiện tại về máy dưới dạng file .json. */
async function exportBackup() {
  const { data } = await client.get('/backup/export')
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  downloadBlob(blob, `backup_chitieu_${Date.now()}.json`)
}

async function importBackup(e) {
  const file = e.target.files[0]
  // Xóa lựa chọn để lần sau chọn lại đúng file đó vẫn kích hoạt được
  e.target.value = ''
  if (!file) return

  importMessage.value = ''
  let data
  try {
    data = JSON.parse(await file.text())
  } catch {
    importMessage.value = 'File không hợp lệ.'
    return
  }

  const ok = await confirm.ask({
    title: 'Khôi phục từ file backup',
    message:
      'Toàn bộ dữ liệu hiện tại (giao dịch, khoản nợ, tiết kiệm, hóa đơn, ngân sách, tiền mừng) ' +
      'sẽ bị xóa và thay bằng nội dung file. Không hoàn tác được. ' +
      'Máy sẽ tự tải một file backup của dữ liệu hiện tại trước khi ghi đè.',
    confirmText: 'Khôi phục',
  })
  if (!ok) return

  // Lưu lại dữ liệu cũ trước khi ghi đè — thao tác import không hoàn tác được.
  try {
    await exportBackup()
  } catch {
    importMessage.value = 'Không tải được bản sao lưu dự phòng nên đã dừng, chưa thay đổi gì.'
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
  downloadBlob(response.data, 'giao_dich.csv')
}
</script>

<template>
  <PageShell>
    <template #sticky>
      <PageTitle text="Cài đặt" />
    </template>

    <div class="bg-white rounded-2xl p-5 card-shadow space-y-2">
      <h2 class="font-semibold">Sao lưu dữ liệu</h2>
      <button @click="exportBackup" class="w-full border rounded-lg py-2 text-sm">Xuất file backup (.json)</button>
      <label class="w-full border rounded-lg py-2 text-sm block text-center cursor-pointer">
        Nhập từ file backup
        <input type="file" accept=".json" class="hidden" @change="importBackup" />
      </label>
      <p class="text-xs text-gray-900">
        Khôi phục sẽ <span class="text-red-600 font-medium">xóa hết dữ liệu hiện tại</span> rồi thay bằng nội dung file.
        Bạn sẽ được hỏi lại, và máy tự tải bản sao lưu dự phòng trước khi ghi đè.
      </p>
      <p v-if="importMessage" class="text-xs text-gray-900">{{ importMessage }}</p>
    </div>

    <div class="bg-white rounded-2xl p-5 card-shadow space-y-2">
      <h2 class="font-semibold">Xuất báo cáo Excel</h2>
      <button @click="exportCSV" class="w-full border rounded-lg py-2 text-sm">Xuất file Excel (.csv) — tháng này</button>
      <p class="text-xs text-gray-900">File .csv mở trực tiếp được bằng Excel, Numbers, Google Sheets.</p>
    </div>
  </PageShell>
</template>
