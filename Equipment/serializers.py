from rest_framework import serializers
from .models import Equip


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
        instance.save()
        return instance

    def on(self, instance):
        instance.is_on = True
        # to superuser noti+1
        instance.save()
        return instance

    def off(self, instance):
        instance.is_on = False
        instance.save()
        return instance

    def allow(self, instance):
        instance.is_rent = True
        instance.rent_start = datetime.date.now()
        # rent_user_name
        #  to user noti +1 and
        instance.save()
        return instance