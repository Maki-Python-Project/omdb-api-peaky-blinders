from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'info', views.UserViewSet, basename='user')
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterApi.as_view()),
    path('logout/', views.LogoutView.as_view(), name='auth_logout'),
]
