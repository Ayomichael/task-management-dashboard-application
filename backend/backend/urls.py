from django.contrib import admin
from django.urls import path, include
from dashboard.views import CreateUserView
from rest_framework_simplejwt.views import (
    TokenRefreshView,TokenObtainPairView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/register/",CreateUserView.as_view(), name="register"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('dashboard.urls')),
    path("auth/", include("rest_framework.urls"))
]
