from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    pin = models.CharField(max_length=4, default="0000", validators=[RegexValidator(r'^\d{4}$', 'PIN must be a 4-digit number.')])

    def __str__(self) -> str:
        return f"{self.user.username} Profile"
