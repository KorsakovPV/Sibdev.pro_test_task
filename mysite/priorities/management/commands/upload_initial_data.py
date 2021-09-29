import json

import pyprind
from django.conf import settings
from django.core.management.base import BaseCommand

from accounts.factories import AccountFactory
from accounts.models import Account
from priorities.factories import PrioritiesModelFactory, PrioritiesNameModelFactory
from priorities.models import PrioritiesModel, PrioritiesNameModel

PLUS = {'positive': 1,
        'negative': -1}


class Command(BaseCommand):
    help = 'Upload initial data.'

    def handle(self, *args, **options):
        """
        python manage.py upload_initial_data
        """
        PrioritiesModel.objects.all().delete()
        PrioritiesNameModel.objects.all().delete()
        Account.objects.all().delete()
        accounts_list = []
        precedents_list = []
        precedents_dict = {}
        gen = self.gen(f'{settings.BASE_DIR}/priorities/management/commands/participants.jsonl')
        try:
            bar = pyprind.ProgBar(20000, title='Generating initial data.')
            while line := next(gen):
                bar.update()
                account = AccountFactory.build(confirmed=True, name=line.get('name'))
                accounts_list.append(account)
                precedents = line.get('precedents')
                for key, value in precedents.items():
                    precedent_name = precedents_dict.get(key)
                    if not precedent_name:
                        precedent_name = PrioritiesNameModelFactory(name=key)
                        precedents_dict[key] = precedent_name

                    precedent = PrioritiesModelFactory.build(account=account, priorities_name=precedent_name,
                                                             importance=PLUS.get(value.get('attitude')) * value.get(
                                                                 'importance'))
                    precedents_list.append(precedent)

                    if len(accounts_list) >= 1000:
                        accounts_list, precedents_list = self.save_in_bd(accounts_list, precedents_list)

        except StopIteration:
            self.save_in_bd(accounts_list, precedents_list)
        finally:
            del gen

    @staticmethod
    def save_in_bd(accounts_list: list, precedents_list: list) -> tuple[list, list]:
        Account.objects.bulk_create(accounts_list)
        accounts_list = []
        PrioritiesModel.objects.bulk_create(precedents_list)
        precedents_list = []
        return accounts_list, precedents_list

    @staticmethod
    def gen(file_name: str) -> dict:
        with open(file_name) as fh:
            while line := fh.readline():
                yield json.loads(line)
