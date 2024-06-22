from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Task
from datetime import date


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class TaskListCreate(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Base queryset for all tasks assigned to the user
        queryset = Task.objects.filter(assigned_to=user)

        # Filter by status based on the request parameter 'status'
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(assigned_to=self.request.user)
        else:
            print(serializer.errors)

class TaskDelete(generics.DestroyAPIView):
    serializer_class=TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assigned_to=user)

class TaskUpdate(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assigned_to=user)

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)


class CompletedTasks(TaskListCreate):
#   View to retrieve completed tasks for the authenticated user.
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()  # Call base get_queryset for user filtering
        return queryset.filter(status='Completed')  # Override to filter for completed tasks

class OverdueTasks(TaskListCreate):

    # View to retrieve overdue tasks for the authenticated user.
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()  # Call base get_queryset for user filtering
        # Implement logic to filter overdue tasks based on your definition of overdue
        # This example assumes a 'due_date' field on the Task model
        today = date.today()
        return queryset.filter(status='In Progress', due_date__lt=today).exclude(due_date=None)
