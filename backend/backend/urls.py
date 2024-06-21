from django.contrib import admin
from django.urls import path, include
from dashboard.views import CreateUserView
from rest_framework_simplejwt.views import (
    TokenRefreshView,TokenObtainPairView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/user/register/",CreateUserView.as_view(), name="register"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('dashboard.urls')),
    path("api-auth/", include("rest_framework.urls"))
]
