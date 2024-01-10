import csv
from django.http import JsonResponse
from django.views import View
from .ais_models import COSPASData, COSPASBeacon
from datetime import datetime


class COSPASUploadView(View):
    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return JsonResponse({"error": "No file provided."}, status=400)

        try:
            content = file.read().decode("utf-8")
            rows = csv.DictReader(content.splitlines())

            for row in rows:
                # Extract data from CSV row
                beacon_reg_no = row.get("beacon_reg_no")

                # Check if beacon_reg_no exists in COSPASBeacon
                try:
                    cospas_beacon_key = COSPASBeacon.objects.get(bcnid15=beacon_reg_no)
                except COSPASBeacon.DoesNotExist:
                    cospas_beacon_key = None

                # Custom function to handle date parsing and null values
                def parse_date(value):
                    if value:
                        try:
                            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f %z")
                        except ValueError:
                            return None
                    else:
                        return None

                # Create COSPASData object and save to database
                cospas_data = COSPASData(
                    occurrence_type=row.get("occurrence_type"),
                    distress_conf=row.get("distress_conf"),
                    beacon_operating_mode=row.get("beacon_operating_mode"),
                    beacon_reg_no=row.get("beacon_reg_no"),
                    msg_ref=row.get("msg_ref"),
                    detected_at=parse_date(row.get("detected_at")),
                    det_satellite=row.get("det_satellite"),
                    det_freq_typeA=row.get("det_freq_typeA"),
                    det_freq_typeB=row.get("det_freq_typeB"),
                    det_freq_typeC=row.get("det_freq_typeC"),
                    user_class_std_location=row.get("user_class_std_location"),
                    cospos_beacon_key=cospas_beacon_key,
                    emergency_code=row.get("emergency_code"),
                    pos_confirmed_lat=row.get("pos_confirmed_lat"),
                    pos_confirmed_long=row.get("pos_confirmed_long"),
                    pos_dopplerA=row.get("pos_dopplerA"),
                    pos_dopplerB=row.get("pos_dopplerB"),
                    pos_doa_lat=row.get("pos_doa_lat"),
                    pos_doa_long=row.get("pos_doa_long"),
                    pos_expected_acc=row.get("pos_expected_acc"),
                    pos_altitude=row.get("pos_altitude"),
                    pos_encoded_lat=row.get("pos_encoded_lat"),
                    pos_encoded_long=row.get("pos_encoded_long"),
                    pos_updated_time=parse_date(row.get("pos_updated_time")),
                    pos_provided_by=row.get("pos_provided_by"),
                    nextpass_confirmed=parse_date(row.get("nextpass_confirmed")),
                    nextpass_doppA=parse_date(row.get("nextpass_doppA")),
                    nextpass_doppB=parse_date(row.get("nextpass_doppB")),
                    nextpass_doa=parse_date(row.get("nextpass_doa")),
                    nextpass_encoded=parse_date(row.get("nextpass_encoded")),
                    hex_id=row.get("hex_id"),
                    activation_type=row.get("activation_type"),
                    oei_mid=row.get("oei_mid"),
                    oei_loc_protocol_type=row.get("oei_loc_protocol_type"),
                    oei_pos_uncertainty=row.get("oei_pos_uncertainty"),
                    oei_lat=row.get("oei_lat"),
                    oei_long=row.get("oei_long"),
                    oper_info_imo=row.get("oper_info_imo"),
                    oper_info_vessel_type=row.get("oper_info_vessel_type"),
                    oper_info_lpoc=row.get("oper_info_lpoc"),
                    oper_info_npoc=row.get("oper_info_npoc"),
                    oper_ship_owner=row.get("oper_ship_owner"),
                    oper_sat_alert_time=parse_date(row.get("oper_sat_alert_time")),
                    temp_from=parse_date(row.get("temp_from")),
                    temp_to=parse_date(row.get("temp_to")),
                    temp_inc_reporting_time=parse_date(row.get("temp_inc_reporting_time")),
                    temp_inc_details=row.get("temp_inc_details"),
                    temp_actions_list=row.get("temp_actions_list"),
                    remarks=row.get("remarks")
                )
                cospas_data.save()

            return JsonResponse({"message": "Data uploaded successfully in COSPAS."}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
