import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, department, password=None, **extra_fields):
        """
        Normal user yaratadi. Username va email avtomatik yaratiladi.
        """
        from .username_generator import get_prefix, build_username, generate_email

        if not department:
            raise ValueError("Bo'lim tanlash talab etiladi!")

        # Username raqamini chiqarish
        prefix = get_prefix()
        last_user = (
            self.model.objects.filter(department=department)
            .order_by("-username")
            .first()
        )

        if last_user:
            try:
                last_number = int(last_user.username[-3:])
            except:
                last_number = 0
        else:
            last_number = 0

        new_number = last_number + 1

        # Username va email yaratish
        username = build_username(prefix, department, new_number)
        email = generate_email(username)

        extra_fields.setdefault("is_active", False)

        user = self.model(
            username=username,
            email=email,
            department=department,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, email="superadmin@coderboys.uz", password=None, **extra_fields):
        """
        Superuser yaratish uchun kerak.
        Username default "SUPERADMIN" bo'ladi, lekin kiritish mumkin.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if username is None:
            username = "SUPERADMIN"

        if password is None:
            raise ValueError("Superuser uchun parol talab qilinadi")

        user = self.model(
            username=username,
            email=email,
            department="ADMIN",
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):

    DEPARTMENTS = [
        ("BEC", "Backend"),
        ("FET", "Frontend"),
        ("FST", "Fullstack"),
        ("FLU", "Flutter"),
        ("DEV", "Python Backend"),
        ("DSC", "Data Science"),
        ("AIM", "AI / ML"),
        ("OPS", "DevOps"),
        ("SEC", "Cyber Security"),
        ("MBL", "Mobile Android"),
        ("PMM", "Project Manager"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=10, choices=DEPARTMENTS)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return self.username
