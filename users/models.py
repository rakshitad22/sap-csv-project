from django.db import models
from django.contrib.auth.models import User


class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entered_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.entered_name