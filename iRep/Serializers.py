from rest_framework import serializers

from iRep.models import ProductGroup, ProductUnit, Product, SalesForce, AppLanguage


class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup


class ProductUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUnit


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exculde_fields = ['created_date', 'created_by']


class ProfileLang(serializers.ModelSerializer):
    class Meta:
        model = AppLanguage
        fields = ['name']


class SalesForceSerializer(serializers.ModelSerializer):
    u_avatar = serializers.SerializerMethodField('get_avatar_url')

    def get_avatar_url(self, obj):
        if hasattr(obj, 'avatar'):
            return self.context['request'].build_absolute_uri(obj.avatar)
        return ''

    class Meta:
        model = SalesForce
        fields = ['id', 'u_avatar', 'name', 'phone', 'email', 'profile_language', 'last_activity']


class ProductCategory(serializers.ModelSerializer):
    products = ProductSerializer()

    class Meta:
        model = ProductGroup
        fields = ['id', 'name', 'products']
