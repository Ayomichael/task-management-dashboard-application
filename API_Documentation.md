# API Documentation

### Endpoint

### User Registration

URL: /user/register/

Method: POST

Request Body:{
"username": "testuser",
"email": "testuser@example.com",
"password": "testpassword123"
}
Response:
{
"id": 1,
"username": "testuser",
"email": "testuser@example.com",
"access": "access_token",
"refresh": "refresh_token"
}

### User Login

URL: /login/

Method: POST

Request Body:{
"username": "testuser",
"password": "testpassword123"
}
Response: {
"access": "access_token",
"refresh": "refresh_token"
}

### Create Task

URL: /tasks/

Method: POST

Headers:Authorization: Bearer access_token
Request Bosy: {
"title": "Test Task",
"description": "This is a test task",
"status": "In Progress",
"due_date": "2024-06-30"
}
Response: {
"id": 1,
"title": "Test Task",
"description": "This is a test task",
"status": "In Progress",
"priority": null,
"due_date": "2024-06-30",
"category": null,
"assigned_to": 1
}

### Get Completed Tasks

URL: /tasks/completed/

Method: GET

Headers:Authorization: Bearer access_token
Response: [
{
"id": 1,
"title": "Completed Task",
"description": "Completed",
"status": "Completed",
"priority": null,
"due_date": "2024-06-25",
"category": null,
"assigned_to": 1
}
]

### Get In-Progress Tasks

URL: /tasks/inprogress/

Method: GET

Headers:Authorization: Bearer access_token
Response: [
{
"id": 2,
"title": "In Progress Task",
"description": "In Progress",
"status": "In Progress",
"priority": null,
"due_date": "2024-06-30",
"category": null,
"assigned_to": 1
}
]

### Get Overdue Tasks

URL: /tasks/overdue/

Method: GET

Headers:Authorization: Bearer access_token
Response: [
{
"id": 3,
"title": "Overdue Task",
"description": "Overdue",
"status": "In Progress",
"priority": null,
"due_date": "2024-06-24",
"category": null,
"assigned_to": 1
}
]

### Update Task

URL: /tasks/update/<int:pk>

Method: PUT

Headers:Authorization: Bearer access_token
Request Body:{
"title": "Updated Task",
"description": "Updated description",
"status": "Completed"
}
Response:{
"id": 1,
"title": "Updated Task",
"description": "Updated description",
"status": "Completed",
"priority": null,
"due_date": "2024-06-30",
"category": null,
"assigned_to": 1
}

### Delete Task

URL: /tasks/delete/<int:pk>/

Method: DELETE

Headers:Authorization: Bearer access_token
Response: {
"detail": "Task deleted successfully"
}

### Running Tests

To run the unit tests, use the following command:
python manage.py test
