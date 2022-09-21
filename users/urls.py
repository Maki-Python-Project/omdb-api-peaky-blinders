from django.urls import path

from . import views


urlpatterns = [
    path('info/', views.UserViewSet.as_view({'get': 'list'})),
    path('info/<int:pk>/', views.UserViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
    })),
    path('change_password/<int:pk>/', views.ChangePasswordView.as_view()),
    path('register/', views.RegisterApi.as_view()),
    path('logout/', views.LogoutView.as_view(), name='auth_logout'),
]
