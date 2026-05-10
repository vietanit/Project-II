# api/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Problem, Submission
from .serializers import ProblemSerializer, SubmissionSerializer
from .tasks import judge_submission_task  # <--- Import task thay vì run_judge

class ProblemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all().order_by('-created_at')
    serializer_class = SubmissionSerializer

    def create(self, request, *args, **kwargs):
        problem_id = request.data.get('problem')
        code = request.data.get('code')
        
        # Tạm thời gán cho user đầu tiên (admin)
        from django.contrib.auth.models import User
        user = User.objects.first() 
        problem = Problem.objects.get(id=problem_id)
        
        # 1. Lưu bản nộp vào Database với trạng thái Pending
        submission = Submission.objects.create(
            user=user,
            problem=problem,
            code=code,
            status="Pending"
        )

        # 2. Đẩy nhiệm vụ vào hàng đợi Celery (Bất đồng bộ)
        # Hàm .delay() là cách gọi task ngầm của Celery
        judge_submission_task.delay(submission.id)

        # 3. Trả về thông tin bản nộp ngay lập tức cho Frontend
        serializer = self.get_serializer(submission)
        return Response(serializer.data, status=status.HTTP_201_CREATED)