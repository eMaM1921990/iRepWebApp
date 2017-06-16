from rest_framework import serializers

from iRep.models import ProductGroup, ProductUnit, Product, SalesForce, AppLanguage, Client, Orders, OrderLine, \
    SalesForceSchedual


class ProductUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUnit


class ProfileLang(serializers.ModelSerializer):
    class Meta:
        model = AppLanguage
        fields = ['name']


class SalesForceSerializer(serializers.ModelSerializer):
    u_avatar = serializers.SerializerMethodField('get_avatar_url')

    def get_avatar_url(self, obj):
        if hasattr(obj, 'avatar'):
            if obj.avatar:
                return self.context['request'].build_absolute_uri(obj.avatar.url)
        return ''

    class Meta:
        model = SalesForce
        fields = ['id', 'u_avatar', 'name', 'phone', 'email', 'profile_language', 'last_activity']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'ean_code', 'default_price', 'note', 'unit']


class ProductGroupSerializer(serializers.ModelSerializer):
    group_products = ProductSerializer(many=True)

    class Meta:
        model = ProductGroup
        fields = ['id', 'name', 'group_products']


class ClientSerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField('get_region')
    country = serializers.SerializerMethodField('get_country')

    def get_region(self, obj):
        if hasattr(obj, 'state'):
            return obj.state

    def get_country(self, obj):
        if hasattr(obj, 'country'):
            return obj.country

    class Meta:
        model = Client
        fields = ['id', 'name', 'address_txt', 'country', 'region', 'city', 'zipcode', 'contact_name',
                  'contact_title', 'website', 'email', 'phone', 'notes', 'status', 'main_branch']


class OrderLinesSerializer(serializers.ModelSerializer):
    order_product = ProductSerializer(many=True)

    class Meta:
        model = OrderLine
        fields = ['order_product', 'quantity', 'price']


class OrderSerializers(serializers.ModelSerializer):
    order_lines = OrderLinesSerializer(many=True)

    class Meta:
        model = Orders
        fields = ['id', 'sales_force', 'order_date', 'total', 'notes', 'order_lines']


class SchedualSerializers(serializers.ModelSerializer):
    sales_force = SalesForceSerializer(many=True)
    branch = ClientSerializer(many=True)

    class Meta:
        model = SalesForceSchedual
        fields = ['id', 'sales_force', 'branch', 'schedual_date', 'schedual_time', 'notes']
