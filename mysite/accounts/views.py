from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import Account
from accounts.serializers import EmailConfirmationSerializer, RegisterAccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    permission_classes = [AllowAny]
    # http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        queryset = self.queryset.filter(email=self.request.user.email)
        return queryset

    @extend_schema(request=EmailConfirmationSerializer, responses={201: None})
    @action(detail=False, methods=['post'], name='Send confirmation email', permission_classes=[AllowAny])
    def send_confirmation_email(self, request):
        """
        Send email with code for confirmation
        """
        validate_email_serializer = EmailConfirmationSerializer(data=request.data)
        validate_email_serializer.is_valid(raise_exception=True)
        self.perform_create(validate_email_serializer)
        return Response(status=status.HTTP_201_CREATED, data=validate_email_serializer.data)

    @extend_schema(request=RegisterAccountSerializer, responses={201: RegisterAccountSerializer})
    @action(detail=False, methods=['post'], name='Register user', permission_classes=[AllowAny])
    def register(self, request):
        """
        Register user after all confirmation checks
        """
        register_serializer = RegisterAccountSerializer(data=request.data)
        register_serializer.is_valid(raise_exception=True)
        register_serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=register_serializer.data)
