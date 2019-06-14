from django.shortcuts import render
from apps.flights.models import Flight
from apps.flights.serializers import FlightSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from datetime import datetime

# Create your views here.
class FlightList(APIView):

    @staticmethod
    def get_object(pk):
        try:
            return Flight.objects.get(pk=pk)
        except Flight.DoesNotExist:
            raise Http404        

    @staticmethod
    def validate_filter_params(request):

        flight_name = request.GET.get("flight_name", None)
        scheduled_date = request.GET.get("scheduled_date", None)
        departure = request.GET.get("departure", None)
        destination = request.GET.get("destination", None)

        filter_params = {}
        errors = {}
        if flight_name is not None:
            filter_params["flight_name"] = flight_name

            if not all(x.isalpha() or x=="-" for x in flight_name):
               errors["invalid_flight_name"] = "flight_name should be string"

        if scheduled_date is not None:
            filter_params["scheduled_datetime"] = scheduled_date
            try:
                datetime.strptime(scheduled_date, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                errors["invalid_scheduled_date"] = "Incorrect data format, should be Y-m-dTH:M:S"

        if departure is not None:
            filter_params["departure"] = departure

            if not departure.isalpha():
               errors["invalid_departure"] = "departure should be string"

            if len(departure) != 3:
               errors["invalid_departure_len"] = "departure len should be 3"    

        if destination is not None:
            filter_params["destination"] = destination

            if not destination.isalpha():
               errors["invalid_destination"] = "destination should be string"

            if len(destination) != 3:
               errors["invalid_destination_len"] = "destination len should be 3" 

        return filter_params, errors    

    def get(self, request, format=None):

        filter_params, errors = self.validate_filter_params(request)

        if bool(errors):
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)  

        flights = Flight.objects.filter(**filter_params)
        serializer = FlightSerializer(flights, many=True)

        data = serializer.data
        if len(data) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)  
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FlightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            


class FlightDetail(APIView):

    @staticmethod
    def get_object(pk):
        try:
            return Flight.objects.get(pk=pk)
        except Flight.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        flight = self.get_object(pk)
        serializer = FlightSerializer(flight)
        return Response(serializer.data)        

    def put(self, request, pk, format=None):
        flight = self.get_object(pk)
        serializer = FlightSerializer(flight, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        flight = self.get_object(pk)
        flight.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)