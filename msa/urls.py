from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import platform
from .api import reg_vessel
from .api import general_report
from .api import special_report
from .api import user_info
from .api import visuals
from .api import sobia_visuals
from ais import ais_vessel, misrep_views, jmis_views, shipbreaking_views
from intel import intel_views

router = DefaultRouter(trailing_slash=False)
router.register(r'platform', platform.PlatformViewSet, basename="platform")
router.register(r'rvessel', reg_vessel.RvesselViewSet, basename="rvessel")
router.register(r'greport', general_report.GreportViewSet, basename="greport")
router.register(r'fishing', special_report.FishingViewSet, basename="fishing")
router.register(r'merchant', ais_vessel.MerchantViewSet, basename="merchant")
router.register(r'user', user_info.UserViewSet, basename="user")
router.register(r'tripviewset', sobia_visuals.TripViewset, basename="tripviewset")
router.register(r'aisvessel', ais_vessel.AISVesselViewSet, basename="aisvessel")
router.register(r'ireport', intel_views.IreportViewSet, basename="ireport")
router.register(r'ireport_details', intel_views.IRDetailsViewSet, basename='ireport_details')
router.register(r'misrep', misrep_views.MreportViewSet, basename="misrep")
router.register(r'lreport', jmis_views.LreportViewSet, basename="lreport")
router.register(r'sreport', jmis_views.SreportViewSet, basename="sreport")
router.register(r'psreport', jmis_views.PNSCShipDataViewSet, basename="psreport")
router.register(r'ship_breaking', shipbreaking_views.ShipBreakingViewSet, basename="ship_breaking")

urlpatterns = [
    path('', include(router.urls)),

    # User
    path('register', user_info.UserViewSet.as_view({'post': 'create'})),  # used
    path("login", user_info.login_request, name="login"),  # used
    path("logout", user_info.logout_request, name="logout"),

    # Visuals
    # path("fv_leave_enter", visuals.fv_leave_enter),
    path("fv_con", visuals.fv_con),  # used
    path("mv_visiting", visuals.mv_visiting),
    path("mv_visiting_monthly", visuals.mv_visiting_monthly),
    path("narco", visuals.narco),  # used

    # additional changes made by sobia
    path("anti_narcotics", sobia_visuals.anti_narcotics),
    path("contrabands", sobia_visuals.contrabands),
    path("trip", sobia_visuals.trip),
    path("trip_count", sobia_visuals.trip_count),  # used
    path("trip_duration", sobia_visuals.trip_duration),  # used
    path("overstay", sobia_visuals.overstay),  # used
    path("overstay_month", sobia_visuals.overstay_month),
    path("leave_enter", sobia_visuals.leave_enter),  # used
    path("fv_leave_enter", sobia_visuals.fv_leave_enter),  # used
    path("boat_location_stats", sobia_visuals.boat_location_stats),
]
