from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'info', views.UserViewSet, basename='user')
urlpatterns = router.urls

urlpatterns = [
<<<<<<< Updated upstream
    path('', include(router.urls)),
=======
    path('info/', views.UserViewSet.as_view({'get': 'list'})),
    path('info/<int:pk>/', views.UserViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
    })),
    path('change_password/<int:pk>/', views.ChangePasswordView.as_view()),
>>>>>>> Stashed changes
    path('register/', views.RegisterApi.as_view()),
    path('logout/', views.LogoutView.as_view(), name='auth_logout'),
]
