from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Task
from datetime import date, timedelta

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

        login_response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        }, format='json')
        # print("Login response:", login_response.data)  # Debugging
        self.assertEqual(login_response.status_code, status.HTTP_200_OK, f"Login failed: {login_response.data}")

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {login_response.data["access"]}')
        self.user = User.objects.get(username='testuser')  # Get the user instance
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
        # Create tasks
        Task.objects.create(title='Completed Task', description='Completed', status='Completed', due_date=date.today(), assigned_to=self.user)
        Task.objects.create(title='In Progress Task', description='In Progress', status='In Progress', due_date=date.today() + timedelta(days=5), assigned_to=self.user)
        Task.objects.create(title='Overdue Task', description='Overdue', status='In Progress', due_date=date.today() - timedelta(days=1), assigned_to=self.user)

        # Check completed tasks
        response = self.client.get(self.completed_tasks_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Failed to retrieve completed tasks: {response.data}")
        # print("Completed tasks response:", response.data)  # Debug statement
        completed_tasks = [task for task in response.data if task['status'] == 'Completed']
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(completed_tasks[0]['title'], 'Completed Task')

        # Check in-progress tasks
        response = self.client.get(self.inprogress_tasks_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Failed to retrieve in-progress tasks: {response.data}")
        # print("In Progress tasks response:", response.data)  # Debug statement
        inprogress_tasks = [task for task in response.data if task['status'] == 'In Progress' and task['due_date'] >= str(date.today())]
        self.assertEqual(len(inprogress_tasks), 1)
        self.assertEqual(inprogress_tasks[0]['title'], 'In Progress Task')

        # Check overdue tasks
        response = self.client.get(self.overdue_tasks_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Failed to retrieve overdue tasks: {response.data}")
        # print("Overdue tasks response:", response.data)  # Debug statement
        overdue_tasks = [task for task in response.data if task['due_date'] < str(date.today()) and task['status'] == 'In Progress']
        self.assertEqual(len(overdue_tasks), 1)
        self.assertEqual(overdue_tasks[0]['title'], 'Overdue Task')

    def test_update_task(self):
        task = Task.objects.create(title='Test Task', description='This is a test task', status='In Progress', due_date=date.today() + timedelta(days=5), assigned_to=self.user)
        update_url = reverse('update-task', kwargs={'pk': task.id})
        updated_data = {
            'title': 'Updated Task',
            'description': 'Updated description',
            'status': 'Completed'
        }
        response = self.client.put(update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Failed to update task: {response.data}")
        self.assertEqual(response.data['title'], 'Updated Task')
        self.assertEqual(response.data['status'], 'Completed')

    def test_delete_task(self):
        task = Task.objects.create(title='Test Task', description='This is a test task', status='In Progress', due_date=date.today() + timedelta(days=5), assigned_to=self.user)
        delete_url = reverse('delete-task', kwargs={'pk': task.id})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, f"Failed to delete task: {response.data}")
        self.assertFalse(Task.objects.filter(id=task.id).exists(),"Task still exists after deletion")

