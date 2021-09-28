import uuid

import django.contrib.auth.password_validation as validators
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from accounts.models import EmailConfirmation, EmailConfirmationMessage, Account


class EmailConfirmationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        existing_confirmation = EmailConfirmation.objects.filter(email=validated_data['email']).first()
        if existing_confirmation:
            if existing_confirmation.account is not None:
                raise ValidationError({'email': 'Email is already confirmed'})

            if timezone.now() >= existing_confirmation.created + EmailConfirmation.CODE_TIMEDELTA:  # too old code
                existing_confirmation.code = uuid.uuid4()

            existing_confirmation.save()

            instance = existing_confirmation

        else:
            instance = super().create(validated_data)

        return instance

    class Meta:
        model = EmailConfirmation
        fields = ('email',)


class EmailConfirmationResponseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.UUIDField()


class EmailConfirmationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfirmationMessage
        fields = ('email_confirmation',)


class RegisterAccountSerializer(serializers.ModelSerializer):
    """
    Registration serializer, only for account creation
    """
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Account.objects.all())]
    )
    confirmed = serializers.BooleanField(read_only=True, initial=True, default=True)
    email_confirmation_code = serializers.UUIDField(write_only=True)

    def validate_password(self, value):
        """
        Check if password is strong
        """
        try:
            validators.validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))

        return value

    def validate(self, attrs):
        """
        Validation process:
        """
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {'confirm_password': "Passwords didn't match"}
            )

        email_confirmation_code = attrs['email_confirmation_code']
        try:
            EmailConfirmation.objects.get(
                email=attrs['email'], confirmation_code=email_confirmation_code
            )
        except EmailConfirmation.DoesNotExist:
            raise ValidationError({'email': 'Email is not confirmed'})

        return attrs

    def create(self, validated_data):
        """
        Create user and add "User" role to him if it exists
        """

        validated_data.pop('confirm_password')
        email_confirmation_code = validated_data.pop('email_confirmation_code')

        validated_data['confirmed'] = True

        validated_data['password'] = make_password(validated_data['password'])
        email_confirmation = EmailConfirmation.objects.get(
            email=validated_data['email'], confirmation_code=email_confirmation_code
        )

        with transaction.atomic():
            new_user = super().create(validated_data)
            email_confirmation.account = new_user
            email_confirmation.save()

        return new_user

    def update(self, instance, validated_data):
        raise ValidationError('Update is disabled')

    class Meta:
        model = Account
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    """
    Registration serializer, only for account creation
    """

    class Meta:
        model = Account
        fields = '__all__'
