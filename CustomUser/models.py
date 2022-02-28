from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, student_number, student_name, password=None):
        if not email:
            raise ValueError('반드시 이메일 형식이어야 합니다.')
        user = self.model(
            email=self.normalize_email(email),
            student_name=student_name,
            student_number=student_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, student_number, student_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            student_name=student_name,
            student_number=student_number,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(
        max_length=255,
        unique=True
    )

    student_number = models.CharField(
        max_length=10,
        null=False,
        unique=True
    )

    student_name = models.CharField(
        max_length=5,
        null=False
    )

    student_auth = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['student_name', 'student_number']