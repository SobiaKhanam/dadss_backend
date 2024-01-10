from .parent import *
from .models import *
from django.utils import timezone


class RvnakwaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rvcrews
        fields = ['rvc_key', 'rvc_name', 'rvc_nationality', 'rvc_ethnicity', 'rvc_cell']
        read_only_fields = ['rvc_key', 'rvc_rv_key']


class RvownerSerializer(serializers.ModelSerializer):
    rvo_type = serializers.HiddenField(default='OWNER')

    class Meta:
        model = Rvowners
        # fields = '__all__'
        exclude = ['rvo_rv_key']
        read_only_fields = ['rvo_key', 'rvo_rv_key']


class RvesselSerializer(serializers.ModelSerializer):
    rv_rdt = serializers.DateTimeField(default=timezone.now)
    rv_crew = serializers.HiddenField(default=1)
    rv_length = serializers.IntegerField()
    rv_breadth = serializers.IntegerField()
    rv_tonnage = serializers.IntegerField()
    nakwaDetails = RvnakwaSerializer(many=True, source='nakwa', required=False)
    ownerDetails = RvownerSerializer(many=True, source='owner')

    class Meta:
        model = Rvessels
        fields = '__all__'
        # fields = ['rv_key', 'tonnage']
        # exclude = ['rv_crew']
        read_only_fields = ['rv_key', 'rv_rdt']

    def create(self, validated_data):
        nakwaDetails = validated_data.pop('nakwa', [])
        ownerDetails = validated_data.pop('owner')
        rvessel = Rvessels.objects.create(**validated_data)
        for nakwa in nakwaDetails:
            Rvcrews.objects.create(**nakwa, rvc_rv_key=rvessel)
        for owner in ownerDetails:
            Rvowners.objects.create(**owner, rvo_rv_key=rvessel)
        return rvessel


class RvesselViewSet(CustomViewSet):
    queryset = Rvessels.objects.all()
    serializer_class = RvesselSerializer

    filterset_fields = {
        'rv_key': ['exact', 'gte', 'lte'],
        'rv_id': ['exact'],
        'rv_pf_id': ['exact'],
        'rv_name': ['exact'],
        'rv_type': ['exact'],
        'rv_regno': ['exact'],
        'rv_rdt': ['exact', 'gte', 'lte', 'gt', 'lt']
    }
    search_fields = ['rv_id', 'rv_name', 'rv_regno']
    ordering_fields = ['rv_key', 'rv_rdt']
    ordering = ['-rv_key']

