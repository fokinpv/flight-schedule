from django.db import models

class Flight(models.Model):

    flight_name = models.CharField(max_length=100)
    flight_number = models.IntegerField()
    scheduled_datetime = models.DateTimeField()
    expected_arrival_datetime = models.DateTimeField()
    departure = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)
    fare = models.IntegerField()
    flight_duration = models.TimeField()

    