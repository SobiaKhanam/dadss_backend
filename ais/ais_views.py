from .ais_models import *
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, timedelta
import pandas as pd
from pytz import timezone
from rest_framework.decorators import api_view


@api_view(http_method_names=['GET'])
def stay_count(request):
    start_date_str = request.GET.get('date_from')
    end_date_str = request.GET.get('date_to')
    port = request.GET.get('port')

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    ship_data = Full_Data.objects.filter(timestamp__range=[start_date, end_date]).values('ship_id', 'current_port', 'timestamp').order_by('timestamp')

    # all_ships = Full_Data.objects.filter(timestamp__range=(start_date, end_date))
    # if port:
    #     all_ships = all_ships.filter(current_port=port)
    #
    # # Convert queryset to list of dictionaries
    # ship_data = list(all_ships.values())
    # Convert the data to a DataFrame
    ship_df = pd.DataFrame.from_records(ship_data)

    # Combine "KARACHI" and "KARACHI ANCH" into a single category "KARACHI" and same for PORT QASIM AND PORT QASIM ANCH
    ship_df['current_port'] = ship_df['current_port'].replace({'KARACHI ANCH': 'KARACHI', 'PORT QASIM ANCH': 'PORT QASIM'})

    # Filter data for provided port only
    karachi_data = ship_df[ship_df['current_port'] == port]

    # Group data by ship_id
    grouped_data = karachi_data.groupby('ship_id')

    # Calculate the duration for each group (first and last timestamp)
    port_durations = grouped_data.agg({'timestamp': ['first', 'last']})
    print(port_durations)

    # Calculate the duration in days
    port_durations['duration'] = (port_durations['timestamp']['last'] - port_durations['timestamp']['first']).dt.days

    # Calculate the number of days each ship stayed in Karachi
    days_counts = port_durations['duration'].value_counts().sort_index()

    # Create a dictionary for the JSON response
    response_data = {f"{days} day{'s' if days > 1 else ''}": count for days, count in days_counts.items()}

    # Create a dictionary for the JSON response and print ship_id
    # response_data = {}
    #
    # for days, count in days_counts.items():
    #     ship_ids = list(port_durations[port_durations['duration'] == days].index)
    #     response_data[f"{days} day{'s' if days > 1 else ''}"] = {"count": count, "ship_ids": ship_ids}

    return JsonResponse(response_data)


@api_view(http_method_names=['GET'])
def ship_counts(request):
    start_date_str = request.GET.get('date_from')
    end_date_str = request.GET.get('date_to')

    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    else:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7 * 7)

    # Filter the data based on the specified time period
    filtered_data = Full_Data.objects.filter(Q(timestamp__range=(start_date, end_date))).\
        values('ship_id', 'current_port').distinct()

    # Create a dictionary to count the ports
    port_counts = {
        "KARACHI": 0,
        "PORT QASIM": 0,
        "GWADAR": 0,
        "CROSSING": 0,
    }

    for item in filtered_data:
        current_port = item['current_port']
        if current_port in ['KARACHI', 'KARACHI ANCH']:
            port_counts['KARACHI'] += 1
        elif current_port in ['PORT QASIM', 'PORT QASIM ANCH']:
            port_counts['PORT QASIM'] += 1
        elif current_port == 'GWADAR':
            port_counts['GWADAR'] += 1
        elif current_port == '':
            port_counts['CROSSING'] += 1

    # Create a JSON response
    return JsonResponse(port_counts)


@api_view(http_method_names=['GET'])
def ship_counts_week(request):
    # Get the start and end dates from the request
    start_date_str = request.GET.get('date_from')
    end_date_str = request.GET.get('date_to')

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    # Calculate the number of weeks between start and end dates
    total_weeks = (end_date - start_date).days // 7 + 1

    # Create a list of dictionaries to store counts for each week
    weekly_counts = []

    # Iterate through each week and calculate counts
    for week in range(total_weeks):
        week_start = start_date + timedelta(weeks=week)
        week_end = week_start + timedelta(days=6)

        # Filter the data for the current week
        filtered_data = Full_Data.objects.filter(
            Q(timestamp__range=(week_start, week_end))
        ).values('ship_id', 'current_port').distinct()

        # Create a dictionary to count the ports
        port_counts = {
            "KARACHI": 0,
            "PORT QASIM": 0,
            "GWADAR": 0,
            "CROSSING": 0,
        }

        for item in filtered_data:
            current_port = item['current_port']
            if current_port in ['KARACHI', 'KARACHI ANCH']:
                port_counts['KARACHI'] += 1
            elif current_port in ['PORT QASIM', 'PORT QASIM ANCH']:
                port_counts['PORT QASIM'] += 1
            elif current_port == 'GWADAR':
                port_counts['GWADAR'] += 1
            elif current_port == '':
                port_counts['CROSSING'] += 1

        # Create a dictionary for the current week's counts
        weekly_count = {
            "Week Start": week_start.strftime('%Y-%m-%d'),
            "Week End": week_end.strftime('%Y-%m-%d'),
            "Counts": port_counts,
        }

        # Append the weekly counts to the list
        weekly_counts.append(weekly_count)

    # Create a JSON response with weekly counts
    return JsonResponse(weekly_counts, safe=False)


@api_view(http_method_names=['GET'])
def vessel_position(request):
    ship_id = request.GET.get('ship_id')

    if ship_id:
        ship_positions = Full_Data.objects.filter(ship_id=ship_id).order_by('-timestamp').values(
            'timestamp',
            'latitude',
            'longitude'
        )

        response_data = [
            {
                'timestamp': position['timestamp'].astimezone(timezone('Asia/Karachi')).strftime('%Y-%m-%d %H:%M:%S.%f %z'),
                'latitude': position['latitude'],
                'longitude': position['longitude']
            }
            for position in ship_positions
        ]
    else:
        latest_positions = Full_Data.objects.order_by('ship_id', '-timestamp').distinct('ship_id').values(
            'ship_id',
            'latitude',
            'longitude',
            'timestamp'
        )

        response_data = [
            {
                'ship_id': position['ship_id'],
                'latitude': position['latitude'],
                'longitude': position['longitude'],
                'timestamp': position['timestamp'].astimezone(timezone('Asia/Karachi')).strftime('%Y-%m-%d %H:%M:%S.%f %z')
            }
            for position in latest_positions
        ]

    return JsonResponse(response_data, safe=False)


@api_view(http_method_names=['POST'])
def populate_data(request):
    full_data_records = Full_Data.objects.all().order_by('timestamp')

    for row in full_data_records:
        Merchant_Vessel.objects.get_or_create(
            mv_imo=row.imo,
            mv_ship_id=row.ship_id,
            defaults={
                'mv_mmsi': row.mmsi,
                'mv_ship_name': row.ship_name,
                'mv_ship_type': row.ship_type,
                'mv_flag': row.flag,
                'mv_length': row.length,
                'mv_width': row.width,
                'mv_grt': row.grt,
                'mv_dwt': row.dwt,
                'mv_year_built': row.year_built,
                'mv_type_name': row.type_name,
                'mv_ais_type_summary': row.ais_type_summary,
                'mv_data_source': 'ais'
            }
        )
    return JsonResponse({"message": "All unique ships from Full_Data has been successfully uploaded in merchant_vessel."}, status=200)


# def populate_data(request):
#     full_data_records = Full_Data.objects.all().order_by('timestamp')
#
#     for row in full_data_records:
#         # Create or get Merchant_Vessel instance
#         merchant_vessel, created = Merchant_Vessel.objects.get_or_create(
#             mv_imo=row.imo,
#             mv_ship_id=row.ship_id,
#             defaults={
#                 'mv_mmsi': row.mmsi,
#                 'mv_ship_name': row.ship_name,
#                 'mv_ship_type': row.ship_type,
#                 'mv_flag': row.flag,
#                 'mv_length': row.length,
#                 'mv_width': row.width,
#                 'mv_grt': row.grt,
#                 'mv_dwt': row.dwt,
#                 'mv_year_built': row.year_built,
#                 'mv_type_name': row.type_name,
#                 'mv_ais_type_summary': row.ais_type_summary
#             }
#         )
#
#         mvd_lat = row.get("latitude")  # replace with the actual column name
#         mvd_lon = row.get("longitude")
#         mvd_position = f"POINT({mvd_lon} {mvd_lat})"
#
#         # Create MVDetails instance and associate it with Merchant_Vessel
#         MVDetails.objects.create(
#             mvd_mv_key=merchant_vessel,
#             mvd_position=mvd_position,
#             mvd_speed=row.speed,
#             mvd_heading=row.heading,
#             mvd_status=row.status,
#             mvd_course=row.course,
#             mvd_timestamp=row.timestamp,
#             mvd_dsrc=row.dsrc,
#             mvd_utc_seconds=row.utc_seconds,
#             mvd_draught=row.draught,
#             mvd_rot=row.rot,
#             mvd_destination=row.destination,
#             mvd_eta=row.eta,
#             mvd_current_port=row.current_port,
#             mvd_last_port=row.last_port,
#             mvd_last_port_time=row.last_port_time,
#             mvd_current_port_id=row.current_port_id,
#             mvd_current_port_unlocode=row.current_port_unlocode,
#             mvd_current_port_country=row.current_port_country,
#             mvd_last_port_id=row.last_port_id,
#             mvd_last_port_unlocode=row.last_port_unlocode,
#             mvd_last_port_country=row.last_port_country,
#             mvd_next_port_id=row.next_port_id,
#             mvd_next_port_unlocode=row.next_port_unlocode,
#             mvd_next_port_name=row.next_port_name,
#             mvd_next_port_country=row.next_port_country,
#             mvd_eta_calc=row.eta_calc,
#             mvd_eta_updated=row.eta_updated,
#             mvd_distance_to_go=row.distance_to_go,
#             mvd_distance_travelled=row.distance_travelled,
#             mvd_awg_speed=row.awg_speed,
#             mvd_max_speed=row.max_speed,
#         )
#
#     return JsonResponse({"message": "All unique ships from Full_Data have been successfully uploaded in Merchant_Vessel and MVDetails."}, status=200)


@api_view(http_method_names=['GET'])
def flag_counts(request):
    start_date_str = request.GET.get('date_from')
    end_date_str = request.GET.get('date_to')
    port = request.GET.get('port')

    date_from = datetime.strptime(start_date_str, '%Y-%m-%d')
    date_to = datetime.strptime(end_date_str, '%Y-%m-%d')

    all_ships = Full_Data.objects.filter(timestamp__range=(date_from, date_to))
    ship_data = list(all_ships.values())
    ship_df = pd.DataFrame.from_records(ship_data)
    ship_df['current_port'] = ship_df['current_port'].replace({'KARACHI ANCH': 'KARACHI', 'PORT QASIM ANCH': 'PORT QASIM'})
    if port:
        ship_df = ship_df[ship_df['current_port'] == port]

    unique_ships = {}
    for ship in ship_df.itertuples():
        unique_ships[ship.ship_id] = ship.flag

    flag_count = {}
    for flag in unique_ships.values():
        flag_count[flag] = flag_count.get(flag, 0) + 1

    return JsonResponse(flag_count)


@api_view(http_method_names=['GET'])
def type_counts(request):
    start_date_str = request.GET.get('date_from')
    end_date_str = request.GET.get('date_to')
    port = request.GET.get('port')

    date_from = datetime.strptime(start_date_str, '%Y-%m-%d')
    date_to = datetime.strptime(end_date_str, '%Y-%m-%d')

    all_ships = Full_Data.objects.filter(timestamp__range=(date_from, date_to))
    if port:
        all_ships = all_ships.filter(current_port=port)

    ship_data = list(all_ships.values())
    ship_df = pd.DataFrame.from_records(ship_data)
    ship_df['current_port'] = ship_df['current_port'].replace({'KARACHI ANCH': 'KARACHI', 'PORT QASIM ANCH': 'PORT QASIM'})
    unique_ships = ship_df.drop_duplicates(subset='ship_id')
    type_count = unique_ships.groupby('ais_type_summary')['ship_id'].count().to_dict()

    return JsonResponse(type_count)


'''
def register_vessel_data(request):
    # Fetch data from the Extended_Data table
    extended_data_records = Full_Data.objects.all().order_by('timestamp')
    # Initialize a dictionary to keep track of ongoing trips for each vessel
    ongoing_trips = {}
    for row in extended_data_records:
        # Register vessel data if not already registered
        vessel, created = Merchant_Vessel.objects.get_or_create(
            imo=row.imo,
            ship_id=row.ship_id,
            defaults={
                'mmsi': row.mmsi,
                'ship_name': row.ship_name,
                'ship_type': row.ship_type,
                'call_sign': row.call_sign,
                'flag': row.flag,
                'length': row.length,
                'width': row.width,
                'grt': row.grt,
                'dwt': row.dwt,
                'year_built': row.year_built,
                'type_name': row.type_name,
                'ais_type_summary': row.ais_type_summary
            }
        )
        # Parse timestamp and create datetime object
        timestamp = row.timestamp
        # Check if the vessel has an ongoing trip
        if vessel.mmsi in ongoing_trips:
            trip = ongoing_trips[vessel.mmsi]
            if row.destination != trip.destination:
                # if row.draught != trip.draught or row.destination != trip.destination:
                # Complete the ongoing trip and create a new one
                trip = Merchant_Trip.objects.create(
                    vessel=vessel,
                    dsrc=row.dsrc,
                    destination=row.destination,
                    eta=row.eta
                )
                ongoing_trips[vessel.mmsi] = trip
            # Create or update TripDetail for ongoing trip
            Trip_Details.objects.create(
                trip=trip,
                longitude=row.longitude,
                latitude=row.latitude,
                speed=row.speed,
                heading=row.heading,
                status=row.status,
                course=row.course,
                timestamp=timestamp,
                utc_seconds=row.utc_seconds,
                draught=row.draught,
                rot=row.rot,
                current_port=row.curent_port,
                last_port=row.last_port,
                last_port_time=row.last_port_time,
                current_port_id=row.current_port_id,
                current_port_unlocode=row.current_port_unlocode,
                current_port_country=row.current_port_country,
                last_port_id=row.last_port_id,
                last_port_unlocode=row.last_port_unlocode,
                last_port_country=row.last_port_country,
                next_port_id=row.next_port_id,
                next_port_unlocode=row.next_port_unlocode,
                next_port_name=row.next_port_name,
                next_port_country=row.next_port_country,
                eta_calc=row.eta_calc,
                eta_updated=row.eta_updated,
                distance_to_go=row.distance_to_go,
                distnace_travelled=row.distnace_travelled,
                awg_speed=row.awg_speed,
                max_speed=row.max_speed
            )
        else:
            # Create a new trip and TripDetail
            trip = Merchant_Trip.objects.create(
                vessel=vessel,
                dsrc=row.dsrc,
                destination=row.destination,
                eta=row.eta
            )
            ongoing_trips[vessel.mmsi] = trip
            Trip_Details.objects.create(
                trip=trip,
                longitude=row.longitude,
                latitude=row.latitude,
                speed=row.speed,
                heading=row.heading,
                status=row.status,
                course=row.course,
                timestamp=timestamp,
                utc_seconds=row.utc_seconds,
                draught=row.draught,
                rot=row.rot,
                current_port=row.curent_port,
                last_port=row.last_port,
                last_port_time=row.last_port_time,
                current_port_id=row.current_port_id,
                current_port_unlocode=row.current_port_unlocode,
                current_port_country=row.current_port_country,
                last_port_id=row.last_port_id,
                last_port_unlocode=row.last_port_unlocode,
                last_port_country=row.last_port_country,
                next_port_id=row.next_port_id,
                next_port_unlocode=row.next_port_unlocode,
                next_port_name=row.next_port_name,
                next_port_country=row.next_port_country,
                eta_calc=row.eta_calc,
                eta_updated=row.eta_updated,
                distance_to_go=row.distance_to_go,
                distnace_travelled=row.distnace_travelled,
                awg_speed=row.awg_speed,
                max_speed=row.max_speed
            )
'''