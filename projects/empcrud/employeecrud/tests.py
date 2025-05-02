from unittest import mock

from django.test import TestCase

# Create your tests here.


import pytest
from rest_framework.test import APIClient
from rest_framework import status
from .models import Employee


# test method for creating employee success
@pytest.mark.django_db
def test_create_employee_success():
    client = APIClient()
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "salary": "75000.00",
        "designation": "Developer"
    }

    response = client.post("/api/employees/create/", payload, format='json')

    # assert the response
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Alice"
    assert response.data["email"] == "alice@example.com"
    assert float(response.data["salary"]) == 75000.00
    assert response.data["designation"] == "Developer"
    assert Employee.objects.count() == 1


@pytest.fixture
def create_employee():
    return Employee.objects.create(
        name="John",
        email="john@example.com",
        salary="60000.00",
        designation="Engineer"
    )


# test method for getting list of employees
@pytest.mark.django_db
def test_list_employees(create_employee):
    client = APIClient()
    response = client.get("/api/employees/")

    # assert the response
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


# test method for retreving single employee by id
@pytest.mark.django_db
def test_get_employee_success(create_employee):
    client = APIClient()
    response = client.get(f"/api/employees/{create_employee.id}/")

    # assert the response
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "John"


# test method for updating the employee
@pytest.mark.django_db
def test_update_employee_success(create_employee):
    client = APIClient()
    payload = {
        "name": "Updated Name",
        "email": "updated@example.com",
        "salary": "90000.00",
        "designation": "Senior Developer"
    }

    response = client.put(f"/api/employees/{create_employee.id}/update/", payload, format='json')

    # assert the response
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Updated Name"
    assert response.data["email"] == "updated@example.com"
    assert float(response.data["salary"]) == 90000.00


# test method for deleting employee
@pytest.mark.django_db
def test_delete_employee_success():
    employee = Employee.objects.create(
        name="John",
        email="john@example.com",
        salary="60000.00",
        designation="Engineer"
    )

    client = APIClient()
    response = client.delete(f"/api/employees/{employee.id}/delete/")

    # assert the response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Employee.objects.count() == 0


# test method for deleting an employee that does not exists in database
@pytest.mark.django_db
def test_delete_employee_not_found():
    client = APIClient()
    response = client.delete("/api/employees/999/delete/")

    # assert the response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["error"] == "Employee not found"


# test method for update an employee that does not exists in database
@pytest.mark.django_db
def test_update_employee_not_found():
    payload = {
        "name": "Ghost",
        "email": "ghost@example.com",
        "salary": "0.00",
        "designation": "None"
    }

    client = APIClient()
    response = client.put("/api/employees/999/update/", payload, format='json')

    # assert the respononse
    assert response.status_code == status.HTTP_404_NOT_FOUND


# test method for searching an employee
@pytest.mark.django_db
def test_search_employees_success():
    # Create sample employees to test search functionality
    Employee.objects.create(name="Alice", email="alice@example.com", salary=50000.00, designation="Developer")
    Employee.objects.create(name="Bob", email="bob@example.com", salary=60000.00, designation="Manager")

    client = APIClient()

    # Test searching by name
    response = client.get("/api/employees/search/", {'q': 'Alice'})

    # assert the response
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Alice"

    # Test searching by email
    response = client.get("/api/employees/search/", {'q': 'bob@example.com'})

    # assert the response
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["email"] == "bob@example.com"


# test method for where no employees match the search query
@pytest.mark.django_db
def test_search_employees_no_results():
    client = APIClient()

    response = client.get("/api/employees/search/", {'q': 'Nonexistent'})

    # assert the response
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


# test method for checking count of employees
@pytest.mark.django_db
def test_employee_count_success():
    Employee.objects.create(name="Alice", email="alice@example.com", salary=50000.00, designation="Developer")
    Employee.objects.create(name="Bob", email="bob@example.com", salary=60000.00, designation="Manager")

    client = APIClient()
    response = client.get("/api/employees/count/")

    # Assert the response
    assert response.status_code == status.HTTP_200_OK
    assert response.data["total_employees"] == 2


# test method for checking employees when there is no employees
@pytest.mark.django_db
def test_employee_count_no_employees():
    client = APIClient()
    response = client.get("/api/employees/count/")

    # assert the response
    assert response.status_code == status.HTTP_200_OK
    assert response.data["total_employees"] == 0
