# Taixiu Android (Kivy) — Package for GitHub Actions build

Gói này chứa toàn bộ mã nguồn để bạn upload lên GitHub và tự động build `.apk` bằng GitHub Actions.

## File có trong gói
- `main.py` — Kivy GUI; requires Kivy to run locally.
- `backend.py` — Headless backend (RootModel) — logic, persistence, Markov prediction.
- `tai_xiu.kv` — giao diện Kivy.
- `buildozer.spec` — cấu hình buildozer.
- `.github/workflows/build-apk.yml` — workflow GitHub Actions để build file `.apk`.
- `tests/` — chứa unit tests cho backend.
- `images/` — hướng dẫn bước bằng ảnh minh họa.
- `README.md` — (bạn đang đọc).

---

## Hướng dẫn chi tiết (bằng ảnh, làm theo từng bước)

### 1) Tạo repository trên GitHub
- Vào github.com → **New repository**.
- Đặt tên (ví dụ `tai-xiu-app`) và bấm **Create repository**.

Xem ảnh: `images/step1_create_repo.png`

### 2) Upload toàn bộ file trong gói này lên repository
- Tải lên qua web (Add files → Upload files) hoặc clone repo và `git push` từ máy bạn.
- Đảm bảo `main.py`, `backend.py`, `tai_xiu.kv`, `buildozer.spec` và thư mục `.github/workflows` có trong repository.

Xem ảnh: `images/step2_upload_files.png`

### 3) Push lên branch `main`
- Nếu bạn đẩy lên `main`, workflow sẽ tự chạy. Nếu dùng branch khác, chỉnh `build-apk.yml`.
- Kịch bản đơn giản:
```bash
git init
git add .
git commit -m "Initial commit: Taixiu app"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo>.git
git push -u origin main
```

Xem ảnh: `images/step3_push_main.png`

### 4) Chờ GitHub Actions build
- Vào tab **Actions** trong repository, chọn workflow `Build Android APK`.
- Chờ quá trình build chạy (có thể mất 10–30 phút lần đầu).

Xem ảnh: `images/step4_actions.png`

### 5) Tải file `.apk`
- Sau khi workflow chạy xong, kéo xuống phần **Artifacts** → tải file `.apk`.
- Cài file `.apk` lên điện thoại Android (bật cài đặt từ nguồn không xác định).

Xem ảnh: `images/step5_download.png`

---

## Chạy app cục bộ (desktop) — cần Kivy
1. Cài Python 3.10+.
2. Cài Kivy:
```bash
python -m pip install --upgrade pip setuptools wheel
pip install "kivy[base]" kivy_examples
```
3. Chạy:
```bash
python main.py
```

---

## Muốn mình build giúp?
Nếu bạn muốn, mình có thể:
- Hướng dẫn kỹ hơn từng bước upload (mình sẽ kèm ảnh chụp màn hình từng thao tác).
- Nếu bạn tạm thời đưa quyền repo hoặc thêm mình làm collaborator (không cần, bạn có thể tự làm), mình có thể kiểm tra workflow và file APK.

---

## Ghi chú kỹ thuật
- Workflow trong `.github/workflows/build-apk.yml` sử dụng `buildozer -v android debug`. Tùy môi trường GitHub Actions, bạn có thể cần bổ sung vài package hệ thống (nếu build thất bại, mình sẽ giúp điều chỉnh workflow).
- Nếu bạn muốn tối ưu build (keepsigned, release, etc.) mình sẽ hướng dẫn cấu hình thêm.
