import uuid

from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.models import Entity
from utils.utils_functions import generate_random_otp


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, name, email, password=None, is_verified=False):
        if not email:
            raise ValueError('user must have email')

        user = self.model(email=self.normalize_email(email))
        user.name = name
        user.set_password(password)
        user.is_verified = is_verified
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if not email:
            raise ValueError('user must have email')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser, Entity):
    username = models.NOT_PROVIDED
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=200)
    profile = models.URLField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=17, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return perm in self.get_group_permissions()

    def has_module_perms(self, app_label):
        return True


class Otp(models.Model):
    number = models.IntegerField(default=generate_random_otp)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp')

    def __str__(self):
        return f'{self.user} ||| {self.number}'
