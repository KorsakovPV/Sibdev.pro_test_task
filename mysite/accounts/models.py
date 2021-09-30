import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel, UUIDModel


class Account(AbstractBaseUser, TimeStampedModel, UUIDModel):
    USERNAME_FIELD = 'email'

    email = models.EmailField(verbose_name=_('email address'), unique=True)
    confirmed = models.BooleanField(verbose_name=_('Confirmed'), default=False)
    name = models.CharField(verbose_name=_('Full name'), max_length=255)

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = 'Accounts'

class EmailConfirmation(TimeStampedModel):
    CODE_TIMEDELTA = timezone.timedelta(days=1)

    email = models.EmailField(_('Email'), unique=True)
    confirmation_code = models.UUIDField(_('Confirmation code'), default=uuid.uuid4)
    account = models.OneToOneField(
        Account, verbose_name=_('Account'), on_delete=models.CASCADE, null=True,
        default=None, related_name='email_confirmation', blank=True
    )

    class Meta:
        verbose_name = _('Email confirmation')
        verbose_name_plural = _('Email confirmations')
        ordering = ('-created',)

    def __str__(self):
        return str(self.email)


class EmailConfirmationMessage(TimeStampedModel):
    email_confirmation = models.ForeignKey(
        EmailConfirmation, verbose_name=_('Email confirmation'), on_delete=models.CASCADE,
        related_name=_('confirmation_messages')
    )
    sent_code = models.UUIDField(_('Sent code'))
    success = models.BooleanField(_('Success'))
    error = models.TextField('Error', blank=True)

    class Meta:
        verbose_name = _('Email confirmation message')
        verbose_name_plural = _('Email confirmation messages')
        ordering = ('-created',)

    def __str__(self):
        return str(self.email_confirmation.email)
