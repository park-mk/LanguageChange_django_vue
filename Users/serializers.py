from rest_framework import serializers
from .models import Users


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



class UserStatusSerial(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username','userid','is_staff','is_apply_a']
       # fields = ['username','email','is_verified','is_active','created_at']

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