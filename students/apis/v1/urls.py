from django.urls import path, include
from rest_framework.routers import DefaultRouter
from students.apis.v1 import views as student_views

"""
URL configuration for the academic API endpoints.

Includes:
    - Students
    - Subjects
    - Report Cards
    - Marks

Base classes:
    - rest_framework.routers.DefaultRouter
Returns:
    - Automatically generated routes for viewsets.
"""

app_name = 'students_apis_v1'

router = DefaultRouter()
router.register('apis/v1/students', student_views.StudentView, basename='student')

urlpatterns = router.urls