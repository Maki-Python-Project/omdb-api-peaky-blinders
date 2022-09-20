from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer
from .pagination import StandardResultsSetPagination


<<<<<<< Updated upstream
User = get_user_model()
=======
class UserViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes_by_action = {
        'list': [IsAuthenticated, IsAdminUser],
        'retrieve': [IsAuthenticated, IsAdminUser],
        'destroy': [IsAuthenticated, IsAdminUser],
    }

    def get_queryset(self):
        return User.objects.all()
>>>>>>> Stashed changes


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = StandardResultsSetPagination


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
