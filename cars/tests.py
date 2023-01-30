from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Car

# Create your tests here.

class CarTests(APITestCase):
    # In Python, the @classmethod decorator is used to declare a method in the class as a class method that can be called using ClassName.MethodName()
    # click the blue circle, this overrides a particular method
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_car = Car.objects.create(
            name="M3",
            owner=testuser1,
            description="A Nice BMW",
        )
        test_car.save()


    def test_cars_model(self):
        car = Car.objects.get(id=1)
        actual_owner = str(car.owner)
        actual_name = str(car.name)
        actual_description = str(car.description)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_name, "M3")
        self.assertEqual(
            actual_description, "A Nice BMW"
        )

    def test_get_car_list(self):
        url = reverse("car_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cars = response.data
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0]["name"], "M3")


    def test_get_car_by_id(self):
        url = reverse("car_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        car = response.data
        self.assertEqual(car["name"], "M3")


    def test_create_car(self):
        url = reverse("car_list")
        data = {"owner": 1, "name": "Z3", "description": "A nice convertible BMW"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cars = Car.objects.all()
        self.assertEqual(len(cars), 2)
        self.assertEqual(Car.objects.get(id=2).name, "Z3")

    def test_update_car(self):
        url = reverse("car_detail", args=(1,))
        data = {
            "owner": 1,
            "name": "Z3",
            "description": "A nice convertible BMW",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        car = Car.objects.get(id=1)
        self.assertEqual(car.name, data["name"])
        self.assertEqual(car.owner.id, data["owner"])
        self.assertEqual(car.description, data["description"])

    def test_delete_car(self):
        url = reverse("car_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        cars = Car.objects.all()
        self.assertEqual(len(cars), 0)
