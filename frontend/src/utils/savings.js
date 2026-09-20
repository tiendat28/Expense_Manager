/** Tổng số tiền đã nạp cho một mục tiêu tiết kiệm. */
export function savedAmount(goal) {
  return (goal.contributions || []).reduce((sum, c) => sum + Number(c.amount), 0)
}
