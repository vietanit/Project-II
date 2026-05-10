# Sử dụng Python bản nhẹ
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    docker.io \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các thư viện Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Chạy server Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]