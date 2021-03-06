import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime, timedelta
from apps.users.models import User
from django.utils.http import urlencode


class FlightListTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.scheduled_datetime = datetime.now()
        self.expected_arrival_datetime = self.scheduled_datetime + timedelta(hours=5)
        self.flight_duration= '05:00' 

        self.flight1 = {
            "flight_name": "thr-osd",
            "flight_number": 7777,
            "scheduled_datetime": self.scheduled_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "expected_arrival_datetime": self.expected_arrival_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "departure": "thr",
            "destination": "osd",
            "fare": 100,
            "flight_duration": self.flight_duration
        }

        self.flights = [
            {
                "flight_name": "thr-osd",
                "flight_number": 7777,
                "scheduled_datetime": self.scheduled_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "expected_arrival_datetime": self.expected_arrival_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "departure": "thr",
                "destination": "osd",
                "fare": 100,
                "flight_duration": self.flight_duration
            },
            {
                "flight_name": "ost-thr",
                "flight_number": 1111,
                "scheduled_datetime": self.scheduled_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "expected_arrival_datetime": self.expected_arrival_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "departure": "osd",
                "destination": "thr",
                "fare": 100,
                "flight_duration": self.flight_duration
            },
            {
                "flight_name": "ist-osd",
                "flight_number": 7689,
                "scheduled_datetime": self.scheduled_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "expected_arrival_datetime": self.expected_arrival_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "departure": "ist",
                "destination": "osd",
                "fare": 100,
                "flight_duration": self.flight_duration
            },
            {
                "flight_name": "thr-ist",
                "flight_number": 4332,
                "scheduled_datetime": self.scheduled_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "expected_arrival_datetime": self.expected_arrival_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "departure": "thr",
                "destination": "ist",
                "fare": 100,
                "flight_duration": self.flight_duration
            },
        ]

        test_user1 = User.objects.create_user(
            username="testuser1",
            email="testuser1@test.com",
            password="1234qrew"
        )

        token_res = self.client.post(
            path=reverse('login_user'),
            data=json.dumps({
                "username": "testuser1",
                "password": "1234qrew"
            }),
            content_type='application/json'
        )

        token_json = json.loads(token_res.content)

        self.token = token_json["token"]
        self.headers = {'HTTP_AUTHORIZATION': 'JWT ' + self.token}

        for flight in self.flights:
            res = self.client.post(
                path=reverse('flight_list_view'),
                data=json.dumps(flight),
                content_type='application/json',
                **self.headers
            )

    def test_create_a_flight(self):

        res = self.client.post(
            path=reverse('flight_list_view'),
            data=json.dumps(self.flight1),
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get_all_flights(self):

        flights_res = self.client.get(
            path=reverse('flight_list_view'),
            **self.headers
        )

        self.assertEqual(flights_res.status_code, status.HTTP_200_OK)

        flights = json.loads(flights_res.content)

        self.assertEqual(len(flights), len(self.flights))

    def test_search_flights_with_flight_name(self):

        query_params = {"flight_name": "thr-osd"}
        url = '{}?{}'.format(reverse('flight_list_view'), urlencode(query_params))
        flights_res = self.client.get(
            path=url,
            **self.headers
        )
        self.assertEqual(flights_res.status_code, status.HTTP_200_OK)

        flights = json.loads(flights_res.content)

        self.assertEqual(len(flights["results"]), 1)

        self.assertEqual(flights["results"][0]['flight_name'], 'thr-osd')

    def test_search_flights_with_invalid_flight_name(self):

        query_params = {"flight_name": "thr-osd-invalid"}
        url = '{}?{}'.format(reverse('flight_list_view'), urlencode(query_params))
        flights_res = self.client.get(
            path=url,
            **self.headers
        )
        self.assertEqual(flights_res.status_code, status.HTTP_404_NOT_FOUND)


    def test_search_flights_with_scheduled_date(self):

        query_params = {'scheduled_date': self.scheduled_datetime.strftime("%Y-%m-%dT%H:%M:%S")}
        url = '{}?{}'.format(reverse('flight_list_view'), urlencode(query_params))
        flights_res = self.client.get(
            path=url,
            **self.headers
        )
        self.assertEqual(flights_res.status_code, status.HTTP_200_OK)

        flights = json.loads(flights_res.content)

        self.assertEqual(len(flights), len(self.flights))

    def test_search_flights_with_invalid_scheduled_date_but_correct_format(self):

        scheduled_date = datetime.now() + timedelta(weeks=1)
        query_params = {'scheduled_date': scheduled_date.strftime("%Y-%m-%dT%H:%M:%S")}
        url = '{}?{}'.format(reverse('flight_list_view'), urlencode(query_params))
        flights_res = self.client.get(
            path=url,
            **self.headers
        )
        self.assertEqual(flights_res.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_flights_with_invalid_scheduled_date_format(self):

        scheduled_date = datetime.now() + timedelta(weeks=1)
        query_params = {'scheduled_date': scheduled_date.strftime("%Y%m%dT%H-%M-%S")}
        url = '{}?{}'.format(reverse('flight_list_view'), urlencode(query_params))
        flights_res = self.client.get(
            path=url,
            **self.headers
        )
        self.assertEqual(flights_res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_flights_with_departure(self):

        query_params = {'departure': "thr"}
        url = '{}?{}'.format(reverse('flight_list_view'), urlencode(query_params))
        flights_res = self.client.get(
            path=url,
            **self.headers
        )
        self.assertEqual(flights_res.status_code, status.HTTP_200_OK)

        flights = json.loads(flights_res.content)

        self.assertEqual(len(flights["results"]), 2)    

    def test_search_flights_with_invalid_departure(self):

        query_params = {'departure': "xyz"}
        url = '{}?{}'.format(reverse('flight_list_view'), urlencode(query_params))
        flights_res = self.client.get(
            path=url,
            **self.headers
        )
        self.assertEqual(flights_res.status_code, status.HTTP_404_NOT_FOUND) 

    def test_search_flights_with_invalid_departure_format(self):

        query_params = {'departure': 2332}
        url = '{}?{}'.format(reverse('flight_list_view'), urlencode(query_params))
        flights_res = self.client.get(
            path=url,
            **self.headers
        )
        self.assertEqual(flights_res.status_code, status.HTTP_400_BAD_REQUEST)

        query_params = {'departure': "222"}
        url = '{}?{}'.format(reverse('flight_list_view'), urlencode(query_params))
        flights_res = self.client.get(
            path=url,
            **self.headers
        )
        self.assertEqual(flights_res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_flights_with_invalid_departure_len(self):

        query_params = {'departure': "xyzvv"}
        url = '{}?{}'.format(reverse('flight_list_view'), urlencode(query_params))
        flights_res = self.client.get(
            path=url,
            **self.headers
        )
        self.assertEqual(flights_res.status_code, status.HTTP_400_BAD_REQUEST)
        flights_res_json = json.loads(flights_res.content)
        self.assertIn("invalid_departure_len", flights_res_json)

    def test_search_flights_with_destination(self):

        query_params = {'destination': "osd"}
        url = '{}?{}'.format(reverse('flight_list_view'), urlencode(query_params))
        flights_res = self.client.get(
            path=url,
            **self.headers
        )
        self.assertEqual(flights_res.status_code, status.HTTP_200_OK)

        flights = json.loads(flights_res.content)

        self.assertEqual(len(flights["results"]), 2)    

    def test_search_flights_with_invalid_destination(self):

        query_params = {'destination': "zyx"}
        url = '{}?{}'.format(reverse('flight_list_view'), urlencode(query_params))
        flights_res = self.client.get(
            path=url,
            **self.headers
        )
        self.assertEqual(flights_res.status_code, status.HTTP_404_NOT_FOUND) 

    def test_search_flights_with_invalid_destination_format(self):

        query_params = {'destination': 2332}
        url = '{}?{}'.format(reverse('flight_list_view'), urlencode(query_params))
        flights_res = self.client.get(
            path=url,
            **self.headers
        )
        self.assertEqual(flights_res.status_code, status.HTTP_400_BAD_REQUEST)
        flights_res_json = json.loads(flights_res.content)
        self.assertIn("invalid_destination", flights_res_json)

        query_params = {'destination': "222"}
        url = '{}?{}'.format(reverse('flight_list_view'), urlencode(query_params))
        flights_res = self.client.get(
            path=url,
            **self.headers
        )
        self.assertEqual(flights_res.status_code, status.HTTP_400_BAD_REQUEST)
        flights_res_json = json.loads(flights_res.content)
        self.assertIn("invalid_destination", flights_res_json)

    def test_search_flights_with_invalid_destination_len(self):

        query_params = {'destination': "xyzvv"}
        url = '{}?{}'.format(reverse('flight_list_view'), urlencode(query_params))
        flights_res = self.client.get(
            path=url,
            **self.headers
        )
        self.assertEqual(flights_res.status_code, status.HTTP_400_BAD_REQUEST) 
        flights_res_json = json.loads(flights_res.content)
        self.assertIn("invalid_destination_len", flights_res_json)

class FlightDetail(TestCase):

    def setUp(self):
        self.client = Client()

        self.scheduled_datetime = datetime.now()
        self.expected_arrival_datetime = self.scheduled_datetime + timedelta(hours=5)
        self.flight_duration= '05:00' 

        self.flight1 = {
            "flight_name": "thr-osd",
            "flight_number": 7777,
            "scheduled_datetime": self.scheduled_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "expected_arrival_datetime": self.expected_arrival_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "departure": "thr",
            "destination": "osd",
            "fare": 100,
            "flight_duration": self.flight_duration
        }

        self.flight_changed = {
            "flight_name": "osd-thr",
            "flight_number": 7777,
            "scheduled_datetime": self.scheduled_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "expected_arrival_datetime": self.expected_arrival_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "departure": "osd",
            "destination": "thr",
            "fare": 100,
            "flight_duration": self.flight_duration
        }

        self.flights = [
            {
                "flight_name": "thr-osd",
                "flight_number": 7777,
                "scheduled_datetime": self.scheduled_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "expected_arrival_datetime": self.expected_arrival_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "departure": "thr",
                "destination": "osd",
                "fare": 100,
                "flight_duration": self.flight_duration
            },
            {
                "flight_name": "ost-thr",
                "flight_number": 1111,
                "scheduled_datetime": self.scheduled_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "expected_arrival_datetime": self.expected_arrival_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "departure": "osd",
                "destination": "thr",
                "fare": 100,
                "flight_duration": self.flight_duration
            },
            {
                "flight_name": "ist-osd",
                "flight_number": 7689,
                "scheduled_datetime": self.scheduled_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "expected_arrival_datetime": self.expected_arrival_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "departure": "ist",
                "destination": "osd",
                "fare": 100,
                "flight_duration": self.flight_duration
            },
            {
                "flight_name": "thr-ist",
                "flight_number": 4332,
                "scheduled_datetime": self.scheduled_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "expected_arrival_datetime": self.expected_arrival_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "departure": "thr",
                "destination": "ist",
                "fare": 100,
                "flight_duration": self.flight_duration
            },
        ]

        test_user1 = User.objects.create_user(
            username="testuser1",
            email="testuser1@test.com",
            password="1234qrew"
        )

        token_res = self.client.post(
            path=reverse('login_user'),
            data=json.dumps({
                "username": "testuser1",
                "password": "1234qrew"
            }),
            content_type='application/json'
        )

        token_json = json.loads(token_res.content)

        self.token = token_json["token"]
        self.headers = {'HTTP_AUTHORIZATION': 'JWT ' + self.token}  

    def test_delete_a_flight(self):
        res = self.client.post(
            path=reverse('flight_list_view'),
            data=json.dumps(self.flight1),
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        flight_json = json.loads(res.content)

        res = self.client.delete(
            path=reverse('flight_detail_view',  kwargs={"pk": flight_json["id"]}),
            **self.headers
        )

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        res = self.client.get(
            path=reverse('flight_detail_view',  kwargs={"pk": flight_json["id"]}),
            **self.headers
        )

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_a_flight(self):

        res = self.client.post(
            path=reverse('flight_list_view'),
            data=json.dumps(self.flight1),
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        flight_json = json.loads(res.content)

        res = self.client.put(
            path=reverse('flight_detail_view',  kwargs={"pk": flight_json["id"]}),
            data=json.dumps(self.flight_changed),
            content_type='application/json',
            **self.headers
        )

        res_json = json.loads(res.content)

        self.assertEqual(res_json["flight_name"], self.flight_changed["flight_name"])
        self.assertEqual(res_json["departure"], self.flight_changed["departure"])
        self.assertEqual(res_json["destination"], self.flight_changed["destination"])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_get_a_flight(self):

        res = self.client.post(
            path=reverse('flight_list_view'),
            data=json.dumps(self.flight1),
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        flight_json = json.loads(res.content)

        res = self.client.get(
            path=reverse('flight_detail_view',  kwargs={"pk": flight_json["id"]}),
            **self.headers
        )

        res_json = json.loads(res.content)
        self.assertEqual(res.status_code, status.HTTP_200_OK) 
        self.assertEqual(res_json["flight_name"], self.flight1["flight_name"])
        self.assertEqual(res_json["departure"], self.flight1["departure"])
        self.assertEqual(res_json["destination"], self.flight1["destination"])

    def test_flight_not_found(self):

        res = self.client.get(
            path=reverse('flight_detail_view',  kwargs={"pk": 555}),
            **self.headers
        )

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
