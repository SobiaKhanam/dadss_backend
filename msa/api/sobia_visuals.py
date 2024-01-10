from django.http import JsonResponse
from rest_framework.decorators import api_view, action
from .models import *
from .feedsModels import Trip
from django.db.models import Q, Sum, F, Count, Max
from postgis import Geometry
import csv
from django.core.files.base import ContentFile
from rest_framework import viewsets, serializers, status
from django.core.files.storage import FileSystemStorage
from rest_framework.response import Response
import datetime
from dateutil.parser import parse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from collections import defaultdict


@api_view(http_method_names=['GET'])
# not using currently
def anti_narcotics(request):
   #http://127.0.0.1:8000/anti_narcotics?date_from=2023-03-01&&date_to=2023-05-01
    #date_from = request.GET.get('date_from')
    #date_to = request.GET.get('date_to')
    #sreports = Sreports.objects.filter(Q(sreport_goods__srg_category__icontains='Narcotics'),
     #                                  sr_dtg__range=(date_from, date_to)).distinct()
    sreports = Sreports.objects.filter(Q(sreport_goods__srg_category__icontains='Narcotics')).distinct()
    data = []

    for sreport in sreports:
        platform = Platforms.objects.get(pf_id=sreport.sr_pf_id)
        rvessels = Rvessels.objects.get(rv_id=sreport.sr_rv_key)
        total_quantity = Srgoods.objects.filter(srg_sr_key=sreport.sr_key).values('srg_category').annotate(total_quantity=Sum('srg_qty'))
        total_value = Srgoods.objects.filter(srg_sr_key=sreport.sr_key).values('srg_category').annotate(total_value=Sum('srg_value'))
        #total_category = Srgoods.objects.filter(srg_sr_key=sreport.sr_key, srg_category__icontains='Narcotics').values_list('srg_category', flat=True)

        jsonArray = {
            'dtg': datetime.strftime(sreport.sr_dtg, "%Y-%m-%d"),
            'latitude': Geometry.from_ewkb(sreport.sr_position).coords[0],
            'longitude': Geometry.from_ewkb(sreport.sr_position).coords[1],
            'total_value': total_value[0]['total_value'] if total_value else None,
            'total_qty': total_quantity[0]['total_quantity'] if total_quantity else None,
            #'total_category': " ".join(total_category),
            'pf_name': platform.pf_name,
            'pf_id': sreport.sr_pf_id,
            'rv_name': rvessels.rv_name,
            'rv_id': sreport.sr_rv_key,
        }

        data.append(jsonArray)

    return JsonResponse(data, safe=False)


@api_view(http_method_names=['GET'])
# not using currently
def contrabands(request):
    sreports = Sreports.objects.filter(Q(sreport_goods__srg_remarks__icontains='Contraband')).distinct()
    data = []

    for sreport in sreports:
        platform = Platforms.objects.get(pf_id=sreport.sr_pf_id)
        rvessels = Rvessels.objects.get(rv_id=sreport.sr_rv_key)
        total_quantity = Srgoods.objects.filter(srg_sr_key=sreport.sr_key).values('srg_remarks').annotate(
            total_quantity=Sum('srg_qty'))
        total_value = Srgoods.objects.filter(srg_sr_key=sreport.sr_key).values('srg_remarks').annotate(
            total_value=Sum('srg_value'))
        # total_category = Srgoods.objects.filter(srg_sr_key=sreport.sr_key, srg_category__icontains='Narcotics').values_list('srg_category', flat=True)

        jsonArray = {
            'dtg': datetime.strftime(sreport.sr_dtg, "%Y-%m-%d"),
            'latitude': Geometry.from_ewkb(sreport.sr_position).coords[0],
            'longitude': Geometry.from_ewkb(sreport.sr_position).coords[1],
            'total_value': total_value[0]['total_value'] if total_value else None,
            'total_qty': total_quantity[0]['total_quantity'] if total_quantity else None,
            # 'total_category': " ".join(total_category),
            'pf_name': platform.pf_name,
            'pf_id': sreport.sr_pf_id,
            'rv_name': rvessels.rv_name,
            'rv_id': sreport.sr_rv_key,
        }

        data.append(jsonArray)

    return JsonResponse(data, safe=False)


@api_view(http_method_names=['GET'])
# not using currently
def trip(request):
    boat_name = request.GET.get('boat_name')

    if boat_name:
        trips = Trip.objects.filter(boat_name=boat_name)
        longest_trip = trips.annotate(trip_duration=F('arrival_date') - F('departure_date')).order_by('-trip_duration')\
            .values('trip_duration', 'departure_date', 'arrival_date').first()

        response_data = {
            "boat_name": boat_name,
            "total_trips": trips.count(),
            "longest_trip_duration": longest_trip['trip_duration'].days if longest_trip else 0,
            "longest_trip_departure": str(longest_trip['departure_date']) if longest_trip else None,
            "longest_trip_arrival": str(longest_trip['arrival_date']) if longest_trip else None
        }

    else:
        boats = Trip.objects.values('boat_name').annotate(
            total_trips=Count('id'),
            longest_trip_duration=Max(F('arrival_date') - F('departure_date')),
            longest_trip_departure=Max('departure_date'),
            longest_trip_arrival=Max('arrival_date')
        )

        # Retrieve aggregated data for graph plotting
        # total_trips = [boat['total_trips'] for boat in boats if boat['total_trips'] <= 600]
        # longest_trip_durations = [boat['longest_trip_duration'].days if boat['longest_trip_duration'] and boat[
            # 'longest_trip_duration'].days <= 1000 else 0 for boat in boats if boat['total_trips'] <= 600]

        response_data = [{
            "boat_name": boat['boat_name'],
            "total_trips": boat['total_trips'],
            "longest_trip_duration": boat['longest_trip_duration'].days if boat['longest_trip_duration'] else 0,
            "longest_trip_departure": str(boat['longest_trip_departure']) if boat['longest_trip_departure'] else None,
            "longest_trip_arrival": str(boat['longest_trip_arrival']) if boat['longest_trip_arrival'] else None
        } for boat in boats]

    # Plotting code
    # plt.figure(figsize=(12, 8))
    # plt.scatter(total_trips, longest_trip_durations, marker='o', color='blue',
    #                 s=30)  # Adjust point size (s) as needed
    #
    # plt.xlabel('Number of Trips', fontsize=12)  # Adjust font size as needed
    # plt.ylabel('Longest Trip Duration (days)', fontsize=12)  # Adjust font size as needed
    # plt.title('Longest Trip Duration vs Number of Trips', fontsize=14)  # Adjust font size as needed
    #
    # plt.xticks(fontsize=10)  # Adjust x-axis tick font size as needed
    # plt.yticks(fontsize=10)  # Adjust y-axis tick font size as needed
    #
    # plt.tight_layout()  # Adjust the plot layout
    # plt.show()

    return JsonResponse(response_data, safe=False)


@api_view(http_method_names=['GET'])
def overstay(request):
    boat_location = request.GET.get('boat_location')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if boat_location:
        overstayed_boats = Trip.objects.filter(arrival_date__gt=F('pc_date'), boat_location=boat_location)

        if date_from and date_to:
            overstayed_boats = overstayed_boats.filter(arrival_date__range=[date_from, date_to])

        response_data = [{
            "id": boat.id,
            "boat_name": boat.boat_name,
            "pc_date": boat.pc_date,
            "arrival_date": boat.arrival_date,
            "overstay_duration": (boat.arrival_date - boat.pc_date).days
        } for boat in overstayed_boats]

        return JsonResponse(response_data, safe=False)

    else:
        boat_locations = Trip.objects.values('boat_location').distinct()
        response_data = {
            location['boat_location']: Trip.objects.filter(arrival_date__gt=F('pc_date'),
                                                           boat_location=location['boat_location'],
                                                           arrival_date__range=[date_from, date_to]).count()
            if date_from and date_to else
            Trip.objects.filter(arrival_date__gt=F('pc_date'),
                                boat_location=location['boat_location']).count()
            for location in boat_locations
        }
        return JsonResponse(response_data, safe=False)


@api_view(http_method_names=['GET'])
def trip_duration(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    trips = Trip.objects.annotate(trip_duration=F('arrival_date') - F('departure_date'))

    # Apply date range filter if both date_from and date_to are provided
    if date_from and date_to:
        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        date_to = datetime.strptime(date_to, '%Y-%m-%d')
        trips = trips.filter(departure_date__range=(date_from, date_to))

    less_than_15_days = trips.filter(trip_duration__lt=timedelta(days=15)).count()
    between_15_and_30_days = trips.filter(trip_duration__range=(timedelta(days=15), timedelta(days=30))).count()
    greater_than_30_days = trips.filter(trip_duration__gt=timedelta(days=30)).count()

    response_data = {
        "less than 15 days": less_than_15_days,
        "between 15 and 30 days": between_15_and_30_days,
        "greater than 30 days": greater_than_30_days
    }

    return JsonResponse(response_data)


@api_view(http_method_names=['GET'])
def trip_count(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    date_from = datetime.strptime(date_from, '%Y-%m-%d')
    date_to = datetime.strptime(date_to, '%Y-%m-%d')

    response = []
    num_days = (date_to - date_from).days + 1
    if num_days > 90:
        grouping_level = 'month'
    else:
        grouping_level = 'day'

    if grouping_level == 'month':
        increment = relativedelta(months=1)
    else:
        increment = timedelta(days=1)

    trips = Trip.objects.filter(departure_date__range=(date_from, date_to))
    current_date = date_from
    while current_date <= date_to:
        year = current_date.year
        month = current_date.month
        day = current_date.day

        item = {'Year': year, 'Month': datetime.strftime(current_date, '%B')}
        if grouping_level == 'day':
            item['Date'] = day

        if grouping_level == 'month':
            filtered_trips = trips.filter(departure_date__year=year, departure_date__month=month)
        else:
            filtered_trips = trips.filter(departure_date=current_date)

        counts = filtered_trips.values('boat_location').annotate(count=Count('boat_location')).order_by('boat_location')
        for count in counts:
            item[count['boat_location']] = count['count']

        all_possible_locations = Trip.objects.values_list('boat_location', flat=True).distinct()
        for location in all_possible_locations:
            if location not in item:
                item[location] = 0

        response.append(item)
        current_date += increment

    return JsonResponse(response, safe=False)


@api_view(http_method_names=['GET'])
def overstay_month(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
    date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
    duration = (date_to - date_from).days

    all_boat_locations = Trip.objects.values_list('boat_location', flat=True).distinct()
    response_data = []
    current_date = date_from
    while current_date <= date_to:
        if duration < 90:
            next_date = current_date + timedelta(days=1)
            date_range_label = current_date.strftime("%d-%B-%Y")
        else:
            next_date = current_date.replace(month=current_date.month % 12 + 1, day=1) if current_date.month < 12 else current_date.replace(year=current_date.year + 1, month=1, day=1)
            date_range_label = current_date.strftime("%B %Y")

        overstays = {location: 0 for location in all_boat_locations}
        ships = Trip.objects.filter(arrival_date__range=(current_date, next_date - timedelta(days=1)), arrival_date__gt=F('pc_date'))
        for ship in ships:
            boat_location = ship.boat_location
            overstays[boat_location] += 1

        data_item = {"date": date_range_label, **overstays}
        response_data.append(data_item)
        current_date = next_date

    return JsonResponse(response_data, safe=False)


# import csv data into the database
fs = FileSystemStorage(location='tmp/')


class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = "__all__"

'''
class TripViewset(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    @action(detail=False, methods=['GET', 'POST'])
    def upload_data(self, request):
        file = request.FILES["file"]
        content = file.read()
        file_content = ContentFile(content)
        file_name = fs.save("_tmp.csv", file_content)
        tmp_file = fs.path(file_name)
        csv_file = open(tmp_file, errors="ignore")

        #file = request.GET.get('file')
        #file_path = urllib.parse.unquote(file)
        #csv_file = open(file_path, errors="ignore")

        reader = csv.reader(csv_file)
        next(reader)

        trip_list = []
        existing_or_discarded_rows = 0

        for row in reader:
            (
                reg_no,
                reg_date,
                boat_name,
                boat_type,
                boat_location,
                departure_date,
                pc_date,
                arrival_date,
            ) = row

            # Check for null values in the row
            # if any(value is None or value.strip() == '' for value in row):
            #     existing_or_discarded_rows += 1
            #     continue

            # Convert date fields to the desired format (YYYY-MM-DD)
            try:
                reg_date = parse(reg_date, dayfirst=True).strftime("%Y-%m-%d")
                departure_date = parse(departure_date, dayfirst=True).strftime("%Y-%m-%d")
                pc_date = parse(pc_date, dayfirst=True).strftime("%Y-%m-%d")
                arrival_date = parse(arrival_date, dayfirst=True).strftime("%Y-%m-%d")
            except ValueError:
                # If there's an error parsing the date, skip the row
                existing_or_discarded_rows += 1
                continue

            # Check if the row already exists in the database based on boat_name and departure_date
            exists = Trip.objects.filter(
                Q(boat_name=boat_name) &
                Q(departure_date=departure_date)
            ).exists()

            if exists:
                existing_or_discarded_rows += 1
            else:
                trip = Trip(
                    reg_no=reg_no,
                    reg_date=reg_date,
                    boat_name=boat_name,
                    boat_type=boat_type,
                    boat_location=boat_location,
                    departure_date=departure_date,
                    pc_date=pc_date,
                    arrival_date=arrival_date,
                )
                trip_list.append(trip)

        Trip.objects.bulk_create(trip_list)

        response_data = {
            "message": "Successfully uploaded the data.",
            "existing_or_discarded_rows": existing_or_discarded_rows,
        }
        return Response(response_data)
'''


class TripViewset(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = file.read()
            file_content = ContentFile(content)
            file_name = fs.save("_tmp.csv", file_content)
            tmp_file = fs.path(file_name)
            csv_file = open(tmp_file, errors="ignore")

            reader = csv.reader(csv_file)
            next(reader)

            trip_list = []
            existing_or_discarded_rows = 0
            error_messages = []

            for row in reader:
                (
                    reg_no,
                    reg_date,
                    boat_name,
                    boat_type,
                    boat_location,
                    departure_date,
                    pc_date,
                    arrival_date,
                ) = row

                try:
                    reg_date = parse(reg_date, dayfirst=True).strftime("%Y-%m-%d")
                    departure_date = parse(departure_date, dayfirst=True).strftime("%Y-%m-%d")
                    pc_date = parse(pc_date, dayfirst=True).strftime("%Y-%m-%d")
                    arrival_date = parse(arrival_date, dayfirst=True).strftime("%Y-%m-%d")
                except ValueError as e:
                    # If there's an error parsing the date, skip the row and record the error
                    error_messages.append(f"Error parsing date in row: {e}")
                    existing_or_discarded_rows += 1
                    continue

                exists = Trip.objects.filter(
                    Q(boat_name=boat_name) &
                    Q(departure_date=departure_date)
                ).exists()

                if exists:
                    existing_or_discarded_rows += 1
                else:
                    trip = Trip(
                        reg_no=reg_no,
                        reg_date=reg_date,
                        boat_name=boat_name,
                        boat_type=boat_type,
                        boat_location=boat_location,
                        departure_date=departure_date,
                        pc_date=pc_date,
                        arrival_date=arrival_date,
                    )
                    trip_list.append(trip)

            Trip.objects.bulk_create(trip_list)

            response_data = {
                "message": "Successfully uploaded the data.",
                "existing_or_discarded_rows": existing_or_discarded_rows,
                "error_messages": error_messages
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(http_method_names=['GET'])
def leave_enter(request):
    date_from_str = request.GET.get('date_from')
    date_to_str = request.GET.get('date_to')
    boat_location = request.GET.get('boat_location')

    # Parse date strings to datetime objects
    date_from = datetime.strptime(date_from_str, "%Y-%m-%d")
    date_to = datetime.strptime(date_to_str, "%Y-%m-%d")

    # Calculate the duration between date_from and date_to
    duration = (date_to - date_from).days

    data = []
    current_date = date_from

    while current_date <= date_to:
        if duration < 90:
            next_date = current_date + timedelta(days=1)
            date_range_label = current_date.strftime("%d-%B-%Y")
        else:
            next_date = current_date.replace(month=current_date.month % 12 + 1, day=1) if current_date.month < 12 else current_date.replace(year=current_date.year + 1, month=1, day=1)
            date_range_label = current_date.strftime("%B %Y")

        # Filter based on boat_location if provided
        if boat_location:
            departures = Trip.objects.filter(
                Q(departure_date__range=(current_date, next_date - timedelta(days=1))) &
                Q(boat_location=boat_location)
            ).count()

            arrivals = Trip.objects.filter(
                Q(arrival_date__range=(current_date, next_date - timedelta(days=1))) &
                Q(boat_location=boat_location)
            ).count()
        else:
            departures = Trip.objects.filter(departure_date__range=(current_date, next_date - timedelta(days=1))).count()
            arrivals = Trip.objects.filter(arrival_date__range=(current_date, next_date - timedelta(days=1))).count()

        data.append({
            "date": date_range_label,
            "departures": -1 * departures,
            "arrivals": arrivals
        })

        current_date = next_date

    return JsonResponse(data, safe=False)


@api_view(http_method_names=['GET'])
def fv_leave_enter(request):
    date_from_str = request.GET.get('date_from')
    date_to_str = request.GET.get('date_to')
    boat_location = request.GET.get('boat_location')

    # Parse date strings to date objects
    date_from = datetime.strptime(date_from_str, "%Y-%m-%d").date()
    date_to = datetime.strptime(date_to_str, "%Y-%m-%d").date()

    data = defaultdict(lambda: defaultdict(lambda: {"arrivals": 0, "departures": 0}))

    # Get all distinct boat_location values from the database
    all_possible_boat_locations = Trip.objects.values_list('boat_location', flat=True).distinct()

    current_date = date_from
    while current_date <= date_to:
        next_date = current_date.replace(day=28) + timedelta(days=4)
        next_date = next_date - timedelta(days=next_date.day)

        month = current_date.strftime("%B")
        year = current_date.strftime("%Y")

        # Filter based on boat_location if provided
        if boat_location:
            trips = Trip.objects.filter(
                Q(departure_date__range=(current_date, next_date)) |
                Q(arrival_date__range=(current_date, next_date)),
                Q(boat_location=boat_location)
            )
        else:
            trips = Trip.objects.filter(
                Q(departure_date__range=(current_date, next_date)) |
                Q(arrival_date__range=(current_date, next_date))
            )

        for trip in trips:
            if trip.departure_date and current_date <= trip.departure_date <= next_date:
                data[(year, month)][trip.boat_location]["departures"] += 1
            if trip.arrival_date and current_date <= trip.arrival_date <= next_date:
                data[(year, month)][trip.boat_location]["arrivals"] += 1

        current_date = next_date + timedelta(days=1)

    response_data = []
    # response_data.append({"boat_locations": list(all_possible_boat_locations)})
    for year_month, location_data in data.items():
        year, month = year_month
        month_data = {"date": f"{month}, {year}"}

        for boat_location in all_possible_boat_locations:
            stats = location_data.get(boat_location, {"arrivals": 0, "departures": 0})
            month_data[boat_location] = {
                "arrivals": stats["arrivals"],
                "departures": stats["departures"]
            }

        response_data.append(month_data)

    return JsonResponse(response_data, safe=False)


'''
@api_view(http_method_names=['GET'])
def fv_leave_enter(request):
    date_from_str = request.GET.get('date_from')
    date_to_str = request.GET.get('date_to')
    boat_location = request.GET.get('boat_location')

    # Parse date strings to date objects
    date_from = datetime.strptime(date_from_str, "%Y-%m-%d").date()
    date_to = datetime.strptime(date_to_str, "%Y-%m-%d").date()

    data = defaultdict(lambda: defaultdict(lambda: {"arrivals": 0, "departures": 0}))

    # Get the top 10 distinct boat_location values based on trip count
    top_10_boat_locations = Trip.objects.values('boat_location').annotate(
        trip_count=Count('id')
    ).order_by('-trip_count')[:10]

    top_10_boat_locations = [entry['boat_location'] for entry in top_10_boat_locations]

    current_date = date_from
    while current_date <= date_to:
        next_date = current_date.replace(day=28) + timedelta(days=4)
        next_date = next_date - timedelta(days=next_date.day)

        month = current_date.strftime("%B")
        year = current_date.strftime("%Y")

        # Filter based on boat_location if provided
        if boat_location:
            trips = Trip.objects.filter(
                Q(departure_date__range=(current_date, next_date)) |
                Q(arrival_date__range=(current_date, next_date)),
                Q(boat_location=boat_location)
            )
        else:
            trips = Trip.objects.filter(
                Q(departure_date__range=(current_date, next_date)) |
                Q(arrival_date__range=(current_date, next_date))
            )

        for trip in trips:
            if trip.departure_date and current_date <= trip.departure_date <= next_date:
                if trip.boat_location in top_10_boat_locations:
                    data[(year, month)][trip.boat_location]["departures"] += 1
            if trip.arrival_date and current_date <= trip.arrival_date <= next_date:
                if trip.boat_location in top_10_boat_locations:
                    data[(year, month)][trip.boat_location]["arrivals"] += 1

        current_date = next_date + timedelta(days=1)

    response_data = []
    response_data.append({"boat_locations": list(top_10_boat_locations)})
    for year_month, location_data in data.items():
        year, month = year_month
        month_data = {"date": f"{month}, {year}"}

        for boat_location in top_10_boat_locations:
            stats = location_data.get(boat_location, {"arrivals": 0, "departures": 0})
            month_data[boat_location] = {
                "arrivals": stats["arrivals"],
                "departures": stats["departures"]
            }

        response_data.append(month_data)

    return JsonResponse(response_data, safe=False)
'''


@api_view(http_method_names=['GET'])
def boat_location_stats(request):
    date_from_str = request.GET.get('date_from')
    date_to_str = request.GET.get('date_to')
    boat_location = request.GET.get('boat_location')

    # Parse date strings to date objects
    date_from = datetime.strptime(date_from_str, "%Y-%m-%d").date()
    date_to = datetime.strptime(date_to_str, "%Y-%m-%d").date()

    data = defaultdict(lambda: defaultdict(lambda: {"arrivals": 0, "departures": 0}))

    all_possible_boat_locations = Trip.objects.values_list('boat_location', flat=True).distinct()

    current_date = date_from
    while current_date <= date_to:
        next_date = current_date.replace(day=28) + timedelta(days=4)
        next_date = next_date - timedelta(days=next_date.day)

        month = current_date.strftime("%B")
        year = current_date.strftime("%Y")

        for boat_location in all_possible_boat_locations:
            if boat_location not in data:
                data[boat_location] = defaultdict(lambda: {"arrivals": 0, "departures": 0})
            data[boat_location][(year, month)] = {"arrivals": 0, "departures": 0}

        if boat_location:
            trips = Trip.objects.filter(
                Q(departure_date__range=(current_date, next_date)) |
                Q(arrival_date__range=(current_date, next_date)),
                Q(boat_location=boat_location)
            )
        else:
            trips = Trip.objects.filter(
                Q(departure_date__range=(current_date, next_date)) |
                Q(arrival_date__range=(current_date, next_date))
            )

        for trip in trips:
            if trip.departure_date and current_date <= trip.departure_date <= next_date:
                data[trip.boat_location][(year, month)]["departures"] += 1
            if trip.arrival_date and current_date <= trip.arrival_date <= next_date:
                data[trip.boat_location][(year, month)]["arrivals"] += 1

        current_date = next_date + timedelta(days=1)

    response_data = []
    for boat_location, location_data in data.items():
        boat_location_info = {"boat_location": boat_location, "data": []}
        for year_month, stats in location_data.items():
            year, month = year_month
            boat_location_info["data"].append({
                "date": f"{month}, {year}",
                "arrivals": stats["arrivals"],
                "departures": stats["departures"]
            })
        response_data.append(boat_location_info)

    return JsonResponse(response_data, safe=False)
