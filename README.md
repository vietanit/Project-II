# HustJudge - Project II (SOICT - HUST)

Hệ thống chấm bài trực tuyến (Online Judge) hỗ trợ ngôn ngữ C++.

## Công nghệ sử dụng:
Backend: Django, Django Rest Framework.
Database: PostgreSQL.
Environment: Docker & Docker Compose.
Compiler: g++ (GNU Compiler Collection).

## Trạng thái dự án:
Cấu hình môi trường Docker chuẩn cho chấm bài.
Thiết kế Database (Problems, Submissions).
Hoàn thiện Judge Engine (Compile & Execute C++ code).
Giao diện quản trị Admin để quản lý bài tập.

## Cách chạy:
1. Cài đặt Docker & Docker Compose.
2. Chạy lệnh: `docker-compose up --build`.
3. Truy cập: `http://localhost:8000/admin`.
