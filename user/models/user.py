from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UserManager as BaseUserAdmin
)
from django.utils.translation import gettext_lazy as _

from base.abstract_models import TimeStampedModel


class UserManager(BaseUserAdmin):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, TimeStampedModel):
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    email = models.EmailField(
        _('email address'),
        max_length=150,
        unique=True
    )
    phone = models.CharField(
        'Телефон',
        max_length=32,
        null=True,
        blank=True,
        unique=True
    )
    is_active = models.BooleanField(
        default=True
    )
    objects = UserManager()

    def __str__(self):
        return "{} {}".format(self.id, self.email)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
