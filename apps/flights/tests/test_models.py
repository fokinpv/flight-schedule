from django.test import TestCase
from apps.flights.models import Flight
from datetime import datetime, timedelta

class FlightTest(TestCase):

    def setUp(self):

        self.scheduled_datetime = datetime.now()
        self.expected_arrival_datetime = self.scheduled_datetime + timedelta(hours=5)
        self.flight_duration= '05:00' 

        test_flight = Flight.objects.create(
            flight_name='thr-osd',
            flight_number=7777,
            scheduled_datetime=self.scheduled_datetime ,
            expected_arrival_datetime=self.expected_arrival_datetime,
            departure='thr',
            destination='osd',
            fare=100,
            flight_duration=self.flight_duration
        )

    def test_get_flight(self):

        flight = Flight.objects.get(flight_name='thr-osd')
        self.assertEqual(flight.departure, 'thr')
        self.assertEqual(flight.destination, 'osd')