from rest_framework import serializers
from .models import Equip,LIST,HIS,GRADE
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

    def activate(self, instance):
        instance.is_on = True
        instance.is_active=True
        instance.is_apply = False
        # to superuser noti+1
        instance.save()
        return instance

    def unactivate(self, instance):
        instance.is_on = False
        instance.is_active = False
        instance.is_apply = False
        instance.save()
        return instance

    def return_equip(self,instance):
        instance.is_return=True
        instance.save()
        print('return is true')
        return instance

    def return_equip_check(self,instance):
        instance.is_return=False
        instance.is_rent=False
        instance.save()
        return instance



class EquipRentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equip
        fields = ['id','name','phone_number','is_apply','is_rent','rent_user_name','provider_id']

    def is_rent(self,instance):
        instance.is_rent=True
        instance.save()
        return instance

class EquipRentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equip
        fields = ['reason','rent_user_name','name','waiting_list']


class EquipONSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equip
        fields = ['id','is_on','name','phone_number','location','is_active']

class EquipStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equip
        fields = ['id','name','phone_number','is_apply','is_on','is_active','waiting_list','history_list','is_rent','provider_id','location','description','grade_list','is_return']

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


class WaitingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LIST
        fields = '__all__'

    def allow(self,instance):
        instance.apply_succes=True
        instance.save()
        return instance

    def deny(self,instance):
        instance.delete()
        return instance


class  HISSerialize(serializers.ModelSerializer):
    class Meta:
        model = HIS
        fields = '__all__'




class  GRADESerialize(serializers.ModelSerializer):
    class Meta:
        model = GRADE
        fields = '__all__'

