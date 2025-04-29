from django.urls import path
from . import views

urlpatterns = [
    path('employees/search/', views.search_employees, name='search_employees'),
    path('employees/', views.list_employees, name='list-employees'),
    path('employees/create/', views.create_employee, name='create-employee'),
    path('employees/<int:pk>/', views.get_employee, name='get-employee'),
    path('employees/<int:pk>/update/', views.update_employee, name='update-employee'),
    path('employees/<int:pk>/delete/', views.delete_employee, name='delete-employee'),
    path('api/status/', views.api_status, name='api_status'),
]
