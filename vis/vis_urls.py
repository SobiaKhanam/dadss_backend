from django.urls import path
from . import vis_views


urlpatterns = [
    path('query_data', vis_views.query_data, name='query_data'),
    path('vis_data', vis_views.BoatTripLogsView.as_view({'get': 'list'}), name='vis_data'),
    path('populate_rvessels', vis_views.populate_rvessels, name='populate_rvessels')
]
