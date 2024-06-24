from django.contrib import admin
from django.urls import path, include
from dashboard.views import CreateUserView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/register/",CreateUserView.as_view(), name="register"),
    path('', include('dashboard.urls')),
    path("auth/", include("rest_framework.urls"))
]
