from django.db import models

# we create value model in model
class Equip(models.Model):
    name = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.IntegerField(default=0)
    is_rent = models.BooleanField(default=False)
    is_apply_a = models.BooleanField(default=False)
    is_apply_b = models.BooleanField(default=False)
    history = models.TextField(default=" ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



