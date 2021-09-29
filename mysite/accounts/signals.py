from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import translation

from accounts.models import EmailConfirmation, EmailConfirmationMessage
from accounts.tasks import send_register_confirmation_email_celery


@receiver(post_save, sender=EmailConfirmation, dispatch_uid='send_email_with_code')
def send_email_with_code(sender, instance, **kwargs):
    if instance.account is not None:
        return

    try:
        send_register_confirmation_email_celery.delay(instance.email, instance.confirmation_code)
    except Exception as e:
        success = False
        error = str(e)
    else:
        success = True
        error = ''

    EmailConfirmationMessage.objects.create(
        email_confirmation=instance, sent_code=instance.confirmation_code,
        success=success, error=error
    )
    translation.deactivate()
