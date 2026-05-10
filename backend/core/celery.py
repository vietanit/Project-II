import os
from celery import Celery

# Thiết lập module settings mặc định cho Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Đọc cấu hình từ settings.py của Django, các biến Celery bắt đầu bằng 'CELERY_'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tự động tìm kiếm các file tasks.py trong các app (như app 'api' của bạn)
app.autodiscover_tasks()