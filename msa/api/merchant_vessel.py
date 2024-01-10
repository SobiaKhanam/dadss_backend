from .fishing_vessel import *
from .models import *
from .parent import *


class MerchantTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sreports2
        # fields = '__all__'
        exclude = ['sr_key']


class MerchantSerializer(CustomSrSerializer):
    trip_source = 'merchant_trip'
    child = Sreports2
    tripDetails = MerchantTripSerializer(many=False, source=trip_source)
    sr_type = serializers.HiddenField(default='MERCHANT')

    class Meta:
        model = Sreports
        fields = '__all__'
        read_only_fields = ['sr_key', 'sr_rdt']


class MerchantViewSet(CustomSrViewSet):
    queryset = Sreports.objects.filter(sr_type='MERCHANT')
    serializer_class = MerchantSerializer
