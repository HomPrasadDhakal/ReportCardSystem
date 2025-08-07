from drf_yasg import openapi
from django.db.models import Avg, F
from django.db import transaction
from core.logs.logger import logger
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from students.apis.v1.filters import ReportCardFilter
from rest_framework.permissions import IsAuthenticated
from students.apis.v1.pagination import CustomPageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

from students.models import (
    Student,
    Subject,
    ReportCard,
    Mark,
)
from .serializers import (
    StudentSerializer,
    SubjectSerializer,
    ReportCardSerializer,
)

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
                logger.error(f"Error: {serializer.errors}")
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
            }
            logger.error(f"Error : {e}")
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(
        operation_summary="Retrieve a Student data by ID",
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
        try:
            student = get_object_or_404(
                Student.objects.only('id', 'name', 'email', 'date_of_birth'),
                pk=pk
            )
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
            logger.error(f"Error: {e}")
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
            }
            logger.error(f"Error: {e}")
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(
        operation_summary="Update Student data by ID",
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
            student = get_object_or_404(Student.objects.only('id', 'name', 'email', 'date_of_birth'), pk=pk)
        except Student.DoesNotExist as e:
            logger.error(f"Error: {e}")
            return Response(
                {"success": False, "message": "Student not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Student data updated successfully")
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Student data updated successfully"
            })
        else:
            logger.error(f"Error:{serializer.errors}")
            return Response({
                "success": False,
                "errors": serializer.errors,
                "message": "Failed to update student"
            }, status=status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(
        operation_summary="Delete Student data by ID",
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
            student = Student.objects.get(id=pk)
            student.delete()
            logger.info("Student data deleted successfully")
            response = {
                'sucess':True,
                'message':"Data deleted successfully"
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            logger.error(f"Error Student dosen't exist")
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
                logger.error(f"Error: {serializer.errors}")
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
            }
            logger.error(f"Error : {e}")
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_summary="Retrieve a Subject data  by ID",
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
    def retrieve(self, request, pk):
        try:
            subject_obj = get_object_or_404(
                Subject.objects.only('id', 'name', 'code'),
                pk=pk
            )
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
            logger.error(f"Error: {e}")
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
            }
            logger.error(f"Error: {e}")
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(
        operation_summary="Update Subject data by ID",
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
            obj = get_object_or_404(
                Subject.objects.only('id', 'name', 'code'),
                pk=pk
            )
        except Subject.DoesNotExist as e:
            logger.error(f"Error: {e}")
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
            logger.error(f"Error:{serializer.errors}")
            return Response({
                "success": False,
                "errors": serializer.errors,
                "message": "Failed to update subject"
            }, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_summary="Delete subject data by ID",
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
            deleted_count, _ = Student.objects.filter(pk=pk).delete()
            if deleted_count == 0:
                return Response({'success': False, 'message': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
            logger.info("Student data deleted successfully")
            return Response({'success': True, 'message': 'Data deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Subject.DoesNotExist as e:
            logger.error(f"Error: {e}")
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


class ReportCardView(viewsets.ViewSet):
    """
        Handles add and update operations for reportcard model.
        Base classes:
            - viewsets.ViewSet
        Returns:
            - subjectView: Handles add and update operations for reportcard instances.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        operation_summary="Create a New ReportCard with student and marks",
        operation_description="Creates a new reportcard with the required fields: student term and year.",
        request_body=ReportCardSerializer,
        tags=["ReportCard Endpoints"],
        security=[{'Bearer': []}]
    )
    def create(self, request):
        serializer = ReportCardSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                response ={
                    'success': True,
                    'data': serializer.data,
                    'message': 'ReportCard created successfully',
                }
                logger.info("ReportCard created successfully")
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                response = {
                    'success': False,
                    'errors': serializer.errors,
                    'message': 'Failed to create ReportCard',
                }
                logger.error(f"Error: {serializer.errors}")
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                'success': False,
                'message': str(e),
            }
            logger.error(f"Error : {e}")
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    filter_params = [
        openapi.Parameter('year', openapi.IN_QUERY, description="Filter by year", type=openapi.TYPE_INTEGER),
        openapi.Parameter('term', openapi.IN_QUERY, description="Filter by term", type=openapi.TYPE_STRING),
        openapi.Parameter('student', openapi.IN_QUERY, description="Filter by student ID", type=openapi.TYPE_INTEGER),
    ]

    @swagger_auto_schema(
        operation_summary="List All the ReportCards",
        operation_description="Returns a paginated list of report cards with related student data.",
        tags=["ReportCard Endpoints"],
        security=[{'Bearer': []}],
        manual_parameters=filter_params,
        responses={200: ReportCardSerializer(many=True)}
    )
    def list(self, request):
        try:
            queryset = ReportCard.objects.select_related('student').defer(
                'created_date', 'updated_date', 
                'student__created_date', 'student__updated_date'
            )
            filterset = ReportCardFilter(request.GET, queryset=queryset)
            if filterset.is_valid():
                queryset = filterset.qs
            else:
                return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)
            paginator = self.pagination_class()
            paginated_qs = paginator.paginate_queryset(queryset, request)
            serializer = ReportCardSerializer(paginated_qs, many=True)
            logger.info("ReportCard list retrieved successfully")
            return paginator.get_paginated_response({
                'success': True,
                'data': serializer.data,
                'message': 'ReportCards retrieved successfully',
            })
        except Exception as e:
            logger.exception(f"Unexpected error retrieving ReportCard list: {e}")
            return Response({
                'success': False,
                'message': 'An unexpected error occurred',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(
    operation_summary="Retrieve a ReportCard by ID",
    operation_description="Retrieves a specific report card by ID.",
    tags=["ReportCard Endpoints"],
    security=[{'Bearer': []}]
    )
    def retrieve(self, request, pk=None):
        try:
            report_card = ReportCard.objects \
            .select_related('student') \
            .defer('created_date', 'updated_date', 'student__created_date', 'student__updated_date') \
            .get(pk=pk)
            serializer = ReportCardSerializer(report_card)
            logger.info(f"ReportCard [{pk}] retrieved successfully")
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'ReportCard retrieved successfully',
            }, status=status.HTTP_200_OK)
        except ReportCard.DoesNotExist:
            logger.error("ReportCard Dosent Exist")
            return Response({
                'success': False,
                'message': 'ReportCard Dosent Exist',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Unexpected error retrieving ReportCard [{pk}]: {e}")
            return Response({
                'success': False,
                'message': 'An unexpected error occurred',
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(
        operation_summary="Update Marks in report Cards",
        operation_description="update marksin in report cards in reportcards by their ID.",
        request_body=ReportCardSerializer,
        tags=["ReportCard Endpoints"],
        security=[{'Bearer': []}]
    )
    @action(detail=True, methods=['patch'], url_path='update-marks')
    def update_marks(self, request, pk=None):
        try:
            report_card = ReportCard.objects \
                .prefetch_related('marks') \
                .defer(
                    'created_date', 'updated_date',
                    'marks__created_date', 'marks__updated_date'
                ).get(pk=pk)
        except ReportCard.DoesNotExist:
            return Response({
                "success": False,
                "message": "Report card not found."
            }, status=status.HTTP_404_NOT_FOUND)
        marks_data = request.data.get('marks', [])
        if not isinstance(marks_data, list):
            return Response({
                "success": False,
                "message": "Marks must be provided as a list."
            }, status=status.HTTP_400_BAD_REQUEST)
        subject_ids = [m.get('subject') for m in marks_data if 'subject' in m]
        existing_marks = Mark.objects.filter(report_card=report_card, subject_id__in=subject_ids)
        existing_lookup = {m.subject_id: m for m in existing_marks}
        marks_to_update = []
        marks_to_create = []
        try:
            for mark_data in marks_data:
                subject_id = mark_data.get('subject')
                score = mark_data.get('score')
                if subject_id is None or score is None:
                    return Response({
                        "success": False,
                        "message": "Each mark must include both 'subject' and 'score'."
                    }, status=status.HTTP_400_BAD_REQUEST)
                if subject_id in existing_lookup:
                    mark = existing_lookup[subject_id]
                    mark.score = score
                    marks_to_update.append(mark)
                else:
                    marks_to_create.append(
                        Mark(report_card=report_card, subject_id=subject_id, score=score)
                    )
            with transaction.atomic():
                if marks_to_update:
                    Mark.objects.bulk_update(marks_to_update, ['score'])
                if marks_to_create:
                    Mark.objects.bulk_create(marks_to_create)
        except Exception as e:
            return Response({
                "success": False,
                "message": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = ReportCardSerializer(report_card)
        return Response({
            "success": True,
            "message": "Marks updated successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_summary="Report Cards and Yearly Summary by Student and Year",
        operation_description="Fetches report cards and computes yearly average scores by student and year.",
        tags=["ReportCard Endpoints"],
        security=[{'Bearer': []}]
    )
    @action(detail=False, methods=['get'], url_path=r'student/(?P<student_id>\d+)/year/(?P<year>\d+)')
    def report_cards_with_summary(self, request, student_id=None, year=None):
        try:
            report_cards = ReportCard.objects.select_related('student').defer('created_date', 'updated_date', 'student__created_date', 'student__updated_date').filter(student_id=student_id, year=year)
            if not report_cards.exists():
                return Response({
                    "success": False,
                    "message": "No report cards found for this student and year."
                }, status=status.HTTP_404_NOT_FOUND)
            serializer = ReportCardSerializer(report_cards, many=True)
            subject_averages = report_cards.values('marks__subject').annotate(avg_score=Avg('marks__score'))
            overall_avg = report_cards.aggregate(overall_avg=Avg('marks__score'))['overall_avg']
            response = {
                "success": True,
                "data": {
                    "report_cards": serializer.data,
                    "summary": {
                        "average_per_subject": subject_averages,
                        "overall_average": overall_avg
                    }
                },
                "message": "Report cards and summary fetched successfully."
            }
            logger.info("Report cards and summary retrieved successfully.")
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error while fetching report card and summary: {e}")
            return Response({
                "success": False,
                "message": f"Internal server error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)