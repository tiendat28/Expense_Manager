// Các input <input type="date"> / <input type="datetime-local"> nhận GIỜ ĐỊA PHƯƠNG.
// Dùng toISOString() sẽ ra giờ UTC — ở VN (UTC+7) sẽ lệch 7 tiếng, và trong khoảng
// 00:00–07:00 còn ra nhầm sang ngày hôm trước. Nên phải tự ghép theo giờ máy.
function pad(n) {
  return String(n).padStart(2, '0')
}

/** Hôm nay theo giờ địa phương, dạng YYYY-MM-DD (cho <input type="date">). */
export function todayISO(d = new Date()) {
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}

/** Bây giờ theo giờ địa phương, dạng YYYY-MM-DDTHH:mm (cho <input type="datetime-local">). */
export function nowISO(d = new Date()) {
  return `${todayISO(d)}T${pad(d.getHours())}:${pad(d.getMinutes())}`
}

/** Hiển thị ngày giờ cho người đọc. */
export function formatDateTime(value) {
  return new Date(value).toLocaleString('vi-VN')
}

// Cột giờ trong DB là timestamptz (mốc tuyệt đối). <input type="datetime-local"> lại làm việc
// bằng giờ máy và không kèm múi giờ, nên phải đổi qua lại rõ ràng ở hai đầu — nếu gửi thẳng
// chuỗi của input lên thì Postgres (TZ=UTC) sẽ hiểu nhầm đó là giờ UTC và lệch đúng 7 tiếng.

/** Mốc thời gian từ API -> chuỗi giờ máy cho <input type="datetime-local">. */
export function toLocalInput(value) {
  return nowISO(new Date(value))
}

/** Giá trị <input type="datetime-local"> (giờ máy) -> mốc tuyệt đối để gửi lên API. */
export function fromLocalInput(value) {
  return new Date(value).toISOString()
}
