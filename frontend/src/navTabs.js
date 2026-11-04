export const primaryTabs = [
  { name: 'dashboard', label: 'Tổng quan', icon: 'fa-solid fa-shapes', badge: 'Live' },
  { name: 'transactions', label: 'Sổ giao dịch', icon: 'fa-solid fa-arrow-right-arrow-left' },
  { name: 'debts', label: 'Sổ nợ', icon: 'fa-solid fa-handshake-simple' },
]

export const moreTabs = [
  { name: 'savings', label: 'Tiết kiệm & Tích lũy', icon: 'fa-solid fa-piggy-bank' },
  { name: 'giftmoney', label: 'Tiền mừng', icon: 'fa-solid fa-gift', badge: 'Đặc thù' },
  { name: 'bills', label: 'Hóa đơn & Định kỳ', icon: 'fa-solid fa-file-invoice-dollar' },
  { name: 'budget', label: 'Ngân sách chi tiêu', icon: 'fa-solid fa-sliders' },
]

export const settingsTab = { name: 'settings', label: 'Cài đặt & Sao lưu', icon: 'fa-solid fa-gear' }

export const navTabs = [...primaryTabs, ...moreTabs]

const CHILD_ROUTES = {
  savings: ['savings-detail'],
  debts: ['debt-detail'],
}

export function isTabActive(tabName, routeName) {
  return routeName === tabName || (CHILD_ROUTES[tabName] || []).includes(routeName)
}
