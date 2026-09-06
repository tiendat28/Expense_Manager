export const primaryTabs = [
  { name: 'dashboard', label: 'Tổng quan', icon: '📊' },
  { name: 'transactions', label: 'Giao dịch', icon: '💳' },
  { name: 'savings', label: 'Tiết kiệm', icon: '🎯' },
  { name: 'debts', label: 'Sổ nợ', icon: '🤝' },
  { name: 'giftmoney', label: 'Tiền mừng', icon: '🎁' },
]

export const moreTabs = [
  { name: 'bills', label: 'Hóa đơn', icon: '🧾' },
  { name: 'budget', label: 'Ngân sách', icon: '🧮' },
]

export const settingsTab = { name: 'settings', label: 'Cài đặt', icon: '⚙️' }

export const navTabs = [...primaryTabs, ...moreTabs]
