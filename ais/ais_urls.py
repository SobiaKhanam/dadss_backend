from django.urls import path
from . import ais_views, jmis_views, cospas_views

urlpatterns = [
    path('stay_count', ais_views.stay_count, name='stay_count'),
    path('ship_counts', ais_views.ship_counts, name='ship_counts'),
    path('ship_counts_week', ais_views.ship_counts_week, name='ship_counts_week'),
    path('vessel_position', ais_views.vessel_position, name='vessel_position'),
    path('populate_data', ais_views.populate_data, name='populate_data'),
    path('flag_counts', ais_views.flag_counts, name='flag_counts'),
    path('type_counts', ais_views.type_counts, name='type_counts'),
    path('lost_report', jmis_views.LostReportUploadView.as_view(), name='lost_report'),
    path('lp_json', jmis_views.LostReportCSVtoJSON.as_view(), name='lp_csv'),
    path('situational_report', jmis_views.SituationalReportUploadView.as_view(), name='situational_report'),
    path('sit_report_json', jmis_views.SituationalReportCSVtoJSON.as_view(), name='sit_report_json'),
    path('PNSC_Ship_Data', jmis_views.PNSCShipDataUploadView.as_view(), name='PNSC_Ship_Data'),
    path('psd_json', jmis_views.PNSCShipDataCSVtoJSON.as_view(), name='psd_json'),
    path('COSPAS_Data', cospas_views.COSPASUploadView.as_view(), name='COSPAS_Data'),
]

# /merchant, /aisvessel, /misrep, /ship_breaking, /lreport, /sreport, /psreport urls defined in msa urls.py
