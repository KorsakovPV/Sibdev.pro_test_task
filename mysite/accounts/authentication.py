from django.contrib.auth.backends import ModelBackend
from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings

from accounts.models import Account


class AccountAuthBackend(ModelBackend):
    """
    Custom auth backend for account auth wit `accounts.Account` model
    Uses `email` field for username
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            account = Account.objects.get(email=username)
            if account.check_password(password) is True:
                return account

        except Account.DoesNotExist:
            pass


class CustomUserJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        """
        Using model `accounts.Account` to authenticate user
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_('Token contained no recognizable user identification'))

        try:
            user = Account.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except Account.DoesNotExist:
            raise AuthenticationFailed(_('User not found'), code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed(_('User is disabled'), code='user_inactive')

        return user
