from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.vary import vary_on_cookie

from .serializers import RegisterSerializer, UserSerializer
from .pagination import StandardResultsSetPagination
from .models import User


class UserViewSet(viewsets.GenericViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes_by_action = {
        'list': [IsAuthenticated, IsAdminUser]
    }

    def get_queryset(self):
        return User.objects.all()

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_cookie)
    def list(self, request):
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
        return Response({
            'user': UserSerializer(
                user, context=self.get_serializer_context()
            ).data
        })


class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Response) -> Response:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(status=status.HTTP_205_RESET_CONTENT)
