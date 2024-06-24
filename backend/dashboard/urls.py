from django.urls import path
from .import views

urlpatterns = [
path("tasks/", views.TaskListCreate.as_view(), name="task-list"), 
path("tasks/delete/<int:pk>/", views.TaskDelete.as_view(), name="delete-task"),
path('tasks/update/<int:pk>/', views.TaskUpdate.as_view(), name='update-task'),
path('tasks/inprogress/', views.InProgressTasks.as_view(), name="inprogress-task"),
path('tasks/completed/', views.CompletedTasks.as_view(), name="completed-task"),
path('tasks/overdue/', views.OverdueTasks.as_view(), name="overdue-task"),
path('login/', views.LoginView.as_view(), name='login'),
]