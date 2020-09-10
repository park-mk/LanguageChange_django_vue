from rest_framework import serializers
from .models import Equip
import datetime

class EquipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equip
        fields = '__all__'

#or fields =['name','is_active'] if you want specific value

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.location = validated_data.get('location', instance.location)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.provider_id = validated_data.get('provider_id', instance.provider_id)
        instance.save()
        return instance

    def delete(self, instance):
        instance.is_active = False
        instance.is_on = False
        instance.delete()
        return instance

    def on(self, instance):
        instance.is_on = True
        instance.is_apply = False
        # to superuser noti+1
        instance.save()
        return instance

    def off(self, instance):
        instance.is_on = False
        instance.is_apply = False
        instance.save()
        return instance

    def allow(self, instance):
        instance.is_rent = True
        instance.rent_start = datetime.date.now()
        # rent_user_name
        #  to user noti +1 and
        instance.save()
        return instance

class EquipRentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equip
        fields = ['id','name','phone_number','is_apply','is_rent','rent_user_name','provider_id']

class EquipRentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equip
        fields = ['reason','rent_user_name','name','rent_start','rent_exp']


class EquipONSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equip
        fields = ['id','is_on','name','phone_number','location']

class EquipStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equip
        fields = ['id','name','phone_number','is_apply','is_on']

    def on_status(self, instance):
        instance.is_on = True
        print('up')
        instance.is_apply = False
        instance.save()
        return instance

    def off_status(self, instance):
        instance.is_on = False
        instance.is_apply = False
        instance.save()
        return instance


    def deny_apply(self, instance):
        instance.is_apply = False
        instance.save()
        return instance


    def accept_apply(self, instance):
        instance.is_apply = False
        instance.is_rent=True
        instance.save()
        return instance


class EquipDesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equip
        fields = ['name','phone_number','location','description']


