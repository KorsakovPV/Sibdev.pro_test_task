from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_register_confirmation_email(receiver_email: str, code: str) -> None:
    """
    Send register confirm email

    :param receiver_email:
    :param code:
    :return:
    """
    subject = 'Confirm your account email'
    html_content = render_to_string(
        'account_confirmation.html',
        {'code': code, 'email': receiver_email}
    )
    text_content = strip_tags(html_content)
    message = EmailMultiAlternatives(
        subject, text_content, 'noreply@email.pro', [receiver_email]
    )
    message.attach_alternative(html_content, 'text/html')
    message.send()
