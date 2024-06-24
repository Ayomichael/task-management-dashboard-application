from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Task
from datetime import date, timedelta
import pdb  # Import the pdb module

class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_user_url = reverse('register')  
        self.login_url = reverse('login')  

    def test_create_user(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.create_user_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_user(self):
        User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class TaskTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_user_url = reverse('register')  
        self.login_url = reverse('login')  
        self.task_list_create_url = reverse('task-list')  
        self.completed_tasks_url = reverse('completed-task')  
        self.inprogress_tasks_url = reverse('inprogress-task') 
        self.overdue_tasks_url = reverse('overdue-task')  

        
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.create_user_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, f"Failed to create user: {response.data}")
        
        login_response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK, f"Login failed: {login_response.data}")
        
        self.access_token = login_response.data.get('access')
        if self.access_token:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        else:
            raise ValueError('Access token not found in login response')

    def test_create_task(self):
        task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'status': 'In Progress',
            'due_date': date.today() + timedelta(days=5)
        }
        response = self.client.post(self.task_list_create_url, task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, f"Failed to create task: {response.data}")
        self.assertEqual(response.data['title'], 'Test Task')

    def test_get_tasks_by_status(self):
        Task.objects.create(title='Completed Task', description='Completed', status='Completed', due_date=date.today(), assigned_to=self.client.user)
        Task.objects.create(title='In Progress Task', description='In Progress', status='In Progress', due_date=date.today() + timedelta(days=5), assigned_to=self.client.user)
        Task.objects.create(title='Overdue Task', description='Overdue', status='In Progress', due_date=date.today() - timedelta(days=1), assigned_to=self.client.user)

        response = self.client.get(self.completed_tasks_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Failed to retrieve completed tasks: {response.data}")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Completed Task')

        response = self.client.get(self.inprogress_tasks_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Failed to retrieve in-progress tasks: {response.data}")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'In Progress Task')

        response = self.client.get(self.overdue_tasks_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Failed to retrieve overdue tasks: {response.data}")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Overdue Task')

    def test_update_task(self):
        task = Task.objects.create(title='Test Task', description='This is a test task', status='In Progress', due_date=date.today() + timedelta(days=5), assigned_to=self.client.user)
        update_url = reverse('update-task', kwargs={'pk': task.id})
        updated_data = {
            'title': 'Updated Task',
            'description': 'Updated description',
            'status': 'Completed'
        }
        pdb.set_trace()  # Insert pdb for debugging
        response = self.client.put(update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Failed to update task: {response.data}")
        self.assertEqual(response.data['title'], 'Updated Task')
        self.assertEqual(response.data['status'], 'Completed')

    def test_delete_task(self):
        task = Task.objects.create(title='Test Task', description='This is a test task', status='In Progress', due_date=date.today() + timedelta(days=5), assigned_to=self.client.user)
        delete_url = reverse('delete-task', kwargs={'pk': task.id})
        pdb.set_trace()  # Insert pdb for debugging
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, f"Failed to delete task: {response.data}")
        self.assertFalse(Task.objects.filter(id=task.id).exists(), "Task still exists after deletion")

