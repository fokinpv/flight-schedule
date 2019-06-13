from django.urls import path
from apps.flights.views import FlightList, FlightDetail
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', FlightList.as_view(), name="flight_list_view"),
    path('<int:pk>/', FlightDetail.as_view(), name="flight_detail_view")
]

urlpatterns = format_suffix_patterns(urlpatterns)