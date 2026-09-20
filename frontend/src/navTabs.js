export const primaryTabs = [
  { name: 'dashboard', label: 'Tổng quan', icon: '📊' },
  { name: 'transactions', label: 'Giao dịch', icon: '💳' },
  { name: 'debts', label: 'Sổ nợ', icon: '🤝' },
]

export const moreTabs = [
  { name: 'savings', label: 'Tiết kiệm', icon: '🎯' },
  { name: 'giftmoney', label: 'Tiền mừng', icon: '🎁' },
  { name: 'bills', label: 'Hóa đơn', icon: '🧾' },
  { name: 'budget', label: 'Ngân sách', icon: '🧮' },
]

export const settingsTab = { name: 'settings', label: 'Cài đặt', icon: '⚙️' }

export const navTabs = [...primaryTabs, ...moreTabs]

// Trang chi tiết vẫn phải làm sáng tab cha của nó trên sidebar và thanh điều hướng.
const CHILD_ROUTES = {
  savings: ['savings-detail'],
  debts: ['debt-detail'],
}

export function isTabActive(tabName, routeName) {
  return routeName === tabName || (CHILD_ROUTES[tabName] || []).includes(routeName)
}
