export const GIFT_MONEY_TYPES = [
  { value: 'wedding', label: 'Tiền cưới', color: 'bg-pink-100 text-pink-700' },
  { value: 'sick', label: 'Ốm đau', color: 'bg-blue-100 text-blue-700' },
  { value: 'newborn', label: 'Thôi nôi', color: 'bg-amber-100 text-amber-700' },
]

export function giftMoneyTypeMeta(value) {
  return GIFT_MONEY_TYPES.find((t) => t.value === value) || GIFT_MONEY_TYPES[0]
}
