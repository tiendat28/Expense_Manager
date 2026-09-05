# Quản lý chi tiêu (Expense Tracker)

Ứng dụng web quản lý chi tiêu cá nhân: theo dõi giao dịch, ngân sách theo danh mục, hóa đơn định kỳ, khoản nợ và mục tiêu tiết kiệm.

## Công nghệ sử dụng

- **Backend**: FastAPI + SQLAlchemy + Alembic, xác thực JWT, Postgres
- **Frontend**: Vue 3 + Vite + Pinia + Tailwind CSS + ApexCharts
- **Hạ tầng**: Docker Compose (Postgres, backend, frontend)

## Cấu trúc project

```
webapp/
├── backend/            FastAPI + SQLAlchemy + Alembic (Postgres)
│   ├── app/
│   │   ├── core/        cấu hình, bảo mật, JWT
│   │   ├── models/       model SQLAlchemy
│   │   ├── routers/      endpoint API (auth, transactions, budgets, bills, debts, savings, backup)
│   │   ├── schemas/      schema Pydantic
│   │   └── services/     logic nghiệp vụ
│   └── alembic/          migration database
├── frontend/            Vue 3 + Tailwind + Pinia + ApexCharts
│   └── src/
│       ├── api/          client gọi API (axios)
│       ├── components/   component dùng lại (form, chart, modal...)
│       ├── stores/        Pinia store (auth, transactions, budget, bills, debts, savings)
│       └── views/         các trang (Dashboard, Transactions, Bills, Debts, Savings, Settings...)
└── docker-compose.yml
```

## Tính năng chính

- Đăng ký / đăng nhập, xác thực bằng JWT
- Ghi nhận và theo dõi giao dịch thu chi
- Ngân sách theo danh mục
- Hóa đơn định kỳ (bills)
- Quản lý khoản nợ và lịch trả nợ
- Mục tiêu tiết kiệm
- Biểu đồ xu hướng chi tiêu theo tháng (ApexCharts)
- Sao lưu dữ liệu (backup)

## Chạy dự án

### Cách 1: Docker (khuyên dùng)

Yêu cầu **Docker Desktop** đã cài và đang chạy.

```bash
cd webapp
cp backend/.env.example backend/.env
```

Mở `backend/.env`, đổi `SECRET_KEY` thành một chuỗi ngẫu nhiên dài (dùng để ký JWT — không dùng giá trị mẫu khi chạy thật).

```bash
docker compose up --build
```

Lần đầu chạy, mở terminal khác để tạo bảng trong Postgres:

```bash
docker compose exec backend alembic upgrade head
```

Truy cập:
- Frontend: http://localhost:5173
- API docs (Swagger): http://localhost:8000/docs

Vào http://localhost:5173/register để tạo tài khoản đầu tiên.

Dừng dự án: `docker compose down` (thêm `-v` nếu muốn xóa luôn dữ liệu Postgres).

### Cách 2: Chạy trực tiếp (không dùng Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # sửa DATABASE_URL trỏ tới Postgres của m
alembic upgrade head
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Biến môi trường

| Nơi | Biến | Ý nghĩa |
|---|---|---|
| backend/.env | `DATABASE_URL` | Chuỗi kết nối Postgres |
| backend/.env | `SECRET_KEY` | Khóa ký JWT — giữ bí mật, đổi khi deploy thật |
| backend/.env | `CORS_ORIGINS` | Domain frontend được phép gọi API (cách nhau bởi dấu phẩy) |
| frontend/.env | `VITE_API_URL` | URL gốc của backend API (mặc định `http://localhost:8000`) |

## Deploy production

Lưu ý quan trọng: **Vercel chỉ phù hợp để host phần frontend** (Vue build ra file tĩnh). Backend FastAPI cần giữ kết nối liên tục tới Postgres — không hợp với mô hình serverless của Vercel. Nên tách:

- **Frontend** → Vercel
- **Backend + Postgres** → Railway (dễ nhất, có free tier) hoặc Render/Fly.io

### Deploy backend + Postgres lên Railway

1. Tạo tài khoản tại https://railway.app, tạo **New Project**
2. **Add a Service → Database → PostgreSQL** — Railway tự tạo và cung cấp biến `DATABASE_URL`
3. **Add a Service → GitHub Repo** (đẩy code lên GitHub trước), chọn thư mục `backend` làm root
4. Vào tab **Variables** của service backend, thêm:
   - `DATABASE_URL` = copy từ service Postgres (dạng `postgresql://...`)
   - `SECRET_KEY` = chuỗi ngẫu nhiên dài
   - `ACCESS_TOKEN_EXPIRE_MINUTES` = `10080`
   - `CORS_ORIGINS` = domain Vercel của frontend (thêm vào sau khi deploy xong bước sau), ví dụ `https://ten-app.vercel.app`
5. Railway tự build bằng `backend/Dockerfile` đã có sẵn
6. Sau khi deploy xong, mở tab **Shell** của service, chạy: `alembic upgrade head`
7. Copy domain public Railway cấp cho backend (dạng `https://xxx.up.railway.app`) — sẽ dùng ở bước sau

### Deploy frontend lên Vercel

1. Đẩy code lên GitHub (nếu chưa)
2. Vào https://vercel.com → **Add New Project** → chọn repo, đặt **Root Directory** = `frontend`
3. Vercel tự nhận diện là project Vite — không cần chỉnh build command
4. Trong **Environment Variables**, thêm:
   - `VITE_API_URL` = domain backend Railway ở bước trên (ví dụ `https://xxx.up.railway.app`)
5. Bấm **Deploy**

### Nối 2 bên lại

Sau khi có domain Vercel thật (ví dụ `https://chi-tieu.vercel.app`):
1. Quay lại Railway, cập nhật biến `CORS_ORIGINS` = `https://chi-tieu.vercel.app`
2. Redeploy backend (Railway tự redeploy khi đổi biến môi trường)
3. Mở domain Vercel, thử đăng ký tài khoản — nếu lỗi CORS thì kiểm tra lại đúng domain (có `https://`, không có dấu `/` cuối)

## Các lệnh Alembic hay dùng

```bash
# Tạo migration mới sau khi sửa model
alembic revision --autogenerate -m "mo ta thay doi"

# Áp dụng migration mới nhất
alembic upgrade head

# Lùi lại 1 bước
alembic downgrade -1
```

## Sự cố thường gặp

- **CORS error khi gọi API từ frontend**: kiểm tra `CORS_ORIGINS` ở backend đã đúng domain frontend chưa, restart lại backend sau khi sửa.
- **401 liên tục dù vừa đăng nhập**: token hết hạn hoặc `SECRET_KEY` bị đổi sau khi token đã phát hành — đăng nhập lại.
- **Bảng không tồn tại sau khi deploy**: quên chạy `alembic upgrade head` trên môi trường mới.
