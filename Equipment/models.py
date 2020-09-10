from django.db import models

# we create value model in model
class Equip(models.Model):
    #origin info
    id = models.AutoField(primary_key=True,unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    is_rent = models.BooleanField(default=False)
    is_on = models.BooleanField(default=False)
    description = models.CharField(default='',max_length=50)
    location = models.CharField(default='',max_length=50)
    phone_number = models.CharField(default='',max_length=50)
    provider_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(null=True, blank=True)
    is_apply =models.BooleanField(default=False)
    waiting_list = models.ManyToManyField('LIST', blank=True)
    # following user info
    reason = models.CharField(default='',max_length=200)
    rent_start = models.DateTimeField(null=True, blank=True)
    rent_exp = models.DateTimeField(null=True, blank=True)
    rent_user_name = models.CharField(default='',max_length=50)
    rent_user_id = models.IntegerField(default=0)




class LIST(models.Model):

    user_id = models.CharField(max_length=30)
    rent_start = models.DateTimeField(null=True, blank=True)
    rent_exp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
