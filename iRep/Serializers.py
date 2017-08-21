from rest_framework import serializers

from iRep.models import ProductGroup, ProductUnit, Product, SalesForce, AppLanguage, Client, Orders, OrderLine, \
    SalesForceSchedual, SalesFunnelStatus, SalesForceTimeLine, SalesForceCheckInOut, Visits, SalesForceTrack, \
    ClientTags, \
    Tags


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
        fields = ['id', 'u_avatar', 'name', 'phone', 'email', 'profile_language', 'last_activity', 'slug']


class MemberSerializer(serializers.ModelSerializer):
    u_avatar = serializers.SerializerMethodField('get_avatar_url')

    def get_avatar_url(self, obj):
        if hasattr(obj, 'avatar'):
            if obj.avatar:
                return self.context['request'].build_absolute_uri(obj.avatar.url)
        return ''

    members = SalesForceSerializer(source='reporting_to', many=True)

    class Meta:
        model = SalesForce
        fields = ['id', 'u_avatar', 'name', 'phone', 'email', 'profile_language', 'last_activity', 'slug', 'members']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'ean_code', 'default_price', 'note', 'unit']


class ProductGroupSerializer(serializers.ModelSerializer):
    product = ProductSerializer(source='group_products', many=True)

    class Meta:
        model = ProductGroup
        fields = ['id', 'name', 'product']


class TagSerlizers(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id', 'name']


class ClientTagSerialzer(serializers.ModelSerializer):
    tags = TagSerlizers()

    class Meta:
        model = ClientTags
        fields = ['tags']


class ClientSerializer(serializers.ModelSerializer):
    client_tags = ClientTagSerialzer(many=True)
    text = serializers.SerializerMethodField('get_text_val')
    sales_force = SalesForceSerializer()

    def get_text_val(self, obj):
        if hasattr(obj, 'name'):
            return obj.name

    class Meta:
        model = Client
        fields = ['id', 'name', 'address_txt', 'country', 'state', 'city', 'zipcode', 'contact_name',
                  'contact_title', 'website', 'email', 'phone', 'notes', 'status', 'main_branch', 'text', 'sales_force',
                  'client_tags']


class OrderLinesSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderLine
        fields = ['product', 'quantity', 'price']


class OrderSerializers(serializers.ModelSerializer):
    order_lines = OrderLinesSerializer(many=True)

    class Meta:
        model = Orders
        fields = ['id', 'sales_force', 'order_date', 'total', 'sub_total', 'discount', 'notes', 'order_lines']


class SchedualSerializers(serializers.ModelSerializer):
    branch = ClientSerializer()

    class Meta:
        model = SalesForceSchedual
        fields = ['id', 'sales_force', 'branch', 'schedual_date', 'schedual_time', 'notes', 'is_visit']


class SalesFunnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesFunnelStatus
        fields = ['id', 'status_name']


class TimeLineSerializers(serializers.ModelSerializer):
    class Meta:
        model = SalesForceTimeLine
        fields = ['id', 'sales_force', 'time_line_date', 'start_time', 'end_time', 'km', 'hours']


class VisitSerializer(serializers.ModelSerializer):
    schedual = SchedualSerializers()
    branch = ClientSerializer()
    sales_force = SalesForceSerializer()

    class Meta:
        model = Visits
        fields = ['id', 'sales_force', 'branch', 'visit_date', 'notes', 'schedualed', 'schedual']


class CheckInOutSerializers(serializers.ModelSerializer):
    # branch = ClientSerializer()
    # visit = VisitSerializer()

    class Meta:
        model = SalesForceCheckInOut
        fields = ['id', 'latitude', 'longitude', 'check_in_date', 'check_in_time', 'branch', 'visit', 'check_out_date',
                  'check_out_time']


class SalesForceTracking(serializers.ModelSerializer):
    sales_force = SalesForceSerializer()

    class Meta:
        model = SalesForceTrack
        fields = ['id', 'latitude', 'longitude', 'sales_force']
