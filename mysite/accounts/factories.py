import factory
import faker
from factory import Faker, LazyAttribute
from factory.django import DjangoModelFactory

from accounts.models import Account


class AccountFactory(DjangoModelFactory):
    DEFAULT_PASSWORD = 'test1'

    id = Faker('uuid4')
    # email = Faker('email')
    # email = LazyAttribute(lambda _: faker.Faker().country_calling_code() + faker.Faker().msisdn())
    email = LazyAttribute(lambda _: faker.Faker().uuid4() + faker.Faker().email())
    password = factory.PostGenerationMethodCall('set_password', DEFAULT_PASSWORD)
    name = Faker('name')

    class Meta:
        model = Account
        django_get_or_create = ('email',)
        exclude = ('DEFAULT_PASSWORD',)
