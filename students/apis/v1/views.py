from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from students.models import (
    Student,
    Subject,
)
from .serializers import (
    StudentSerializer,
    SubjectSerializer,
)

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.logs.logger import logger


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
        tags=["Student Endpoints"],
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
                logger.info("student created successfully")
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                response = {
                    'success': False,
                    'errors': serializer.errors,
                    'message': 'Failed to create student',
                }
                logger.warning(f"Error: {serializer.errors}")
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
            }
            logger.error(f"Error : {e}")
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
        tags=["Student Endpoints"],
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
            logger.info("successfully retrive student data")
            return Response(response, status=status.HTTP_200_OK)
        except Student.DoesNotExist as e:
            response = {
                'success': False,
                'message': 'Student not found',
            }
            logger.warning(f"Error: {e}")
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
            }
            logger.warning(f"Error: {e}")
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
        tags=["Student Endpoints"],
        security=[{'Bearer': []}]
    )
    def update(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist as e:
            logger.warning(f"Error: {e}")
            return Response(
                {"success": False, "message": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Student data updated successfully")
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Student data updated successfully"
            })
        else:
            logger.warning(f"Error:{serializer.errors}")
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
        tags=["Student Endpoints"],
        security=[{'Bearer': []}]
    )
    def destroy(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
            student.delete()
            logger.info("Student data deleted successfully")
            response = {
                'sucess':True,
                'message':" data delete sucessfully"
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist as e:
            logger.warning(f"Error: {e}")
            return Response(
                {
                    "success": False,
                    "message": "Student not found"
                }, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error: {e}")
            return Response(
                {
                    "success": False,
                    "message": "Internal server error"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class subjectView(viewsets.ViewSet):
    """
    Handles CRUD operations for subject model.
    Base classes:
        - viewsets.ViewSet
    Returns:
        - subjectView: Handles CRUD operations for Student instances.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a New Subject",
        operation_description="Creates a new Subject with the required fields: name and code.",
        request_body=SubjectSerializer,
        responses={
            201: openapi.Response(
                description="Subject created successfully", 
                schema=SubjectSerializer,
                examples={
                    "application/json": {
                        "success": True,
                        "data": {
                            "name": "computer",
                            "code": "CMP123",
                        },
                        "message": "Subject created successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=SubjectSerializer,
                examples={
                    "application/json": {
                        "success": False,
                        "errors": {
                            "name": ["This field is required."],
                            "code": ["This field is required."]
                        },
                        "message": "Failed to create Subject"
                    }
                }
            ), 
            500: openapi.Response(
                description="internal server error",
                schema=SubjectSerializer,
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Internal server error"
                    }
                }
            ),
        },
        tags=["Subject Endpoints"],
        security=[{'Bearer': []}]
    )
    def create(self, request):
        """POST /Subject/ - Create a new subject"""
        serializer = SubjectSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                response ={
                    'success': True,
                    'data': serializer.data,
                    'message': 'Subject created successfully',
                }
                logger.info("Subject created successfully")
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                response = {
                    'success': False,
                    'errors': serializer.errors,
                    'message': 'Failed to create subject',
                }
                logger.warning(f"Error: {serializer.errors}")
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
            }
            logger.error(f"Error : {e}")
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_summary="Retrieve a Subject data",
        operation_description="retrieves a Subject by their ID.",
        request_body=None,
        responses={
            200: openapi.Response(
                description="data fetched successfully", 
                schema=None,
                examples={
                    "application/json": {
                        "success": True,
                        "data": {
                            "name": "Computer",
                            "code": "CMP234"
                        },
                        "message": "data fetched successfully"
                    }
                }
            ),
            404: openapi.Response(
                description="Subject not found",
                schema=None,
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Subject not found"
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
        tags=["Subject Endpoints"],
        security=[{'Bearer': []}]
    )
    def retrieve(self, request, pk=None):
        """GET /Subject/{id}/ - Retrieve Subject by ID"""
        try:
            subject_obj = Subject.objects.get(pk=pk)
            serializer = SubjectSerializer(subject_obj)
            response = {
                'success': True,
                'data': serializer.data,
                'message': 'Subject retrieved successfully',
            }
            logger.info("successfully retrive subject data")
            return Response(response, status=status.HTTP_200_OK)
        except Subject.DoesNotExist as e:
            response = {
                'success': False,
                'message': 'subject not found',
            }
            logger.warning(f"Error: {e}")
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
            }
            logger.warning(f"Error: {e}")
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(
        operation_summary="Update Subject data",
        operation_description="update Subject by their ID.",
        request_body=SubjectSerializer,
        responses={
            200: openapi.Response(
                description="data updated successfully", 
                schema=SubjectSerializer,
                examples={
                    "application/json": {
                        "success": True,
                        "data": {
                            "name": "Computer",
                            "code": "CMP213"
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
                            "code": ["This field is required."],
                        },
                        "message": "Failed to create subject"
                    }
                }
            ), 
            404: openapi.Response(
                description="subject not found",
                schema=None,
                examples={
                    "application/json": {
                        "success": False,
                        "message": "subject not found"
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
        tags=["Subject Endpoints"],
        security=[{'Bearer': []}]
    )
    def update(self, request, pk=None):
        try:
            obj = Subject.objects.get(pk=pk)
        except Subject.DoesNotExist as e:
            logger.warning(f"Error: {e}")
            return Response(
                {"success": False, "message": "subject not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = SubjectSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Subject data updated successfully")
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Subject data updated successfully"
            })
        else:
            logger.warning(f"Error:{serializer.errors}")
            return Response({
                "success": False,
                "errors": serializer.errors,
                "message": "Failed to update subject"
            }, status=status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(
        operation_summary="Delete subject data",
        operation_description="Delete subject by their ID.",
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
                description="subject not found",
                schema=None,
                examples={
                    "application/json": {
                        "success": False,
                        "message": "subject not found"
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
        tags=["Subject Endpoints"],
        security=[{'Bearer': []}]
    )
    def destroy(self, request, pk=None):
        try:
            obj = Subject.objects.get(pk=pk)
            obj.delete()
            logger.info("Subject data deleted successfully")
            response = {
                'sucess':True,
                'message':" data delete sucessfully"
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except Subject.DoesNotExist as e:
            logger.warning(f"Error: {e}")
            return Response(
                {
                    "success": False,
                    "message": "Subject not found"
                }, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error: {e}")
            return Response(
                {
                    "success": False,
                    "message": "Internal server error"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )