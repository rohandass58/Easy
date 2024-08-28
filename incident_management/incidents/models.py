from django.db import models
from django.contrib.auth.models import AbstractUser


from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import random


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_category", "Individual")  # Set a default category

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    USER_TYPE = [
        ("Individual", "Individual"),
        ("Enterprise", "Enterprise"),
        ("Government", "Government"),
    ]

    username = None  # Remove username field
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    pin_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    user_category = models.CharField(
        max_length=10, choices=USER_TYPE, blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Incident(models.Model):
    INCIDENT_STATUS_CHOICES = [
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Closed", "Closed"),
    ]
    PRIORITY_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]
    ENTITY_TYPE_CHOICES = [
        ("Enterprise", "Enterprise"),
        ("Government", "Government"),
        ("Individual", "Individual"),
    ]

    id = models.AutoField(primary_key=True)
    incident_id = models.CharField(max_length=15, unique=True, editable=False)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPE_CHOICES)
    details = models.TextField()
    reported_date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=INCIDENT_STATUS_CHOICES)

    def save(self, *args, **kwargs):
        if not self.incident_id:
            self.incident_id = self.generate_unique_incident_id()
        super(Incident, self).save(*args, **kwargs)

    @classmethod
    def generate_unique_incident_id(cls):
        current_year = timezone.now().year
        while True:
            random_number = random.randint(10000, 99999)
            incident_id = f"RMG{random_number}{current_year}"
            if not cls.objects.filter(incident_id=incident_id).exists():
                return incident_id

    def __str__(self):
        return self.incident_id
