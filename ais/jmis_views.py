import csv
from django.http import JsonResponse
from django.views import View
from .ais_models import LostReport, Merchant_Vessel, SituationalReport, PNSCShipData
from datetime import datetime
import re
from io import StringIO
from rest_framework import serializers
from rest_framework.views import APIView
from msa.api.parent import PositionField, CustomViewSet


class LostReportSerializer(serializers.ModelSerializer):
    lr_position = PositionField(required=False)
    mv_imo = serializers.IntegerField(write_only=True, required=False)
    mv_ship_name = serializers.CharField(write_only=True, required=False)
    mv_flag = serializers.CharField(write_only=True, required=False)
    mv_ais_type_summary = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = LostReport
        fields = '__all__'
        read_only_fields = ['lr_key', 'lr_mv_key', 'lr_rdt']

    def create(self, validated_data):
        mv_imo = validated_data.pop('mv_imo', None)
        mv_ship_name = validated_data.pop('mv_ship_name', None)
        mv_ais_type_summary = validated_data.pop('mv_ais_type_summary', None)
        mv_flag = validated_data.pop('mv_flag', None)

        merchant_vessel = Merchant_Vessel.objects.filter(mv_imo=mv_imo).first()

        if not merchant_vessel:
            merchant_vessel = Merchant_Vessel.objects.create(
                mv_imo=mv_imo,
                mv_ship_name=mv_ship_name,
                mv_ais_type_summary=mv_ais_type_summary,
                mv_flag=mv_flag,
                mv_data_source='lost_report'
            )
        validated_data['lr_mv_key'] = merchant_vessel
        lost_report = LostReport.objects.create(**validated_data)
        return lost_report


class LostReportListSerializer(serializers.ListSerializer):
    def to_internal_value(self, data):
        # This method is called when deserializing the input data.
        # It ensures that the child serializer is properly instantiated.
        return [self.child.to_internal_value(item) for item in data]
    child = LostReportSerializer()


class LreportViewSet(CustomViewSet):
    queryset = LostReport.objects.all()
    serializer_class = LostReportSerializer

    filterset_fields = {
        'lr_key': ['exact', 'gte', 'lte'],
        'lr_rdt': ['exact', 'gte', 'lte', 'gt', 'lt'],
        'lr_reporting_date': ['exact', 'gte', 'lte', 'gt', 'lt'],
    }
    search_fields = ['lr_coi_number']
    ordering_fields = ['lr_key', 'lr_rdt', 'lr_reporting_date']
    ordering = ['-lr_key']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LostReportListSerializer
        return LostReportSerializer


class LostReportUploadView(APIView):
    # read csv file and save it in the database
    REQUIRED_COLUMNS = [
        "COINumber", "SubscriberCode", "PRNumber", "ActionAddresseeCodes", "ReportingDatetime",
        "Remarks", "Latitude", "Longitude", "CreatedOn", "CreatedBy", "IMO", "ShipName", "Flag",
        "ShipType", "TrackStatus", "TotalCrew"
    ]

    # read csv file and convert it into json
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No file provided."}, status=400)

        try:
            content = file.read().decode("utf-8")
            rows = csv.DictReader(content.splitlines())

            # Check if all required columns are present
            missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in rows.fieldnames]
            if missing_columns:
                return JsonResponse({"error": f"Missing columns: {', '.join(missing_columns)}"}, status=400)

            for row in rows:
                lr_imo = row.get("IMO")
                lr_ship_name = row.get("ShipName")
                lr_flag = row.get("Flag")
                lr_ship_type = row.get("ShipType")
                lr_lat = row.get("Latitude")
                lr_lon = row.get("Longitude")
                lr_position = f"POINT({lr_lon} {lr_lat})"

                # Check if Merchant_Vessel with the given imo exists
                merchant_vessel, created = Merchant_Vessel.objects.get_or_create(
                    mv_imo=lr_imo,
                    defaults={
                        "mv_ship_name": lr_ship_name,
                        "mv_flag": lr_flag,
                        "mv_ais_type_summary": lr_ship_type,
                        "mv_data_source": "lost_report"
                    },
                )

                # Custom function to handle date parsing and null values
                def parse_date(value):
                    if value:
                        try:
                            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f %z")
                        except ValueError:
                            return None
                    else:
                        return None

                # Update LostReport with the found or newly created Merchant_Vessel
                LostReport.objects.create(
                    lr_mv_key=merchant_vessel,
                    lr_coi_number=row.get("COINumber"),
                    lr_subscriber_code=row.get("SubscriberCode"),
                    lr_pr_number=row.get("PRNumber"),
                    lr_action_addresses_codes=row.get("ActionAddresseeCodes"),
                    lr_reporting_date=parse_date(row.get("ReportingDatetime")),
                    lr_remarks=row.get("Remarks"),
                    lr_position=lr_position,
                    lr_created_on=parse_date(row.get("CreatedOn")),
                    lr_created_by=row.get("CreatedBy"),
                    lr_track_status=row.get("TrackStatus"),
                    lr_total_crew=row.get("TotalCrew") if row.get("TotalCrew") in row else None
                )

            return JsonResponse({"message": "Data uploaded successfully in lost report."}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class LostReportCSVtoJSON(APIView):
    REQUIRED_COLUMNS = [
        "COINumber", "SubscriberCode", "PRNumber", "ActionAddresseeCodes", "ReportingDatetime",
        "Remarks", "Latitude", "Longitude", "CreatedOn", "CreatedBy", "IMO", "ShipName", "Flag",
        "ShipType", "TrackStatus", "TotalCrew"
    ]
    # read csv file and convert it into json
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No file provided."}, status=400)

        try:
            content = file.read().decode("utf-8")
            rows = csv.DictReader(content.splitlines())

            # Check if all required columns are present
            missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in rows.fieldnames]
            if missing_columns:
                return JsonResponse({"error": f"Missing columns: {', '.join(missing_columns)}"}, status=400)

            converted_data = []
            for row in rows:
                lat = row.get("Latitude")
                long = row.get("Longitude")

                def parse_date(value):
                    if value:
                        try:
                            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f %z")
                        except ValueError:
                            return None
                    else:
                        return None

                converted_data.append({
                    "mv_imo": row.get("IMO"),
                    "mv_ship_name": row.get("ShipName"),
                    "mv_flag": row.get("Flag"),
                    "mv_ais_type_summary": row.get("ShipType"),
                    "lr_position": {
                        "type": "Point",
                        "coordinates": [float(long), float(lat)]
                    },
                    "lr_coi_number": row.get("COINumber"),
                    "lr_subscriber_code": row.get("SubscriberCode"),
                    "lr_pr_number": row.get("PRNumber"),
                    "lr_action_addresses_codes": row.get("ActionAddresseeCodes"),
                    "lr_reporting_date": row.get("ReportingDatetime"),
                    "lr_remarks": row.get("Remarks"),
                    "lr_created_on": parse_date(row.get("CreatedOn")),
                    "lr_created_by": row.get("CreatedBy"),
                    "lr_track_status": row.get("TrackStatus"),
                    "lr_total_crew": row.get("TotalCrew") if row.get("TotalCrew") in row else None,
                })

            return JsonResponse(converted_data, safe=False, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class SitReportSerializer(serializers.ModelSerializer):
    sit_position = PositionField()
    mv_imo = serializers.IntegerField(write_only=True, required=False)
    mv_mmsi = serializers.IntegerField(write_only=True, required=False)
    mv_ship_name = serializers.CharField(write_only=True, required=False)
    mv_flag = serializers.CharField(write_only=True, required=False)
    mv_ais_type_summary = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = SituationalReport
        fields = '__all__'
        read_only_fields = ['sit_key', 'sit_mv_key', 'sit_rdt']

    def create(self, validated_data):
        mv_imo = validated_data.pop('mv_imo', None)
        mv_mmsi = validated_data.pop('mv_mmsi', None)
        mv_ship_name = validated_data.pop('mv_ship_name', None)
        mv_ais_type_summary = validated_data.pop('mv_ais_type_summary', None)
        mv_flag = validated_data.pop('mv_flag', None)

        merchant_vessel = Merchant_Vessel.objects.filter(mv_imo=mv_imo).first()

        if not merchant_vessel:
            merchant_vessel = Merchant_Vessel.objects.create(
                mv_imo=mv_imo,
                mv_mmsi=mv_mmsi,
                mv_ship_name=mv_ship_name,
                mv_ais_type_summary=mv_ais_type_summary,
                mv_flag=mv_flag,
                mv_data_source='situational_report'
            )
        validated_data['sit_mv_key'] = merchant_vessel
        sit_report = SituationalReport.objects.create(**validated_data)
        return sit_report


class SituationalReportListSerializer(serializers.ListSerializer):
    def to_internal_value(self, data):
        # This method is called when deserializing the input data.
        # It ensures that the child serializer is properly instantiated.
        return [self.child.to_internal_value(item) for item in data]
    child = SitReportSerializer()


class SreportViewSet(CustomViewSet):
    queryset = SituationalReport.objects.all()
    serializer_class = SitReportSerializer

    filterset_fields = {
        'sit_key': ['exact', 'gte', 'lte'],
        'sit_rdt': ['exact', 'gte', 'lte', 'gt', 'lt']
    }
    search_fields = ['sit_dtg']
    ordering_fields = ['sit_key', 'sit_rdt']
    ordering = ['-sit_key']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SituationalReportListSerializer
        return SitReportSerializer


class SituationalReportUploadView(View):
    REQUIRED_COLUMNS = [
        "S.No", "DTG", "MMSI", "IMO", "Name", "Flag", "Type", "Position", "LPOC", "Last Port Country", "NPOC",
        "Next Port Country", "CO/SPD", "Source"
    ]

    # read csv file and convert it into json
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No file provided."}, status=400)

        try:
            content = file.read().decode("utf-8")
            rows = csv.DictReader(content.splitlines())

            # Check if all required columns are present
            missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in rows.fieldnames]
            if missing_columns:
                return JsonResponse({"error": f"Missing columns: {', '.join(missing_columns)}"}, status=400)

            for row in rows:
                print("Row Data:", row)
                mv_imo = row.get("IMO")
                mv_ship_name = row.get("Name")
                mv_flag = row.get("Flag")
                mv_ship_type = row.get("Type")
                mv_mmsi = row.get("MMSI")

                # Check if Merchant_Vessel with the given imo exists
                merchant_vessel, created = Merchant_Vessel.objects.get_or_create(
                    mv_imo=mv_imo,
                    defaults={
                        "mv_ship_name": mv_ship_name,
                        "mv_flag": mv_flag,
                        "mv_ais_type_summary": mv_ship_type,
                        "mv_mmsi": mv_mmsi,
                        "mv_data_source": "situational_report",
                    },
                )

                # Custom function to handle date parsing and null values
                def parse_date(value):
                    if value:
                        try:
                            return datetime.strptime(value, "%b %dst %Y, %I:%M:%S %p")
                        except ValueError:
                            return None
                    else:
                        return None

                position_data = row.get("Position")
                if position_data:
                    lat_lon_match = re.search(r'Lat:(?P<lat>[\d.-]+)\/Lon:(?P<lon>[\d.v]+)', position_data)
                    if lat_lon_match:
                        latitude = lat_lon_match.group("lat")
                        longitude = lat_lon_match.group("lon")
                        sit_position = f"POINT({longitude} {latitude})"
                    else:
                        sit_position = None
                else:
                    sit_position = None

                co_spd_data = row.get("CO/SPD")
                if co_spd_data:
                    co_spd_match = re.search(r'(?P<course>[\d.]+)/(?P<speed>[\d.]+)', co_spd_data)
                    if co_spd_match:
                        course = co_spd_match.group("course")
                        speed = co_spd_match.group("speed")
                    else:
                        course = None
                        speed = None
                else:
                    course = None
                    speed = None

                # Update LostReport with the found or newly created Merchant_Vessel
                SituationalReport.objects.create(
                    sit_mv_key=merchant_vessel,
                    sit_dtg=parse_date(row.get("DTG")),
                    sit_position=sit_position,
                    sit_lpoc=row.get("LPOC"),
                    sit_last_port_country=row.get("Last Port Country"),
                    sit_npoc=row.get("NPOC"),
                    sit_next_port_country=row.get("Next Port Country"),
                    sit_course=course,
                    sit_speed=speed,
                    sit_source=row.get("Source")
                )

            return JsonResponse({"message": "Data uploaded successfully in situational report."}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class SituationalReportCSVtoJSON(APIView):
    REQUIRED_COLUMNS = [
        "S.No", "DTG", "MMSI", "IMO", "Name", "Flag", "Type", "Position", "LPOC", "Last Port Country", "NPOC",
        "Next Port Country", "CO/SPD", "Source"
    ]

    # read csv file and convert it into json
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No file provided."}, status=400)

        try:
            content = file.read().decode("utf-8")
            rows = csv.DictReader(content.splitlines())

            # Check if all required columns are present
            missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in rows.fieldnames]
            if missing_columns:
                return JsonResponse({"error": f"Missing columns: {', '.join(missing_columns)}"}, status=400)

            converted_data = []
            for row in rows:
                def parse_date(value):
                    if value:
                        try:
                            return datetime.strptime(value, "%b %dst %Y, %I:%M:%S %p")
                        except ValueError:
                            return None
                    else:
                        return None

                position_data = row.get("Position")
                if position_data:
                    lat_lon_match = re.search(r'Lat:(?P<lat>[\d.-]+)\/Lon:(?P<lon>[\d.v]+)', position_data)
                    if lat_lon_match:
                        latitude = lat_lon_match.group("lat")
                        longitude = lat_lon_match.group("lon")
                    else:
                        latitude = None
                        longitude = None
                else:
                    latitude = None
                    longitude = None

                co_spd_data = row.get("CO/SPD")
                if co_spd_data:
                    co_spd_match = re.search(r'(?P<course>[\d.]+)/(?P<speed>[\d.]+)', co_spd_data)
                    if co_spd_match:
                        course = co_spd_match.group("course")
                        speed = co_spd_match.group("speed")
                    else:
                        course = None
                        speed = None
                else:
                    course = None
                    speed = None

                converted_data.append({
                    "mv_imo": row.get("IMO"),
                    "mv_mmsi": row.get("MMSI"),
                    "mv_ship_name": row.get("Name"),
                    "mv_flag": row.get("Flag"),
                    "mv_ais_type_summary": row.get("Type"),
                    "sit_dtg": parse_date(row.get("DTG")),
                    "sit_position": {
                        "type": "Point",
                        "coordinates": [float(longitude), float(latitude)]
                    },
                    "sit_lpoc": row.get("LPOC"),
                    "sit_last_port_country": row.get("Last Port Country"),
                    "sit_npoc": row.get("NPOC"),
                    "sit_next_port_country": row.get("Next Port Country"),
                    "sit_course": course,
                    "sit_speed": speed,
                    "sit_source": row.get("Source")
                })

            return JsonResponse(converted_data, safe=False, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class PNSCShipDataSerializer(serializers.ModelSerializer):
    ps_position = PositionField()
    mv_imo = serializers.IntegerField(write_only=True, required=False)
    mv_ship_name = serializers.CharField(write_only=True, required=False)
    mv_flag = serializers.CharField(write_only=True, required=False)
    mv_ais_type_summary = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = PNSCShipData
        fields = '__all__'
        read_only_fields = ['ps_key', 'ps_mv_key', 'ps_rdt']

    def create(self, validated_data):
        mv_imo = validated_data.pop('mv_imo', None)
        mv_ais_type_summary = validated_data.pop('mv_ais_type_summary', None)

        merchant_vessel = Merchant_Vessel.objects.filter(mv_imo=mv_imo).first()

        if not merchant_vessel:
            merchant_vessel = Merchant_Vessel.objects.create(
                mv_imo=mv_imo,
                mv_ais_type_summary=mv_ais_type_summary,
                mv_data_source='PNSC_ship_data'
            )
        validated_data['ps_mv_key'] = merchant_vessel
        ps_report = PNSCShipData.objects.create(**validated_data)
        return ps_report


class PNSCShipDataListSerializer(serializers.ListSerializer):
    def to_internal_value(self, data):
        # This method is called when deserializing the input data.
        # It ensures that the child serializer is properly instantiated.
        return [self.child.to_internal_value(item) for item in data]
    child = PNSCShipDataSerializer()


class PNSCShipDataViewSet(CustomViewSet):
    queryset = PNSCShipData.objects.all()
    serializer_class = PNSCShipDataSerializer

    filterset_fields = {
        'ps_key': ['exact', 'gte', 'lte'],
        'ps_rdt': ['exact', 'gte', 'lte', 'gt', 'lt']
    }
    search_fields = ['ps_track_number']
    ordering_fields = ['ps_key', 'ps_rdt']
    ordering = ['-ps_key']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PNSCShipDataListSerializer
        return PNSCShipDataSerializer


class PNSCShipDataUploadView(View):
    REQUIRED_COLUMNS = [
        "Country", "StatusSymbol", "StatusSymbolRemarks", "StatusSymbolAssignedTime", "TrackNumber", "Lat", "Lon",
        "Speed", "Course", "Timestamp", "Imo", "LastPort", "NextPortName", "TrackType", "ShipTypeName", "TrackLabel"
    ]

    # read csv file and convert it into json
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No file provided."}, status=400)

        try:
            content = file.read().decode("utf-8")
            rows = csv.DictReader(content.splitlines())

            # Check if all required columns are present
            missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in rows.fieldnames]
            if missing_columns:
                return JsonResponse({"error": f"Missing columns: {', '.join(missing_columns)}"}, status=400)

            for row in rows:
                ps_imo = row.get("Imo")
                ps_ship_type = row.get("ShipTypeName")
                ps_lat = row.get("Lat")  # replace with the actual column name
                ps_lon = row.get("Lon")
                ps_position = f"POINT ({ps_lon} {ps_lat})"

                # Check if Merchant_Vessel with the given imo exists
                merchant_vessel, created = Merchant_Vessel.objects.get_or_create(
                    mv_imo=ps_imo,
                    defaults={
                        "mv_ais_type_summary": ps_ship_type,
                        "mv_data_source": "PNSC_ship_data",
                    },
                )

                # Custom function to handle date parsing and null values
                def parse_date(value):
                    if value:
                        try:
                            return datetime.strptime(value, "%Y-%m-%d %H:%M")
                        except ValueError:
                            return None
                    else:
                        return None
                # Update LostReport with the found or newly created Merchant_Vessel
                PNSCShipData.objects.create(
                    ps_mv_key=merchant_vessel,
                    ps_country=row.get("Country"),
                    ps_status_symbol=row.get("StatusSymbol"),
                    ps_status_symbol_remarks=row.get("StatusSymbolRemarks"),
                    ps_status_symbol_assigned_time=parse_date(row.get("StatusSymbolAssignedTime")),
                    ps_track_number=parse_date(row.get("TrackNumber")),
                    ps_position=ps_position,
                    ps_speed=row.get("Speed"),
                    ps_course=row.get("Course"),
                    ps_timestamp=parse_date(row.get("Timestamp")),
                    ps_lastport=row.get("LastPort"),
                    ps_next_port=row.get("NextPortName"),
                    ps_track_type=row.get("TrackType"),
                    ps_track_label=row.get("TrackLabel")
                )
            return JsonResponse({"message": "Data uploaded successfully in PNSC Ship Data."}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class PNSCShipDataCSVtoJSON(APIView):
    REQUIRED_COLUMNS = [
        "Country", "StatusSymbol", "StatusSymbolRemarks", "StatusSymbolAssignedTime", "TrackNumber", "Lat", "Lon",
        "Speed", "Course", "Timestamp", "Imo", "LastPort", "NextPortName", "TrackType", "ShipTypeName", "TrackLabel"
    ]

    # read csv file and convert it into json
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No file provided."}, status=400)

        try:
            content = file.read().decode("utf-8")
            rows = csv.DictReader(content.splitlines())

            # Check if all required columns are present
            missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in rows.fieldnames]
            if missing_columns:
                return JsonResponse({"error": f"Missing columns: {', '.join(missing_columns)}"}, status=400)

            converted_data = []
            for row in rows:
                lat = row.get("Lat")
                long = row.get("Lon")

                def parse_date(value):
                    if value:
                        try:
                            return datetime.strptime(value, "%Y-%m-%d %H:%M")
                        except ValueError:
                            return None
                    else:
                        return None

                converted_data.append({
                    "mv_imo": row.get("Imo"),
                    "mv_ais_type_summary": row.get("ShipTypeName"),
                    "ps_country": row.get("Country"),
                    "ps_status_symbol": row.get("StatusSymbol"),
                    "ps_status_symbol_remarks": row.get("StatusSymbolRemarks"),
                    "ps_status_symbol_assigned_time": parse_date(row.get("StatusSymbolAssignedTime")),
                    "ps_track_number": parse_date(row.get("TrackNumber")),
                    "ps_position": {
                        "type": "Point",
                        "coordinates": [float(long), float(lat)]
                    },
                    "ps_speed": row.get("Speed"),
                    "ps_course": row.get("Course"),
                    "ps_timestamp": parse_date(row.get("Timestamp")),
                    "ps_lastport": row.get("LastPort"),
                    "ps_next_port": row.get("NextPortName"),
                    "ps_track_type": row.get("TrackType"),
                    "ps_track_label": row.get("TrackLabel")
                })

            return JsonResponse(converted_data, safe=False, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
