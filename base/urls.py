from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenVerifyView
from .settings import DEBUG


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('episodes.urls')),
    path('api/users/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

if DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
