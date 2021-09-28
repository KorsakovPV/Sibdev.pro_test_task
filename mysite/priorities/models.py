from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import UUIDModel

from accounts.models import Account


class PrioritiesNameModel(UUIDModel):
    name = models.CharField(verbose_name='Full name', max_length=255)

    class Meta:
        verbose_name = _('Prioritie name')
        verbose_name_plural = _('Prioritie names')

    def __str__(self):
        return f"{self.name}"


class PrioritiesModel(UUIDModel):
    account = models.ForeignKey(Account, verbose_name=_('Account'), on_delete=models.PROTECT,
                                related_name='precedents')
    priorities_name = models.ForeignKey(PrioritiesNameModel, verbose_name=_('Priorities name'),
                                        on_delete=models.PROTECT,
                                        related_name='precedents')
    importance = models.IntegerField(verbose_name=_('Importance'),
                                     validators=[MinValueValidator(-11), MaxValueValidator(11)])

    class Meta:
        verbose_name = _('Prioritie')
        verbose_name_plural = _('Priorities')
        unique_together = ('account', 'priorities_name')

    def __str__(self):
        return f"{self.account} - {self.priorities_name} - {self.importance}"
