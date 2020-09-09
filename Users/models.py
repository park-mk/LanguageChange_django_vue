from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, is_provider=False):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)

        if is_provider:
            user.is_staff = 2      # 提供者
        else:
            user.is_staff = 3      # 一般用户

        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = 1   # 管理者
        user.save()
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    userid=models.CharField(max_length=255,unique=True, db_index=True)
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
    waiting_list=models.ManyToManyField('LIST',blank=True)
    history_e = models.ManyToManyField('HIS',blank=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

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

