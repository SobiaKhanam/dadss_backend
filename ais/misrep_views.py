from rest_framework import serializers
from .ais_models import MissionReport, MRDetails, Merchant_Vessel
from .parent import CustomViewSet, PositionField


class MRDetailsSerializer(serializers.ModelSerializer):
    mrd_position = PositionField()

    class Meta:
        model = MRDetails
        fields = '__all__'
        read_only_fields = ['mrd_key', 'mrd_mr_key', 'mrd_mv_key']


class MreportSerializer(serializers.ModelSerializer):
    missionreportdetails = MRDetailsSerializer(many=True, source='mrdetails')

    class Meta:
        model = MissionReport
        fields = '__all__'
        read_only_fields = ['mr_key', 'mr_rdt']

    def create(self, validated_data):
        missionreportdetails = validated_data.pop('mrdetails')
        mreport = MissionReport.objects.create(**validated_data)

        for mrdetails in missionreportdetails:
            mrd_mmsi = mrdetails.get('mrd_mmsi', None)
            mrd_vessel_type = mrdetails.get('mrd_vessel_type', None)
            mrd_vessel_name = mrdetails.get('mrd_vessel_name', None)
            merchant_vessel = Merchant_Vessel.objects.filter(mv_mmsi=mrd_mmsi).first()

            if not merchant_vessel:
                merchant_vessel = Merchant_Vessel.objects.create(
                    mv_mmsi=mrd_mmsi,
                    mv_ship_name=mrd_vessel_name,
                    mv_ais_type_summary=mrd_vessel_type,
                    mv_data_source="misrep"
                )
            MRDetails.objects.create(mrd_mr_key=mreport, mrd_mv_key=merchant_vessel, **mrdetails)
        return mreport


class MreportViewSet(CustomViewSet):
    queryset = MissionReport.objects.all()
    serializer_class = MreportSerializer

    filterset_fields = {
        'mr_key': ['exact', 'gte', 'lte'],
        'mr_pf_id': ['exact'],
        'mr_rdt': ['exact', 'gte', 'lte', 'gt', 'lt'],
        'mr_dtg': ['exact', 'gte', 'lte', 'gt', 'lt'],
    }
    search_fields = ['mr_pf_id']
    ordering_fields = ['mr_key', 'mr_rdt', 'mr_dtg']
    ordering = ['-mr_key']
