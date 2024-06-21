from django.urls import path, include
from .import views

urlpatterns = [
path("tasks/", views.TaskListCreate.as_view(), name="task-list"), 
path("tasks/delete/<int:pk>/", views.TaskDelete.as_view(), name="delete-task"),
path('tasks/update/<int:pk>/', views.TaskUpdateView.as_view(), name='update-task'),
]