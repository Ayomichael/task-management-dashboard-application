from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, TaskSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Task
from datetime import date


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'username': self.user.username})
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # print(f"User created: {user.username}, {user.email}, {user.is_active}") used to debug
        refresh = RefreshToken.for_user(user)
        response_data = {
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

class LoginUserView(CustomTokenObtainPairView):
    
    # API view to handle user login and return JWT tokens.
    pass


class TaskListCreate(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        status = self.request.query_params.get('status')
        queryset = Task.objects.filter(assigned_to=user)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def perform_create(self, serializer):
        serializer.save(assigned_to=self.request.user)

class TaskUpdate(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

class TaskDelete(generics.DestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

class CompletedTasks(generics.ListAPIView):
    serializer_class = TaskSerializer
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(status='Completed',assigned_to=user)

class InProgressTasks(generics.ListAPIView):
    serializer_class = TaskSerializer
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(status='In Progress',assigned_to=user)

class OverdueTasks(generics.ListAPIView):
    serializer_class = TaskSerializer
    def get_queryset(self):
        user = self.request.user
        # today = date.today()
        return Task.objects.filter(status='In Progress', due_date__lt=date.today(),assigned_to=user).exclude(due_date=None)
