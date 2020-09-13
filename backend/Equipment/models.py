from django.db import models

# we create value model in model
class Equip(models.Model):
    #origin info
    id = models.AutoField(primary_key=True,unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    is_rent = models.BooleanField(default=False)
    is_return =models.BooleanField(default=False)
    is_gelai=models.IntegerField(default=0)
    is_on = models.BooleanField(default=False)
    description = models.CharField(default='',max_length=50)
    location = models.CharField(default='',max_length=50)
    phone_number = models.CharField(default='',max_length=50)
    provider_id = models.CharField(max_length=50,default="0")
    created_at = models.DateTimeField(null=True, blank=True)
    apply_num=models.IntegerField(default=0)
    is_apply =models.BooleanField(default=False)
    apply_pending_list=models.ManyToManyField('Pending', blank=True)
    waiting_list = models.ManyToManyField('LIST', blank=True)
    history_list = models.ManyToManyField('HIS', blank=True)
    grade_list= models.ManyToManyField('GRADE', blank=True)

    # following user info
    reason = models.CharField(default='',max_length=200)
    rent_user_name = models.CharField(default='',max_length=50)
    rent_user_id = models.IntegerField(default=0)




class Pending(models.Model):

    user_id = models.CharField(max_length=30)
    user_name = models.CharField(max_length=30)
    rent_start = models.DateTimeField(null=True, blank=True)
    rent_exp = models.DateTimeField(null=True, blank=True)






class LIST(models.Model):

    user_id = models.CharField(max_length=30)
    user_name = models.CharField(max_length=30)
    rent_start = models.DateTimeField(null=True, blank=True)
    rent_exp = models.DateTimeField(null=True, blank=True)
    apply_succes=models.BooleanField(default=False)
    reason=models.CharField(max_length=300,default=' ')




class HIS(models.Model):

    user_id = models.CharField(max_length=30)
    user_name = models.CharField(max_length=30)
    rent_start = models.CharField(max_length=30,default=' ')
    rent_exp =models.CharField(max_length=30,default=' ')
    reason = models.CharField(max_length=300,default=' ')



class GRADE(models.Model):
    user_id = models.CharField(max_length=30)
    user_name = models.CharField(max_length=30)
    comment=models.CharField(max_length=300)
    grade=models.FloatField(default=0)


    def __str__(self):
        return self.user_name
