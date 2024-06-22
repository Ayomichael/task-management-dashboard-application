from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from ..models import User, Task
from ..views import (
    CreateUserView, 
    TaskListCreate, 
    TaskDelete, 
    TaskUpdate, 
    CompletedTasks, 
    OverdueTasks
)
from ..serializers import UserSerializer, TaskSerializer

class TestUserView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {'username': 'testuser','email':'test@email.com', 'password': 'password123'}

    def test_user_creation(self):
        response = self.client.post(reverse('register'), self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(username=self.user_data['username']).username, self.user_data['username'])

class TestTaskViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',email='test@email.com' , password='password123')
        self.client.force_authenticate(user=self.user)
        self.task_data = {'title': 'Test Task', 'description': 'This is a test task'}

    def test_task_list_create(self):
        response = self.client.post(reverse('task-list'), self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, self.task_data['title'])

        response = self.client.get(reverse('task-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_task_update(self):
        task = Task.objects.create(assigned_to=self.user, title='Old Task')
        update_data = {'title': 'Updated Task'}
        url = reverse('task-detail', kwargs={'pk': task.pk})

        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, update_data['title'])

    def test_task_delete(self):
        task = Task.objects.create(assigned_to=self.user, title='Task to Delete')
        url = reverse('task-detail', kwargs={'pk': task.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

class TestCompletedTasks(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',email='test@email.com' , password='password123')
        self.client.force_authenticate(user=self.user)
        self.completed_task = Task.objects.create(assigned_to=self.user, title='Completed Task', status='Completed')
        self.in_progress_task = Task.objects.create(assigned_to=self.user, title='In Progress Task', status='In Progress')

    def test_completed_tasks_list(self):
        url = reverse('completed-tasks')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.completed_task.title)

class TestOverdueTasks(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User
