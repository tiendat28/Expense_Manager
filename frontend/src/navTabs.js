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
