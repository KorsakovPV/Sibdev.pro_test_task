# Generated by Django 3.2.7 on 2021-09-29 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_emailconfirmation_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailconfirmationmessage',
            name='email_confirmation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='confirmation_messages', to='accounts.emailconfirmation', verbose_name='Email confirmation'),
        ),
    ]
