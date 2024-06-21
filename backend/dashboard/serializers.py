from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id","title", "description", "status", "priority", "due_date","category","assigned_to"]
        extra_kwargs = {"assigned_to": {"read_only": True}}