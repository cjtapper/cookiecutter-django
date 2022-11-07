import factory

from {{cookiecutter.project_slug}}.user_auth import models


class User(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    email = factory.Faker("safe_email")
