from rest_framework import serializers
from .intel_models import IntelReportDetails, IntelReport
from msa.api.parent import CustomViewSet


class IRDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntelReportDetails
        fields = '__all__'
        read_only_fields = ['ird_key']


class IreportSerializer(serializers.ModelSerializer):
    intelreportdetails = IRDetailsSerializer(many=True, source='irdetails', required=False)

    class Meta:
        model = IntelReport
        fields = '__all__'
        read_only_fields = ['ir_key', 'ir_rdt']

    def create(self, validated_data):
        intelreportdetails = validated_data.pop('irdetails', [])
        ireport = IntelReport.objects.create(**validated_data)

        for irdetails in intelreportdetails:
            IntelReportDetails.objects.create(ird_ir_key=ireport, **irdetails)
        return ireport


class IreportViewSet(CustomViewSet):
    queryset = IntelReport.objects.all()
    serializer_class = IreportSerializer

    filterset_fields = {
        'ir_key': ['exact', 'gte', 'lte'],
        'ir_reporting_time': ['exact', 'gte', 'lte', 'gt', 'lt'],
        'ir_pf_id': ['exact'],
        'ir_rdt': ['exact', 'gte', 'lte', 'gt', 'lt']
    }
    search_fields = ['ir_reporter_name', 'ir_jetty']
    ordering_fields = ['ir_key', 'ir_rdt', 'ir_reporting_time']
    ordering = ['-ir_key']


class IRDetailsViewSet(CustomViewSet):
    queryset = IntelReportDetails.objects.all()
    serializer_class = IRDetailsSerializer
