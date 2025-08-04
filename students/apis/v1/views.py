from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from students.models import Student
from .serializers import StudentSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class StudentView(viewsets.ViewSet):
    """
    Handles CRUD operations for students model.
    Base classes:
        - viewsets.ViewSet
    Returns:
        - StudentView: Handles CRUD operations for Student instances.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a New Student",
        operation_description="Creates a new student with the required fields: name, email, and date of birth.",
        request_body=StudentSerializer,
        responses={
            201: openapi.Response(
                description="Student created successfully", 
                schema=StudentSerializer,
                examples={
                    "application/json": {
                        "success": True,
                        "data": {
                            "name": "Hom Prasad Dhakal",
                            "email": "test@example.com",
                            "date_of_birth": "2000-01-01",
                        },
                        "message": "Student created successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=StudentSerializer,
                examples={
                    "application/json": {
                        "success": False,
                        "errors": {
                            "name": ["This field is required."],
                            "email": ["This field is required."],
                            "date_of_birth": ["This field is required."]
                        },
                        "message": "Failed to create student"
                    }
                }
            ), 
            500: openapi.Response(
                description="internal server error",
                schema=StudentSerializer,
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Internal server error"
                    }
                }
            ),
        },
        tags=["Students"],
        security=[{'Bearer': []}]
    )
    def create(self, request):
        """POST /students/ - Create a new student"""
        serializer = StudentSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                response ={
                    'success': True,
                    'data': serializer.data,
                    'message': 'Student created successfully',
                }
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                response = {
                    'success': False,
                    'errors': serializer.errors,
                    'message': 'Failed to create student',
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    @swagger_auto_schema(
        operation_summary="Retrieve a Student data",
        operation_description="retrieves a student by their ID.",
        request_body=None,
        responses={
            200: openapi.Response(
                description="data fetched successfully", 
                schema=None,
                examples={
                    "application/json": {
                        "success": True,
                        "data": {
                            "name": "Hom Prasad Dhakal",
                            "email": "test@example.com",
                            "date_of_birth": "2000-01-01",
                        },
                        "message": "data fetched successfully"
                    }
                }
            ),
            404: openapi.Response(
                description="Student not found",
                schema=None,
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Student not found"
                    }
                }
            ), 
            500: openapi.Response(
                description="internal server error",
                schema=None,
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Internal server error"
                    }
                }
            ),
        },
        tags=["Students"],
        security=[{'Bearer': []}]
    )
    def retrieve(self, request, pk=None):
        """GET /students/{id}/ - Retrieve student by ID"""
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student)
            response = {
                'success': True,
                'data': serializer.data,
                'message': 'Student retrieved successfully',
            }
            return Response(response, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            response = {
                'success': False,
                'message': 'Student not found',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_summary="Update Student data",
        operation_description="update student by their ID.",
        request_body=StudentSerializer,
        responses={
            200: openapi.Response(
                description="data updated successfully", 
                schema=StudentSerializer,
                examples={
                    "application/json": {
                        "success": True,
                        "data": {
                            "name": "Hom Prasad Dhakal",
                            "email": "test@example.com",
                            "date_of_birth": "2000-01-01",
                        },
                        "message": "data updated successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=None,
                examples={
                    "application/json": {
                        "success": False,
                        "errors": {
                            "name": ["This field is required."],
                            "email": ["This field is required."],
                            "date_of_birth": ["This field is required."]
                        },
                        "message": "Failed to create student"
                    }
                }
            ), 
            404: openapi.Response(
                description="Student not found",
                schema=None,
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Student not found"
                    }
                }
            ),
            500: openapi.Response(
                description="internal server error",
                schema=None,
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Internal server error"
                    }
                }
            ),
        },
        tags=["Students"],
        security=[{'Bearer': []}]
    )
    def update(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(
                {"success": False, "message": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Student updated successfully"
            })
        else:
            return Response({
                "success": False,
                "errors": serializer.errors,
                "message": "Failed to update student"
            }, status=status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(
        operation_summary="Delete Student data",
        operation_description="Delete student by their ID.",
        request_body=None,
        responses={
            204: openapi.Response(
                description="Data deleted successfully", 
                schema=None,
                examples={
                    "application/json": {
                        "success": True,
                        "message": "data deleted successfully"
                    }
                }
            ),
            404: openapi.Response(
                description="Student not found",
                schema=None,
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Student not found"
                    }
                }
            ),
            500: openapi.Response(
                description="internal server error",
                schema=None,
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Internal server error"
                    }
                }
            ),
        },
        tags=["Students"],
        security=[{'Bearer': []}]
    )
    def destroy(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
            student.delete()
            response = {
                'sucess':True,
                'message':" data delete sucessfully"
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Student not found"
                }, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Internal server error"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

