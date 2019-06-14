Flight Service
===
a service to create and manage flight schedules

How to run
---
this application can run dev and prod mode
to run application in dev mode run:

    make migrate # to create database for fist time
    make runserver to runserver

to run tests:

    make test

to create docker image run:

    make build

to run application with docker-compose

    cd deployments
    docker-compose up -d


Exposed RESTAPIs
---
create user using username, password and email

    path: /users/register/
    method: POST
    body: 
        type: application/json
        content sample:
            {
                "username": "username",
                "password": "pass",
                "email": "em@em.com"
            }
    returns:
        201:
            {
                "username": "username",
                "password": "password-hash",
                "email": "em@em.com"
            }
        400:
            bad request    

optain token for a user using username and password

    path: /users/register/
    method: POST
    body: 
        type: application/json
        content sample:
            {
                "username": "username",
                "password": "pass",
            }
    returns:
        200:
            {
                "token": "jwt token hash",
            }
        400:
            when username or password is invalid 

create a new flight schedule

    path: /flights/
    method: POST
    headers:
        Authorization: JWT <token> # from login response
    body: 
        type: application/json
        content sample:
            {
                "flight_name": "thr-ist",
                "flight_number": 7777,
                "scheduled_datetime": "2019-06-14T14:17:00",
                "expected_arrival_datetime": "2019-06-14T19:17:00",
                "departure": "thr",
                "destination": "ist",
                "fare": 100,
                "flight_duration": "05:00"
            }
    returns:
        201:
            {
                "id": 1,
                "flight_name": "thr-ist",
                "flight_number": 7777,
                "scheduled_datetime": "2019-06-14T14:17:00Z",
                "expected_arrival_datetime": "2019-06-14T19:17:00Z",
                "departure": "thr",
                "destination": "ist",
                "fare": 100,
                "flight_duration": "05:00:00"
            }
        400:
            when input data is invalid

        401:
            when authorization data is invalid

update a flight schedule

    path: /flights/<int:flightId> # id from flight create response
    method: PUT
    headers:
        Authorization: JWT <token> # from login response    
    body: 
        type: application/json
        content sample:
            {
                "flight_name": "thr-ist",
                "flight_number": 7777,
                "scheduled_datetime": "2019-06-14T14:17:00",
                "expected_arrival_datetime": "2019-06-14T19:17:00",
                "departure": "thr",
                "destination": "ist",
                "fare": 100,
                "flight_duration": "05:00"
            }
    returns:
        200:
            {
                "id": 1,
                "flight_name": "thr-ist",
                "flight_number": 7777,
                "scheduled_datetime": "2019-06-14T14:17:00Z",
                "expected_arrival_datetime": "2019-06-14T19:17:00Z",
                "departure": "thr",
                "destination": "ist",
                "fare": 100,
                "flight_duration": "05:00:00"
            }
        400:
            when input data is invalid

        401:
            when authorization data is invalid

remove a flight schedule

    path: /flights/<int:flightId> # id from flight create response
    method: DELETE
    headers:
        Authorization: JWT <token> # from login response    
    returns:
        204:
           when flight schedule removed
        400:
            when flight schedule is invalid
        401:
            when authorization data is invalid

search for a flight schedule, user can pass ```flight_name```, ```scheduled_date```
```departure```, ```destination``` as url params to search them.

    path: /flights?flight_name=flight-name

    method: GET
    headers:
        Authorization: JWT <token> # from login response    
    returns:
        200:
           {
                "count": 1,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "id": 2,
                        "flight_name": "thr-ist",
                        "flight_number": 7777,
                        "scheduled_datetime": "2019-06-14T14:17:00Z",
                        "expected_arrival_datetime": "2019-06-14T19:17:00Z",
                        "departure": "thr",
                        "destination": "ist",
                        "fare": 100,
                        "flight_duration": "05:00:00"
                    },
                    .
                    .
                    .
                ]
            }
        404:
           when no flight schedule found
        401:
           when authorization data is invalid


Library and tools
---
    Django==2.2.2
    djangorestframework==3.9.4
    djangorestframework-jwt==1.11.0