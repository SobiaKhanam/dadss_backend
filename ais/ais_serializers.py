from .ais_models import *
from rest_framework import serializers


class VesselTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant_Trip
        fields = '__all__'
        read_only_fields = ['mt_key', 'mt_mv_key']


class MerchantVesselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant_Vessel
        fields = '__all__'
        read_only_fields = ['mv_key']


class TripDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip_Details
        fields = '__all__'
        read_only_fields = ['mtd_key', 'mtd_mt_key']
