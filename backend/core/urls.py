from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ProblemViewSet, SubmissionViewSet

router = DefaultRouter()
router.register(r'problems', ProblemViewSet)
router.register(r'submissions', SubmissionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), # Các API sẽ bắt đầu bằng /api/
]