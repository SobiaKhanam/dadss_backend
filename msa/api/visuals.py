from django.http import JsonResponse
from rest_framework.decorators import api_view
import random
from datetime import timedelta, datetime
from .feedsModels import *


@api_view(http_method_names=['GET'])
def fv_con(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    season = request.GET.get('season')
    harbor = request.GET.get('harbor')
    vessel_type = request.GET.get('type')
    print(date_from, date_to, season, harbor, vessel_type)

    if date_from or date_to:
        queryset = Fdensity.objects.filter(date__range=[date_from, date_to])
    else:
        queryset = Fdensity.objects.all()

    queryset = list(queryset.values())

    jsonArray = []

    for data in queryset:
        latitude = round(int(data['latitude']) + ((data['latitude'] - int(data['latitude'])) / 6), 5)
        longitude = round(int(data['longitude']) + ((data['longitude'] - int(data['longitude'])) / 6), 5)
        jsonArray.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [longitude, latitude],
            },
            "properties": {
                "intensity": data['no_vessels'],
            },
        })

    return JsonResponse(jsonArray, safe=False)


@api_view(http_method_names=['GET'])
def mv_visiting(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    vessel_type = request.GET.get('type')
    print(date_from, date_to, vessel_type)

    jsonArray = {
        "crossed": random.randint(50, 100),
        "KPT": random.randint(30, 60),
        "GWADAR": random.randint(40, 70),
        "PQA": random.randint(10, 40),
    }

    return JsonResponse(jsonArray, safe=False)


@api_view(http_method_names=['GET'])
def mv_visiting_monthly(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    vessel_type = request.GET.get('type')
    print(date_from, date_to, vessel_type)

    startDate = datetime.strptime(date_from, '%Y-%m-%d').date()
    endDate = datetime.strptime(date_to, '%Y-%m-%d').date()
    months = (endDate.year - startDate.year) * 12 + (endDate.month - startDate.month)

    jsonArray = []
    for i in range(0, months + 1):
        jsonArray.append({
            "date": (startDate + timedelta(days=i * 31)).strftime("%Y-%m"),
            "crossed": random.randint(50, 100),
            "KPT": random.randint(30, 60),
            "GWADAR": random.randint(40, 70),
            "PQA": random.randint(10, 40),
        }, )

    return JsonResponse(jsonArray, safe=False)


@api_view(http_method_names=['GET'])
def narco(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    qty_gte = request.GET.get('qty_gte')
    qty_lte = request.GET.get('qty_lte')
    value_gte = request.GET.get('value_gte')
    value_lte = request.GET.get('value_lte')
    print(date_from, date_to, qty_gte, qty_lte, value_gte, value_lte)

    if date_from or date_to:
        queryset = Narco.objects.filter(dtg__range=[date_from, date_to]).order_by('dtg')
    else:
        queryset = Narco.objects.order_by('dtg')
        
    if qty_gte:
        queryset = queryset.filter(quantity__gte=qty_gte)
    if qty_lte:
        queryset = queryset.filter(quantity__gte=qty_lte)
    if value_gte:
        queryset = queryset.filter(value__gte=value_gte)
    if value_lte:
        queryset = queryset.filter(value__gte=value_lte)
    queryset = list(queryset.values())

    jsonArray = []
    for data in queryset:
        jsonArray.append({
            "dtg": data['dtg'],
            "latitude": data['latitude'],
            "longitude": data['longitude'],
            "value": data['value'],
            "flag": data['flag'],
            "item": data['item'],
            "quantity": data['quantity'],
            "vessel_name": data['vessel_name'],
            "pf_name": "SINC",
            "pf_id": "515151"
        })

    return JsonResponse(jsonArray, safe=False)
