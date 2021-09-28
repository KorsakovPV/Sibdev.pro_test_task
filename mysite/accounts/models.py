import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel, UUIDModel
from django.utils import timezone


class Account(AbstractBaseUser, TimeStampedModel, UUIDModel):#
    USERNAME_FIELD = 'email'

    email = models.EmailField(verbose_name=_('email address'), unique=True)
    confirmed = models.BooleanField(verbose_name=_('Confirmed'), default=False)
    name = models.CharField(verbose_name=_('Full name'), max_length=255)

class EmailConfirmationQuerySet(models.QuerySet):

    def not_confirmed(self, email):
        return self.filter(email=email, account__isnull=False)

class EmailConfirmation(TimeStampedModel):
    CODE_TIMEDELTA = timezone.timedelta(days=1)

    email = models.EmailField('Email', unique=True)
    confirmation_code = models.UUIDField('Confirmation code', default=uuid.uuid4)
    account = models.OneToOneField(
        Account, verbose_name='Account', on_delete=models.PROTECT, null=True,
        default=None, related_name='email_confirmation', blank=True
    )


    objects = EmailConfirmationQuerySet.as_manager()

    class Meta:
        verbose_name = 'Email confirmation'
        verbose_name_plural = 'Email confirmations'
        ordering = ('-id',)

    def __str__(self):
        return str(self.email)


class EmailConfirmationMessage(TimeStampedModel):
    email_confirmation = models.ForeignKey(
        EmailConfirmation, verbose_name='Email confirmation', on_delete=models.PROTECT,
        related_name='confirmation_messages'
    )
    sent_code = models.UUIDField('Sent code')
    success = models.BooleanField('Success')
    error = models.TextField('Error', blank=True)

    class Meta:
        verbose_name = 'Email confirmation message'
        verbose_name_plural = 'Email confirmation messages'
        ordering = ('-id',)

    def __str__(self):
        return str(self.email_confirmation.email)


