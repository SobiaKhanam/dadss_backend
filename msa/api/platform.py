from .parent import *
from .models import *
from django.utils import timezone


class PlatformSerializer(serializers.ModelSerializer):
    pf_rdt = serializers.DateTimeField(default=timezone.now)
    pf_type = serializers.CharField(allow_blank=False, allow_null=False)

    class Meta:
        model = Platforms
        fields = '__all__'
        read_only_fields = ['pf_key', 'pf_rdt']


class PlatformViewSet(CustomViewSet):
    queryset = Platforms.objects.all()
    serializer_class = PlatformSerializer

    filterset_fields = {
        'pf_key': ['exact', 'gte', 'lte'],
        'pf_id': ['exact'],
        'pf_name': ['exact'],
        'pf_type': ['exact'],
        'pf_rdt': ['exact', 'gte', 'lte', 'gt', 'lt']
    }
    search_fields = ['pf_id', 'pf_name']
    ordering_fields = ['pf_key', 'pf_rdt']
    ordering = ['-pf_key']

    # ordering = ['-pf_key']


