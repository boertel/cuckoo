import factory

from cuckoo import models

from .base import ModelFactory
from .types import GUIDFactory


class ApplicationFactory(ModelFactory):
    id = GUIDFactory()
    name = factory.Faker('name')
    user = factory.SubFactory('cuckoo.factories.UserFactory')
    user_id = factory.SelfAttribute('user.id')

    class Meta:
        model = models.Application
