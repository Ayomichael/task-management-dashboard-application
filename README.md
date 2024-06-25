
# Task Management

# Backend
This is a Django REST framework-based backend for a task management system. It includes user registration, login, task creation, and task management features. The project uses JWT for authentication.

## Setup Instructions

### Prerequisites

- Python 3.7+
- Django 3.2+
- Django REST framework
- Django REST framework Simple JWT

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Ayomichael/task-management-dashboard-application.git
   cd task-management-backend
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```
