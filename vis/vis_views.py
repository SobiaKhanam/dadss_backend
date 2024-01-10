from django.http import JsonResponse, HttpResponse
from .vis_models import BoatTripLogs, Boats
from msa.api.models import Rvessels
import re
from rest_framework.decorators import api_view
from rest_framework import serializers
from msa.api.parent import CustomViewSet


@api_view(http_method_names=['GET'])
def query_data(request):
    queryset = BoatTripLogs.objects.using('maria').select_related('user_location').all()[:100]
    data = [{
        "boat_id": entry.boat_id,
        "nakwa_name": entry.nakwa_name,
        "crew": entry.crew,
        "departure_date": entry.dep_date,
        "pc_date": entry.pc_date,
        "arrival_date": entry.arrival_date,
    } for entry in queryset]

    return JsonResponse(data, safe=False)


class BoatTripLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoatTripLogs
        fields = ['boat_id', 'nakwa_name', 'crew', 'dep_date', 'pc_date', 'arrival_date']


class BoatTripLogsView(CustomViewSet):
    serializer_class = BoatTripLogsSerializer
    filterset_fields = {
        'boat_id': ['exact', 'gte', 'lte'],
        'nakwa_name': ['exact']
    }
    search_fields = ['boat_id', 'nakwa_name']

    def get_queryset(self):
        queryset = BoatTripLogs.objects.using('maria').select_related('user_location').all()
        queryset = queryset.order_by('-id')

        if self.request.query_params.get('search', '').strip():
            return self.filter_queryset(queryset)

        return queryset[:100]


boat_type_mapping = {
    1: "HORA",
    2: "LAUNCH",
    3: "HORA LAUNCH",
    4: "DUNDA",
    5: "DUNDA HORA",
    6: "PASSENGER BOAT",
    7: "HORI",
    8: "OIL BARGE",
    9: "WATER BARGE",
    10: "SUPPLY BOAT",
    11: "PILOT BOAT",
    12: "TUG",
    13: "SAILING BOAT",
    14: "TOWING BOAT",
    15: "STEEL DUMB BARGE",
    16: "YAKDAR",
    17: "CARGO DHOW",
    18: "KAIK",
    19: "DOW",
}


def replace_m_with_zeros(value):
    # If value is not None and contains "M" (case-insensitive), replace it with "000000"
    if value is not None:
        value = re.sub(r'[Mm]', '', value)

    if value is not None and "NIL" in value:
        value = value.replace("NIL", "0")
    return value


@api_view(http_method_names=['POST'])
def populate_rvessels(request):
    boats_entries = Boats.objects.using('maria').all()[:100]

    for boat_entry in boats_entries:
        boat_length = replace_m_with_zeros(boat_entry.boat_length)
        boat_breadth = replace_m_with_zeros(boat_entry.boat_breadth)
        boat_tonnage = replace_m_with_zeros(boat_entry.boat_tonnage)
        rvessels_entry = Rvessels(
            rv_name=boat_entry.boat_name,
            rv_id=boat_entry.old_id,
            rv_regno=boat_entry.reg_no,
            rv_type=boat_type_mapping.get(boat_entry.boat_type_id, None),
            rv_flag="PK",
            rv_province=None,
            rv_length=boat_length,
            rv_breadth=boat_breadth,
            rv_tonnage=boat_tonnage,
            rv_crew=None,
            rv_pf_id=None,
            rv_rdt=boat_entry.reg_date
        )
        rvessels_entry.save()

    return HttpResponse("Rvessels table populated with the first 100 entries from Boats.")
