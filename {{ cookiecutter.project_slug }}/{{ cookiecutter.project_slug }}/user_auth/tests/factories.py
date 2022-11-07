import factory

from essay_perfect.accounts import models


class User(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    email = factory.Faker("safe_email")
