from rest_framework import serializers
from .ais_models import ShipBreaking, Sbcrews, Merchant_Vessel
from msa.api.parent import CustomViewSet


class MerchantVesselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant_Vessel
        fields = ['mv_imo', 'mv_ship_name', 'mv_flag', 'mv_ais_type_summary']


class SbCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sbcrews
        fields = '__all__'
        read_only_fields = ['sbc_key', 'sbc_sb_key']


class ShipBreakingSerializer(serializers.ModelSerializer):
    shipbreakingcrew = SbCrewSerializer(many=True, source='sb_crews', required=False)
    mv_imo = serializers.IntegerField(write_only=True, required=False)
    mv_ship_name = serializers.CharField(write_only=True, required=False)
    mv_flag = serializers.CharField(write_only=True, required=False)
    mv_ais_type_summary = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = ShipBreaking
        fields = '__all__'
        read_only_fields = ['sb_key', 'sb_rdt', 'sb_mv_key']

    def create(self, validated_data):
        shipbreakingcrew = validated_data.pop('sb_crews', [])
        mv_imo = validated_data.pop('mv_imo', None)
        mv_ship_name = validated_data.pop('mv_ship_name', None)
        mv_ais_type_summary = validated_data.pop('mv_ais_type_summary', None)
        mv_flag = validated_data.pop('mv_flag', None)
        merchant_vessel = Merchant_Vessel.objects.filter(mv_imo=mv_imo).first()

        if not merchant_vessel:
            merchant_vessel = Merchant_Vessel.objects.create(
                mv_imo=mv_imo,
                mv_ship_name=mv_ship_name,
                mv_ais_type_summary=mv_ais_type_summary,
                mv_flag=mv_flag,
                mv_data_source='ship_breaking'
            )
        shipbreaking = ShipBreaking.objects.create(**validated_data, sb_mv_key=merchant_vessel)
        for sb_crews in shipbreakingcrew:
            Sbcrews.objects.create(**sb_crews, sbc_sb_key=shipbreaking)
        return shipbreaking


class ShipBreakingViewSet(CustomViewSet):
    queryset = ShipBreaking.objects.all()
    serializer_class = ShipBreakingSerializer

    filterset_fields = {
        'sb_key': ['exact', 'gte', 'lte'],
        'sb_rdt': ['exact', 'gte', 'lte', 'gt', 'lt'],
        'sb_dtg': ['exact', 'gte', 'lte', 'gt', 'lt'],
    }
    search_fields = ['sb_ex_name']
    ordering_fields = ['sb_key', 'sb_rdt', 'sb_dtg']
    ordering = ['-sb_key']
