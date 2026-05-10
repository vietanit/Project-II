from django.contrib import admin
from .models import Problem, Submission
from .tasks import judge_submission_task  # Import Celery task thay vì engine

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_limit', 'memory_limit')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'problem', 'language', 'status', 'created_at')
    actions = ['rejudge_submissions']

    @admin.action(description='Chấm lại các bài đã chọn (Ngầm)')
    def rejudge_submissions(self, request, queryset):
        for sub in queryset:
            sub.status = "Pending"
            sub.save()
            # Đẩy lại vào hàng đợi Celery
            judge_submission_task.delay(sub.id)