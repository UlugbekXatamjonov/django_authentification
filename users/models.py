from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, UserManager
from datetime import datetime, timedelta

from shared.models import BaseModel

import random

USER_ROLES = (
    ('ordinary_user',"Ordinary User"),
    ("meneger","Meneger"),
    ('superadmin',"Super Admin"),
)

AUTH_TYPE_CHOISE = (
    ('via_email',"Via email"),
    ('via_username','Via username'),
    ('via_phone','Via phone')
)

SEX_CHOICES = (
    ('man','Man'),
    ('mail','Mail')
)

_validate_phone = RegexValidator(
    regex = r"^9\d{12}$",
    message = "Telefon raqamingiz 9 bilan boshlanishi va 12 belgidan oshmasligi lozim. Masalan: 998334568978",
)

PHONE_EXPIRE = 2
EMAIL_EXPIRE = 5

AUTH_STATUS = (
    ('new','New'),
    ('code_verified','Code verified'),
    ('information_filled','Information filled'),
    ('done','Done'),
)


class UserConfirmation(models.Model):
    TYPE_CHOISES = (
        ('via_phone', "via phone"),
        ('via_email', "via email"),
    )

    code = models.CharField(max_length=4)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    verify_type = models.CharField(max_length=50, choices=TYPE_CHOISES)
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if self.verify_type == 'via_email':
                self.expiration_time = datetime.now() + timedelta(minutes=EMAIL_EXPIRE)
            else:
                self.expiration_time = datetime.now() + timedelta(minutes=PHONE_EXPIRE)
        super(UserConfirmation, self).save(*args, **kwargs)


class User(AbstractUser, BaseModel):
    user_roles = models.CharField(max_length=50, choices=USER_ROLES, default='ordinary_user')
    auth_type = models.CharField(max_length=50, choices=AUTH_TYPE_CHOISE, default='via_username')
    auth_status = models.CharField(max_length=50, choices=AUTH_STATUS, default='new')
    sex = models.CharField(max_length=50, choices=SEX_CHOICES, null=True)
    email = models.EmailField(null=True, unique=True)
    phone_number = models.CharField(max_length=20, null=True, unique=True, validators=[_validate_phone])
    bio = models.CharField(max_length=250, null=True)

    object = UserManager()

    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def create_verify_code(self, verify_type):
        code = "".join([str(random.randint(0,100) % 10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id  = self.id,
            verify_type=verify_type,
            code = code
        )
        return code


