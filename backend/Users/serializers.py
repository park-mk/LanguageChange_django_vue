from rest_framework import serializers
from .models import Users,HIS


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

       # fields = ['username','email','is_verified','is_active','created_at']
    def delete(self, instance):
        print(instance.userid, 'to herer')
        instance.delete()
        print('to herer')
        return instance

    def user_apply_status_up(self,instance,reason):
        instance.reason_pro=reason
        instance.is_apply_a=True
        instance.save()
        return instance





class UserStatusSerial(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'  #['password','username','userid','is_staff','is_apply_a']
       # fields = ['username','email','is_verified','is_active','created_at']

    def down_noti(self,instance):
        instance.noti=instance.noti-1
        return instance

    def upgrade_status(self, instance):
        instance.is_staff = 2
        print('up')
        instance.is_apply_a = False
        instance.save()
        return instance

    def downgrade_status(self, instance):
        instance.is_staff = 3
        instance.is_apply_a=True
        instance.save()
        return instance

    def deny_apply(self, instance):
        instance.is_apply_a = False
        instance.save()
        return instance

    def user_rent_apply(self, instance,equipid,equipname):
        instance.rent_status = 1
        instance.is_apply_b = True
        instance.apply_equip_id=equipid
        print("whRkfk")
        instance.apply_equip_name=equipname
        instance.save()
        return instance

    def user_rent_apply_to_provider(self, instance):
        instance.noti_count = instance.noti_count +1
        instance.save()
        return instance

    def user_rent_apply_to_super(self, instance):
        instance.noti_count = instance.noti_count +1
        instance.save()
        return instance

    def rent_status_to2(self ,instance):
        instance.rent_status=2
        instance.save()
        return instance

    def update_rent_status(self,instance,is_rent,rent_status):
        instance.is_rent=is_rent
        instance.rent_status=rent_status
        instance.save()
        return instance

    def update_rent_date(self, instance, rent_start, rent_end):
        instance.rent_start = rent_start
        instance.rent_end = rent_end
        instance.save()
        return instance

class UserUpdateApplySerial(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username','userid','is_apply_a','reason_a']
       # fields = ['username','email','is_verified','is_active','created_at']

    def applyform(self, instance,validated_data):
        instance.reason_a = validated_data.get('name', instance.reason_a)
        instance.is_apply_a = True
        instance.save()
        return instance

    def downgrade_status(self, instance):
        instance.is_staff = 3
        instance.is_apply_a=True
        instance.save()
        return instance

    def deny_apply(self, instance):
        instance.is_apply_a = False
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = Users
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                'The username should only contain alphanumeric characters')
        return attrs

    def create(self, validated_data):
        return Users.objects.create_user(**validated_data)


class  HISSerialize(serializers.ModelSerializer):
    class Meta:
        model = HIS
        fields = '__all__'


