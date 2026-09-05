export function formatVND(value) {
  const n = Math.round(Number(value) || 0)
  return n.toLocaleString('vi-VN') + ' đ'
}

export function shortVND(value) {
  const n = Number(value) || 0
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'tr'
  if (n >= 1_000) return Math.round(n / 1_000) + 'k'
  return String(Math.round(n))
}

export const EXPENSE_CATEGORIES = [
  { value: 'Ăn uống', icon: '🍽️', color: '#f97316' },
  { value: 'Di chuyển', icon: '🚗', color: '#3b82f6' },
  { value: 'Nhà ở', icon: '🏠', color: '#a855f7' },
  { value: 'Mua sắm', icon: '🛍️', color: '#ec4899' },
  { value: 'Giải trí', icon: '🎮', color: '#22c55e' },
  { value: 'Hóa đơn', icon: '🧾', color: '#ef4444' },
  { value: 'Sức khỏe', icon: '💊', color: '#14b8a6' },
  { value: 'Khác', icon: '➖', color: '#6b7280' },
]

export const INCOME_CATEGORIES = [
  { value: 'Lương', icon: '💰', color: '#22c55e' },
  { value: 'Thưởng', icon: '🎁', color: '#eab308' },
  { value: 'Đầu tư', icon: '📈', color: '#3b82f6' },
  { value: 'Được cho/tặng', icon: '❤️', color: '#ec4899' },
  { value: 'Bán đồ', icon: '🏷️', color: '#f97316' },
  { value: 'Khác', icon: '➖', color: '#6b7280' },
]

export function categoryMeta(category, type) {
  const list = type === 'income' ? INCOME_CATEGORIES : EXPENSE_CATEGORIES
  return list.find((c) => c.value === category) || { icon: '❓', color: '#6b7280' }
}
