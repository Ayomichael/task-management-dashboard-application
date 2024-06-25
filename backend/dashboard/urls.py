from django.urls import path
from .import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
path("tasks/", views.TaskListCreate.as_view(), name="task-list"), 
path("tasks/delete/<int:pk>/", views.TaskDelete.as_view(), name="delete-task"),
path('tasks/update/<int:pk>/', views.TaskUpdate.as_view(), name='update-task'),
path('tasks/inprogress/', views.InProgressTasks.as_view(), name='inprogress-task'),
path('tasks/completed/', views.CompletedTasks.as_view(), name='completed-task'),
path('tasks/overdue/', views.OverdueTasks.as_view(), name='overdue-task'),
path("user/register/",views.CreateUserView.as_view(), name='register'),
path('login/', views.LoginUserView.as_view(), name='login'),
path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

]