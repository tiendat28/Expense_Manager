import { useConfirmStore } from '../stores/confirm'
import { useToastStore } from '../stores/toast'

/**
 * Hỏi xác nhận trước khi xóa, xóa xong thì báo toast.
 * Trả về true nếu đã xóa, false nếu người dùng bấm Hủy.
 *
 *   const confirmDelete = useConfirmDelete()
 *   await confirmDelete(`Bạn có chắc chắn muốn xóa giao dịch "${t.note}"?`, () => tx.remove(t.id))
 */
export function useConfirmDelete() {
  const confirm = useConfirmStore()
  const toast = useToastStore()

  return async function confirmDelete(message, remove) {
    const ok = await confirm.ask({ message })
    if (!ok) return false
    await remove()
    toast.show('Xóa thành công')
    return true
  }
}
