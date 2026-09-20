/** Phần trăm hoàn thành, chặn trong khoảng 0–100. Mẫu số <= 0 thì trả 0. */
export function percent(part, whole) {
  if (!whole || whole <= 0) return 0
  return Math.min(Number(part) / Number(whole), 1) * 100
}

/** Phần còn lại, không cho âm. */
export function remaining(total, done) {
  return Math.max(Number(total) - Number(done), 0)
}
