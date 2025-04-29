from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from .serializers import EmployeeSerializer


# CREATE Employee
@api_view(['POST'])
def create_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'employee data created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# LIST all Employees
@api_view(['GET'])
def list_employees(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_employee(request, pk):
    employee = Employee.objects.filter(pk=pk).first()

    if not employee:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = EmployeeSerializer(employee)
    return Response(serializer.data)


# UPDATE Employee
@api_view(['PUT'])
def update_employee(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = EmployeeSerializer(employee, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE Employee
@api_view(['DELETE'])
def delete_employee(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

    employee.delete()
    return Response({'message': 'Employee deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# SEARCH Employees
@api_view(['GET'])
def search_employees(request):
    query = request.query_params.get('q', None)

    if query:
        # Search employees by name or email
        employees = Employee.objects.filter(
            Q(name__icontains=query) | Q(email__icontains=query)
        )
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    else:
        return Response({'error': 'Please provide a search query'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_status(request):
    return Response({'status': 'API is running successfully!'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def filter_employees_by_position(request):
    position = request.query_params.get('position', None)

    if position:
        # Filter employees by position
        employees = Employee.objects.filter(position__iexact=position)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    else:
        return Response({'error': 'Please provide a position to filter by'}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def employee_count(request):
    total_employees = Employee.objects.count()
    return Response({'total_employees': total_employees}, status=status.HTTP_200_OK)
