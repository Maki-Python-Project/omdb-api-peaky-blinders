from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.vary import vary_on_cookie
from django.db.models.query import QuerySet
from typing import Type, Union

from .serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer
from .pagination import StandardResultsSetPagination
from .models import User
from .permissions import AccountOwnerPermission
from .tasks import send_a_message_to_email


class UserViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes_by_action = {
        'list': [IsAuthenticated, IsAdminUser],
        'retrieve': [IsAuthenticated, IsAdminUser],
        'destroy': [IsAuthenticated, IsAdminUser],
    }

    def get_queryset(self) -> QuerySet[User]:
        return User.objects.all()

    def get_permissions(self) -> Union[Type[IsAuthenticated], Type[IsAdminUser]]:
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self) -> Type[UserSerializer]:
        return UserSerializer

    @method_decorator(cache_page(60*5))
    @method_decorator(vary_on_cookie)
    def list(self, request: Response) -> Response:
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request: Response) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_a_message_to_email.delay(user.email, user.username)

        return Response({
            'user': UserSerializer(
                user, context=self.get_serializer_context()
            ).data
        })


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, AccountOwnerPermission)
    serializer_class = ChangePasswordSerializer


class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Response) -> Response:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(status=status.HTTP_205_RESET_CONTENT)
