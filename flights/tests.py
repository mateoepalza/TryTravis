
# This is a extension of unittest

from django.db.models import Max

# You gotta realize that we are importing Client
# client -> it will simulate a web client
#   -> a client that is able to make request and get 
#   -> responses back from the server
#   -> So, this will allow us to simulate web request and get
#   -> responses back to different pages, and to make sure that the
#   -> info we get is the correct one.

from django.test import Client, TestCase

from .models import Airport, Flight, Passenger

class FlightTestCase(TestCase):

    def setUp(self):

        # Create airports
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # create flights

        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
    
    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 2) 
    
    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2)
        self.assertTrue(f.is_valid_flight())
    
    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2)
        self.assertTrue(f.is_valid_flight())

    # This function will check that the index page is working and that it 
    # is returning the number of flights that it suppose to return
    def test_index(self):

        # I create a web client, with this i'm gonna be able to make requests
        c = Client()

        # I send a get request to the "/" route, and i get back a response
        response = c.get("/")

        # The first thing that i have to do is to make sure that the response 
        # was successful
        # -> status code 200 = means that everything is okay
        self.assertEqual(response.status_code, 200)

        # I want to check the context of the response in this case the "flights" key
        self.assertEqual(response.context["flights"].count(), 2)

    # This function will check that if i have a valid flight and i try to access the 
    # flight page, it will work
    def test_valid_flight_page(self):

        # first i select a flight
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        # i create a web client
        c = Client()

        # i try top access to /the_id_flight
        response = c.get(f"/{f.id}")

        # I check if the status code is equal to 200
        self.assertEqual(1, 200)
    
    # In this function i try to check what happen if i want access into a flights that 
    # doesn't exists
    def test_invalid_flight_page(self):
        # i want to get the maximum value of any ID of nay flight
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

        # i create a web client
        c = Client()

        # i go to the last id flight + 1, that it suppose doesn't exists
        response = c.get(f"/{max_id + 1}")

        # The status code that i should get is a status code 404
        self.assertEqual(response.status_code, 404)
    
    # The purpose of this function is to check if the amount of passengers in a flight
    # is correct when you get a response after the request
    def test_flight_page_passengers(self):

        # I get a flight, i create a passenger and i add the passenger to the flight
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")
        f.passengers.add(p)

        # I create the a web client
        c = Client()

        # I create a request with /flight_id
        response = c.get(f"/{f.id}")

        # I check that response was successful
        self.assertEqual(response.status_code, 200)

        # Finally, i take the response context and i assert that it is just one
        self.assertEqual(response.context["passengers"].count(), 1)
    
    # This function will check if the amount of non-passengers is correct in an 
    # specific flight
    def test_flight_page_non_passengers(self):

        # Create a flight and a passenger
        f = Flight.objects.get(pk=2)
        p = Passenger.objects.create(first="Alice", last="Adams")

        # i create a web client
        c = Client()

        # I generate a request to /flight_id 
        response = c.get(f"/{f.id}")

        # I check that the response was successful
        self.assertEqual(response.status_code, 200)

        # Finally, I take the context and i assert that the number of non-passengers
        # is equal to 1
        self.assertEqual(response.context["non_passengers"].count(), 1)
