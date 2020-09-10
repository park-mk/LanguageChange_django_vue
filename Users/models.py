from django.db import models

# Create your models here.


class Users(models.Model):
    username = models.CharField(max_length=255)
    userid=models.CharField(max_length=255,unique=True, db_index=True)
    password=models.CharField(max_length=300,default='1234')
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.IntegerField(default=0)
    is_rent = models.BooleanField(default=False)
    is_apply_a = models.BooleanField(default=False)
    is_apply_b = models.BooleanField(default=False)
    history=models.TextField( default=" ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reason_a= models.CharField(max_length=3000,default='')
    apply_equip_id=models.IntegerField(default=0)
    noti_count=models.IntegerField(default=0)
    rent_start=models.DateTimeField(null=True, blank=True)
    rent_end=models.DateTimeField(null=True, blank=True)
    waiting_list=models.ManyToManyField('LIST',blank=True)
    history_e = models.ManyToManyField('HIS',blank=True)






    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['userid']



    def __str__(self):
        return self.email



class LIST(models.Model):
        name = models.CharField(max_length=30)
        userid = models.CharField(max_length=30)

        def __str__(self):
            return self.name


class HIS(models.Model):
    name = models.CharField(max_length=30)
    userid = models.CharField(max_length=30)
    borrow_from =models.DateTimeField(blank=True)
    borrow_til = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

