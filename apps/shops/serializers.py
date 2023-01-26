from rest_framework import serializers

from shops.models import Shop


class ShopSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField('objects_count')

    def objects_count(self, object):
        return 10

    class Meta:
        model = Shop
        fields = '__all__'
