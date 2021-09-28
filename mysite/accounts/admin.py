from django.contrib import admin

from accounts.models import Account, EmailConfirmation, EmailConfirmationMessage


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ('password',)


@admin.register(EmailConfirmation)
class EmailConfirmationAdmin(admin.ModelAdmin):
    pass


@admin.register(EmailConfirmationMessage)
class EmailConfirmationMessageAdmin(admin.ModelAdmin):
    pass
