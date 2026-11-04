export function formatVND(value) {
  const n = Math.round(Number(value) || 0)
  return n.toLocaleString('vi-VN') + ' ₫'
}

export const CATEGORY_MAP = {
  // Khoản chi
  'Ăn uống': { icon: 'fa-utensils', emoji: '🍽️', color: 'amber', hex: '#f97316', label: 'Ăn uống' },
  'Ăn uống & Cafe': { icon: 'fa-utensils', emoji: '🍽️', color: 'amber', hex: '#f97316', label: 'Ăn uống & Cafe' },
  'Di chuyển': { icon: 'fa-car-side', emoji: '🚗', color: 'sky', hex: '#3b82f6', label: 'Di chuyển' },
  'Di chuyển & Xăng xe': { icon: 'fa-car-side', emoji: '🚗', color: 'sky', hex: '#3b82f6', label: 'Di chuyển & Xăng xe' },
  'Nhà ở': { icon: 'fa-house-chimney', emoji: '🏠', color: 'indigo', hex: '#a855f7', label: 'Nhà ở' },
  'Nhà cửa & Tiện ích': { icon: 'fa-house-chimney', emoji: '🏠', color: 'indigo', hex: '#a855f7', label: 'Nhà cửa & Tiện ích' },
  'Mua sắm': { icon: 'fa-bag-shopping', emoji: '🛍️', color: 'purple', hex: '#ec4899', label: 'Mua sắm' },
  'Giải trí': { icon: 'fa-gamepad', emoji: '🎮', color: 'emerald', hex: '#22c55e', label: 'Giải trí' },
  'Giải trí & Thể thao': { icon: 'fa-gamepad', emoji: '🎮', color: 'emerald', hex: '#22c55e', label: 'Giải trí & Thể thao' },
  'Hóa đơn': { icon: 'fa-file-invoice-dollar', emoji: '🧾', color: 'rose', hex: '#eab308', label: 'Hóa đơn' },
  'Sức khỏe': { icon: 'fa-heart-pulse', emoji: '💊', color: 'teal', hex: '#14b8a6', label: 'Sức khỏe' },
  'Hiếu hỉ & Giao tế': { icon: 'fa-envelope-open-text', emoji: '💌', color: 'rose', hex: '#f43f5e', label: 'Hiếu hỉ & Giao tế' },

  // Khoản thu
  'Lương': { icon: 'fa-briefcase', emoji: '💼', color: 'emerald', hex: '#10b981', label: 'Lương' },
  'Lương & Thưởng': { icon: 'fa-briefcase', emoji: '💼', color: 'emerald', hex: '#10b981', label: 'Lương & Thưởng' },
  'Thưởng': { icon: 'fa-gift', emoji: '🎁', color: 'amber', hex: '#f59e0b', label: 'Thưởng' },
  'Đầu tư': { icon: 'fa-chart-line', emoji: '📈', color: 'teal', hex: '#14b8a6', label: 'Đầu tư' },
  'Đầu tư & Cổ tức': { icon: 'fa-chart-line', emoji: '📈', color: 'teal', hex: '#14b8a6', label: 'Đầu tư & Cổ tức' },
  'Được cho/tặng': { icon: 'fa-hand-holding-heart', emoji: '🎀', color: 'pink', hex: '#ec4899', label: 'Được cho/tặng' },
  'Bán đồ': { icon: 'fa-tag', emoji: '🏷️', color: 'orange', hex: '#f97316', label: 'Bán đồ' },
  'Khác': { icon: 'fa-minus', emoji: '➖', color: 'slate', hex: '#64748b', label: 'Khác' },
}

export const EXPENSE_CATEGORIES = [
  { value: 'Ăn uống', icon: 'fa-utensils', emoji: '🍽️', color: '#f97316' },
  { value: 'Di chuyển', icon: 'fa-car-side', emoji: '🚗', color: '#3b82f6' },
  { value: 'Nhà ở', icon: 'fa-house-chimney', emoji: '🏠', color: '#a855f7' },
  { value: 'Mua sắm', icon: 'fa-bag-shopping', emoji: '🛍️', color: '#ec4899' },
  { value: 'Giải trí', icon: 'fa-gamepad', emoji: '🎮', color: '#22c55e' },
  { value: 'Hóa đơn', icon: 'fa-file-invoice-dollar', emoji: '🧾', color: '#eab308' },
  { value: 'Sức khỏe', icon: 'fa-heart-pulse', emoji: '💊', color: '#14b8a6' },
  { value: 'Khác', icon: 'fa-minus', emoji: '➖', color: '#64748b' },
]

export const INCOME_CATEGORIES = [
  { value: 'Lương', icon: 'fa-briefcase', color: '#10b981' },
  { value: 'Thưởng', icon: 'fa-gift', color: '#f59e0b' },
  { value: 'Đầu tư', icon: 'fa-chart-line', color: '#14b8a6' },
  { value: 'Được cho/tặng', icon: 'fa-hand-holding-heart', color: '#ec4899' },
  { value: 'Bán đồ', icon: 'fa-tag', color: '#f97316' },
  { value: 'Khác', icon: 'fa-receipt', color: '#64748b' },
]

export function categoryMeta(category, type) {
  if (CATEGORY_MAP[category]) {
    return CATEGORY_MAP[category]
  }
  const list = type === 'income' ? INCOME_CATEGORIES : EXPENSE_CATEGORIES
  const found = list.find((c) => c.value === category)
  if (found) {
    return { icon: found.icon, color: 'slate', hex: found.color, label: found.value }
  }
  return { icon: 'fa-receipt', color: 'slate', hex: '#64748b', label: category || 'Khác' }
}
