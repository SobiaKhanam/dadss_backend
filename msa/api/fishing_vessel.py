from rest_framework.generics import get_object_or_404

from .models import *
from django.utils import timezone
from .parent import *
from .reg_vessel import RvesselSerializer


class FishingTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sreports1
        # fields = '__all__'
        exclude = ['sr_key']


class SrnakwaSerializer(serializers.ModelSerializer):
    src_type = serializers.HiddenField(default='NAKWA')

    class Meta:
        model = Srcrews
        fields = ['src_key', 'src_name', 'src_nationality', 'src_ethnicity', 'src_cell', 'src_type']
        read_only_fields = ['src_key', 'src_srv_key']


class SrcrewSerializer(serializers.ModelSerializer):
    src_type = serializers.HiddenField(default='CREW')

    class Meta:
        model = Srcrews
        # fields = '__all__'
        exclude = ['src_srv_key', 'src_sr_key']
        read_only_fields = ['src_key']


class SrownerSerializer(serializers.ModelSerializer):
    sro_share = serializers.IntegerField()
    sro_type = serializers.HiddenField(default='OWNER')

    class Meta:
        model = Srowners
        # fields = '__all__'
        exclude = ['sro_sr_key', 'sro_srv_key']
        read_only_fields = ['sro_key']


class SrgoodSerializer(serializers.ModelSerializer):
    srg_qty = serializers.IntegerField()
    srg_value = serializers.IntegerField()

    class Meta:
        model = Srgoods
        # fields = '__all__'
        exclude = ['srg_sr_key']
        read_only_fields = ['sro_key']
        # extra_kwargs = {
        #     'sro_srv_key': {'write_only': True},
        #     'sro_sr_key': {'write_only': True}
        # }


class CustomSrSerializer(serializers.ModelSerializer):
    trip_source = None
    child = None
    primary_key = None
    sr_rdt = serializers.DateTimeField(default=timezone.now)
    sr_position = PositionField()
    nakwaDetails = SrnakwaSerializer(many=True, source='nakwa')
    crewDetails = SrcrewSerializer(many=True, source='crew')
    goodDetails = SrgoodSerializer(many=True, source='goods')
    ownerDetails = SrownerSerializer(many=True, source='srowner')

    class Meta:
        model = Sreports
        fields = '__all__'
        read_only_fields = ['sr_key', 'sr_rdt']

    def create(self, validated_data):
        trip = validated_data.pop(self.trip_source)
        nakwaDetails = validated_data.pop('nakwa')
        crewDetails = validated_data.pop('crew')
        ownerDetails = validated_data.pop('srowner')
        goodDetails = validated_data.pop('goods')
        special_report = Sreports.objects.create(**validated_data)
        self.child.objects.create(**trip, sr_key=special_report)
        for nakwa in nakwaDetails:
            Srcrews.objects.create(**nakwa, src_sr_key=special_report, src_srv_key=special_report.sr_rv_key)
        for crew in crewDetails:
            Srcrews.objects.create(**crew, src_sr_key=special_report, src_srv_key=special_report.sr_rv_key)
        for owner in ownerDetails:
            Srowners.objects.create(**owner, sro_sr_key=special_report, sro_srv_key=special_report.sr_rv_key)
        for good in goodDetails:
            Srgoods.objects.create(**good, srg_sr_key=special_report)
        return special_report


class FishingSerializer(CustomSrSerializer):
    trip_source = 'fishing_trip'
    child = Sreports1
    primary_key = 'sr1_key'
    sr_type = serializers.HiddenField(default='FISHING')
    tripDetails = FishingTripSerializer(many=False, source=trip_source)

    class Meta:
        model = Sreports
        fields = '__all__'
        read_only_fields = ['sr_key', 'sr_rdt']


class CustomSrViewSet(CustomViewSet):
    filterset_fields = ['sr_key', 'sr_pf_id', 'sr_rv_key', 'sr_dtg', 'sr_type', 'sr_movement', 'sr_action']
    ordering = ['-sr_key']

    @action(methods=['get'], detail=False, url_path='rvkey/(?P<sr_rv_key>[^/.]+)')
    def rvkey(self, pk=None, sr_rv_key=None):
        """
            Redirect to Register Vessel object if special report is empty.
        """
        filter_query = self.queryset.filter(sr_rv_key=sr_rv_key).last()
        if filter_query is None:
            rvessel_object = get_object_or_404(Rvessels, rv_key=sr_rv_key)
            return Response(RvesselSerializer(rvessel_object, many=False).data)
        return Response(CustomSrSerializer(filter_query, many=False).data)


class FishingViewSet(CustomSrViewSet):
    queryset = Sreports.objects.filter(sr_type='FISHING')
    serializer_class = FishingSerializer
