from django.core.mail import EmailMultiAlternatives
from django.db.models import Count
from django.utils.html import strip_tags

from accounts.models import Account
from mysite.celery import app
from priorities.models import PrioritiesModel


@app.task
def send_new_preferences_to_all_users_celery() -> None:
    all_accounts = Account.objects.prefetch_related('precedents')
    all_priorities = PrioritiesModel.objects.values('priorities_name_id').annotate(Count('id')).order_by('-id__count')
    for account in all_accounts:
        recommended_for_adding_priorities = all_priorities.exclude(
            priorities_name_id__in=account.precedents.values('priorities_name_id'))[:3]
        if recommended_for_adding_priorities:
            subject = 'Recommended for adding priorities.'
            html_content = ','.join([str(x) for x in recommended_for_adding_priorities])
            text_content = strip_tags(html_content)
            message = EmailMultiAlternatives(
                subject, text_content, 'noreply@email.pro', [account.email]
            )
            message.attach_alternative(html_content, 'text/html')
            message.send()
