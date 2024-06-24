from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework import generics
from .serializers import UserSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Task
from datetime import date
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken


# class CreateUserView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]

@method_decorator(csrf_exempt, name='dispatch')
class CreateUserView(View):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not (username and email and password):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        return JsonResponse({'message': 'User created successfully'}, status=201)   


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        username = data.get('username')
        password = data.get('password')
        
        if not (username and password):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    
    @api_view(['POST'])
    def login(request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=400)
        
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
