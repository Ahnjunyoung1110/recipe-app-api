
# DB 모델

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    # 유저 매니저

    def create_user(self, email, password=None, **extra_field):
        # 새로운 유저 만드는 함수 extra_field로 확장성 첨가
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # 일반 유저
    email = models.EmailField(max_length=256, unique=True)
    name = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
