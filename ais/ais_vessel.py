from .parent import *
from .ais_models import *
from django.utils import timezone
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from .ais_serializers import MerchantVesselSerializer, VesselTripSerializer, TripDetailsSerializer
from rest_framework import generics
from rest_framework.filters import SearchFilter


class AISVesselSerializer(serializers.ModelSerializer):
    mv_data_source = serializers.HiddenField(default='registered_merchant')

    class Meta:
        model = Merchant_Vessel
        fields = '__all__'
        read_only_fields = ['mv_key']

    def create(self, validated_data):
        mv_imo = validated_data.get('mv_imo')
        existing_vessel = Merchant_Vessel.objects.filter(mv_imo=mv_imo).first()
        if existing_vessel:
            raise serializers.ValidationError({'error': 'IMO is already registered'})
        aisvessel = Merchant_Vessel.objects.create(**validated_data)
        return aisvessel


class AISVesselViewSet(CustomViewSet):
    serializer_class = AISVesselSerializer

    filterset_fields = {
        'mv_key': ['exact'],
        'mv_imo': ['exact'],
        'mv_ship_id': ['exact'],
        'mv_ship_name': ['exact'],
    }
    search_fields = ['mv_imo', 'mv_ship_name', 'mv_mmsi']

    def get_queryset(self):
        queryset = Merchant_Vessel.objects.all()
        queryset = queryset.order_by('-mv_key')
        mv_key = self.kwargs.get('pk')

        if mv_key is not None:
            return queryset.filter(mv_key=mv_key)

        if self.request.query_params.get('search', '').strip():
            return self.filter_queryset(queryset)

        return queryset[:100]


class SrgoodSerializer(serializers.ModelSerializer):
    msrg_qty = serializers.IntegerField()
    msrg_value = serializers.IntegerField()

    class Meta:
        model = MerSrgoods
        exclude = ['msrg_msr_key']


class MerchantTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerSreports2
        exclude = ['msr_key']


class CustomSrSerializer(serializers.ModelSerializer):
    trip_source = None
    child = None
    primary_key = None
    msr_rdt = serializers.DateTimeField(default=timezone.now)
    msr_position = PositionField()
    goodDetails = SrgoodSerializer(many=True, source='goods')

    class Meta:
        model = MerSreports
        fields = '__all__'
        read_only_fields = ['msr_key', 'msr_rdt']

    def create(self, validated_data):
        trip = validated_data.pop(self.trip_source)
        goodDetails = validated_data.pop('goods')
        special_report = MerSreports.objects.create(**validated_data)
        self.child.objects.create(**trip, msr_key=special_report)
        for good in goodDetails:
            MerSrgoods.objects.create(**good, msrg_msr_key=special_report)
        return special_report


class MerchantSerializer(CustomSrSerializer):
    trip_source = 'merchant_trip'
    child = MerSreports2
    tripDetails = MerchantTripSerializer(many=False, source=trip_source)

    class Meta:
        model = MerSreports
        fields = '__all__'
        read_only_fields = ['msr_key', 'msr_rdt']


class CustomSrViewSet(CustomViewSet):
    filterset_fields = ['msr_key', 'msr_pf_id', 'msr_mv_key', 'msr_dtg', 'msr_movement', 'msr_action']

    ordering = ['-msr_key']

    @action(methods=['get'], detail=False, url_path='mv_key/(?P<msr_mv_key>[^/.]+)')
    def mv_key(self, request, pk=None, msr_mv_key=None):
        """
            Redirect to Register Vessel object if special report is empty.
        """
        # Request
        path = (request.get_full_path()).split('/')[1]
        tripDetails = 'tripDetails'
        goodDetails = 'goodDetails'
        filter_query = self.queryset.filter(msr_mv_key=msr_mv_key).last()
        if filter_query is None:
            mervessel_object = get_object_or_404(Merchant_Vessel, mv_key=msr_mv_key)
            mervessel = AISVesselSerializer(mervessel_object, many=False).data
            mervessel_updated = {'mv_key': mervessel['mv_key']}
            return Response(mervessel_updated)
        else:
            if path == 'merchant':
                sreport = MerchantSerializer(filter_query, many=False).data
            sreport_updated = {'msr_key': sreport['msr_key'], 'msr_mv_key': sreport['msr_mv_key'],
                               'msr_movement': sreport['msr_movement'], goodDetails: sreport[goodDetails],
                               tripDetails: sreport[tripDetails]}
            return Response(sreport_updated)


class MerchantViewSet(CustomSrViewSet):
    queryset = MerSreports.objects.all()
    serializer_class = MerchantSerializer


class MerchantVesselList(generics.ListAPIView):
    queryset = Merchant_Vessel.objects.all().order_by('-mv_key')
    serializer_class = MerchantVesselSerializer
    filter_backends = [SearchFilter]
    search_fields = ['mv_imo']


class MerchantTripList(generics.ListAPIView):
    serializer_class = VesselTripSerializer

    def get_queryset(self):
        mv_key = self.kwargs['mv_key']
        return Merchant_Trip.objects.filter(mt_mv_key__mv_key=mv_key).order_by('-mt_key')


class TripDetailsList(generics.ListAPIView):
    serializer_class = TripDetailsSerializer

    def get_queryset(self):
        mtd_mt_key = self.kwargs['mtd_mt_key']
        return Trip_Details.objects.filter(mtd_mt_key__mt_key=mtd_mt_key).order_by('-mtd_key')
