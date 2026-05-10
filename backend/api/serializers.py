from rest_framework import serializers
from .models import Problem, Submission
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    # Hiển thị tên user và tiêu đề bài tập thay vì chỉ hiện ID
    user = UserSerializer(read_only=True)
    problem_title = serializers.CharField(source='problem.title', read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'user', 'problem', 'problem_title', 'code', 'status', 'created_at']