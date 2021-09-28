from factory import Faker
from factory.django import DjangoModelFactory

from priorities.models import PrioritiesModel, PrioritiesNameModel


class PrioritiesModelFactory(DjangoModelFactory):
    id = Faker('uuid4')

    class Meta:
        model = PrioritiesModel


class PrioritiesNameModelFactory(DjangoModelFactory):
    id = Faker('uuid4')

    class Meta:
        model = PrioritiesNameModel
