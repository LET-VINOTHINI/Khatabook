from django.contrib.auth.hashers import check_password
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class VerifyPinView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        pin = request.data.get('pin', '')
        user = request.user
        if not user.pin_hash:
            return Response({'valid': False, 'detail': 'No PIN set.'}, status=status.HTTP_400_BAD_REQUEST)
        valid = check_password(pin, user.pin_hash)
        return Response({'valid': valid})


class BackupNowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        user.last_backup_at = timezone.now()
        user.save(update_fields=['last_backup_at'])
        return Response(UserSerializer(user).data)
