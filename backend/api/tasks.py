# api/tasks.py
from celery import shared_task
from .models import Submission
from judge.engine import run_judge

@shared_task
def judge_submission_task(submission_id):
    """
    Task này sẽ được worker nhặt từ Redis Queue để chạy ngầm.
    Chỉ truyền vào ID (integer) chứ không truyền cả object Submission
    vì Celery cần serialize dữ liệu qua JSON.
    """
    try:
        submission = Submission.objects.get(id=submission_id)
    except Submission.DoesNotExist:
        return "Lỗi: Không tìm thấy bài nộp."

    # Chuyển trạng thái sang Đang chấm
    submission.status = "Judging"
    submission.save()

    # Gọi bộ máy chấm bài (vẫn dùng file engine.py của bạn)
    status_result, details = run_judge(submission)

    # Cập nhật kết quả cuối cùng
    submission.status = status_result
    submission.save()
    
    return f"Đã chấm xong {submission_id}: {status_result}"