import { ref, computed, watch } from 'vue'

/**
 * Chia danh sách thành từng trang và gắn thêm số thứ tự (stt) liên tục.
 * Tự về trang 1 khi danh sách nguồn đổi, và tự lùi lại khi trang hiện tại vượt quá tổng số trang
 * (ví dụ xóa phần tử cuối cùng của trang cuối).
 */
export function usePagination(source, pageSize = 10) {
  const page = ref(1)

  const pageCount = computed(() => Math.max(1, Math.ceil(source.value.length / pageSize)))

  const paginated = computed(() => {
    const start = (page.value - 1) * pageSize
    return source.value.slice(start, start + pageSize).map((item, i) => ({ ...item, stt: start + i + 1 }))
  })

  watch(pageCount, (count) => {
    if (page.value > count) page.value = count
  })

  function reset() {
    page.value = 1
  }

  return { page, pageCount, paginated, reset }
}
