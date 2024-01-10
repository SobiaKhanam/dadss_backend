from .models import *
from django.utils import timezone
from .parent import *
from rest_framework.parsers import MultiPartParser, FormParser
import csv
from ais.ais_models import *


class GrfishingSerializer(serializers.ModelSerializer):
    grf_position = PositionField()
    # fishing_csv_file = serializers.FileField(write_only=True, allow_empty_file=False, required=False)  # Add CSV file field

    class Meta:
        model = Grfishing
        fields = '__all__'
        read_only_fields = ['grf_key', 'grf_gr_key']

    # def create(self, validated_data):
    #     fishing_csv_file = validated_data.pop('fishing_csv_file', None)  # Get the CSV file if provided
    #
    #     # Create the Grfishing instance
    #     grfishing = Grfishing.objects.create(**validated_data)
    #
    #     # Handle CSV file upload for Grfishing
    #     if fishing_csv_file:
    #         csv_data = fishing_csv_file.read().decode('utf-8').splitlines()
    #         csv_dict_data = csv.DictReader(csv_data)
    #         for row in csv_dict_data:
    #             Grfishing.objects.create(grf_gr_key=grfishing.grf_gr_key, **row)
    #
    #     return grfishing


class GrmerchantSerializer(serializers.ModelSerializer):
    grm_position = PositionField()

    class Meta:
        model = Grmerchant
        # model = Merchant_Vessel
        fields = '__all__'
        # read_only_fields = ['grm_key', 'grm_gr_key']
        read_only_fields = ['mv_id', 'grm_gr_key']


class GrdensitySerializer(serializers.ModelSerializer):
    grd_position = PositionField()
    grd_qty = serializers.IntegerField()

    class Meta:
        model = Grdensity
        fields = '__all__'
        read_only_fields = ['grd_key', 'grd_gr_key']


'''
class GreportSerializer(serializers.ModelSerializer):
    # fishingVesselObserved = GrfishingSerializer(many=True, source='fishing')
    # merchantVesselObserved = GrmerchantSerializer(many=True, source='merchant')
    # fishingDensities = GrdensitySerializer(many=True, source='density')

    # Add FileFields for CSV uploads
    fishing_csv_file = serializers.FileField(write_only=True, allow_empty_file=False, required=False)
    merchant_csv_file = serializers.FileField(write_only=True, allow_empty_file=False, required=False)
    density_csv_file = serializers.FileField(write_only=True, allow_empty_file=False, required=False)

    class Meta:
        model = Greports
        fields = '__all__'
        read_only_fields = ['gr_key', 'gr_rdt']

    def create(self, validated_data):
        # Check if user-inserted data is provided
        user_inserted_fishing_data = validated_data.get('fishingVesselObserved')
        user_inserted_merchant_data = validated_data.get('merchantVesselObserved')
        user_inserted_density_data = validated_data.get('fishingDensities')

        # Check if CSV files are uploaded
        fishing_csv_file = validated_data.get('fishing_csv_file')
        merchant_csv_file = validated_data.get('merchant_csv_file')
        density_csv_file = validated_data.get('density_csv_file')

        # Create the Greports instance
        greport = Greports.objects.create(**validated_data)

        # Handle user-inserted data for fishing
        if user_inserted_fishing_data:
            for fishing_data in user_inserted_fishing_data:
                Grfishing.objects.create(grf_gr_key=greport, **fishing_data)

        # Handle user-inserted data for merchant
        if user_inserted_merchant_data:
            for merchant_data in user_inserted_merchant_data:
                # Grmerchant.objects.create(grm_gr_key=greport, **merchant_data)
                Merchant_Vessel.objects.create(grm_gr_key=greport, **merchant_data)

        # Handle user-inserted data for density
        if user_inserted_density_data:
            for density_data in user_inserted_density_data:
                Grdensity.objects.create(grd_gr_key=greport, **density_data)

        # Handle CSV file upload for fishing
        if fishing_csv_file:
            csv_data = fishing_csv_file.read().decode('utf-8').splitlines()
            csv_dict_data = csv.DictReader(csv_data)
            for row in csv_dict_data:
                Grfishing.objects.create(grf_gr_key=greport, **row)

        # Handle CSV file upload for merchant
        if merchant_csv_file:
            csv_data = merchant_csv_file.read().decode('utf-8').splitlines()
            csv_dict_data = csv.DictReader(csv_data)
            for row in csv_dict_data:
                # Grmerchant.objects.create(grm_gr_key=greport, **row)
                Merchant_Vessel.objects.create(grm_gr_key=greport, **row)

        # Handle CSV file upload for density
        if density_csv_file:
            csv_data = density_csv_file.read().decode('utf-8').splitlines()
            csv_dict_data = csv.DictReader(csv_data)
            for row in csv_dict_data:
                Grdensity.objects.create(grd_gr_key=greport, **row)

        return greport
'''


class GreportSerializer(serializers.ModelSerializer):
    gr_rdt = serializers.DateTimeField(default=timezone.now)
    gr_fuelrem = serializers.IntegerField()
    gr_position = PositionField()
    fishingVesselObserved = GrfishingSerializer(many=True, source='fishing')
    merchantVesselObserved = GrmerchantSerializer(many=True, source='merchant')
    fishingDensities = GrdensitySerializer(many=True, source='density')
    
    class Meta:
        model = Greports
        fields = '__all__'
        read_only_fields = ['gr_key', 'gr_rdt']

    def create(self, validated_data):
        fishingVesselObserved = validated_data.pop('fishing')
        merchantVesselObserved = validated_data.pop('merchant')
        fishingDensities = validated_data.pop('density')
        greport = Greports.objects.create(**validated_data)
        for fishing in fishingVesselObserved:
            Grfishing.objects.create(**fishing, grf_gr_key=greport)
        for merchant in merchantVesselObserved:
            Grmerchant.objects.create(**merchant, grm_gr_key=greport)
            # Merchant_Vessel.objects.create(**merchant, grm_gr_key=greport)
        for density in fishingDensities:
            Grdensity.objects.create(**density, grd_gr_key=greport)
        return greport


class GreportViewSet(CustomViewSet):
    queryset = Greports.objects.all()
    serializer_class = GreportSerializer

    # Allow file uploads in your views
    # parser_classes = (MultiPartParser, FormParser)

    filterset_fields = {
        'gr_key': ['exact', 'gte', 'lte'],
        'gr_dtg': ['exact', 'gte', 'lte', 'gt', 'lt'],
        'gr_pf_id': ['exact'],
        'gr_patroltype': ['exact'],
        'gr_fuelrem': ['exact', 'gte', 'lte', 'gt', 'lt'],
        'gr_rdt': ['exact', 'gte', 'lte', 'gt', 'lt']
    }
    search_fields = ['gr_pf_id', 'gr_patroltype']
    ordering_fields = ['gr_key', 'gr_rdt', 'gr_dtg']
    ordering = ['-gr_key']
