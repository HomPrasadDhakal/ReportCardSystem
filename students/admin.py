from django.contrib import admin
from django.db import models
from students.models import (
    Student,
    Subject,
    ReportCard,
    Mark,
)
from django.contrib.admin.widgets import AdminDateWidget


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Student instances in the academic system.
    Base classes:
        - admin.ModelAdmin
    Responsibilities:
        - Display and edit Student fields such as name, email, and date of birth.
        - Provide search and filter capabilities in the admin interface.
        - Show created and updated timestamps as read-only fields.
        - Organize form fields using fieldsets for better clarity.
    """
    list_display = ['id', 'name', 'email', 'date_of_birth', 'created_date', 'updated_date']
    list_display_links = ['id', 'name']
    search_fields = ['name', 'email']
    list_filter = ['created_date', 'updated_date']
    readonly_fields = ['created_date', 'updated_date']

    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'date_of_birth'),
        }),
        ('Timestamps', {
            'fields': ('created_date', 'updated_date'),
        }),
    )

    formfield_overrides = {
        models.CharField: {'widget': admin.widgets.AdminTextInputWidget(attrs={'style': 'width: 100%;'})},
        models.EmailField: {'widget': admin.widgets.AdminEmailInputWidget(attrs={'style': 'width: 100%;'})},
        models.DateField: {'widget': AdminDateWidget(attrs={'style': 'width: 930px;'})},
    }


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Subject instances in the academic system.
    Base classes:
        - admin.ModelAdmin
    Returns:
        - Display and edit Subject fields such as name and code.
        - Provide search and filter capabilities in the admin.
        - Show created and updated timestamps as read-only.
    """
    list_display = ['id', 'name', 'code', 'created_date', 'updated_date']
    list_display_links = ['id', 'name']
    search_fields = ['name', 'code']
    list_filter = ['created_date', 'updated_date']
    readonly_fields = ['created_date', 'updated_date']

    fieldsets = (
        ('Subject Information', {
            'fields': ('name', 'code'),
        }),
        ('Timestamps', {
            'fields': ('created_date', 'updated_date'),
        }),
    )

    formfield_overrides = {
        models.CharField: {'widget': admin.widgets.AdminTextInputWidget(attrs={'style': 'width: 100%;'})},
    }


@admin.register(ReportCard)
class ReportCardAdmin(admin.ModelAdmin):
    """
    Admin interface for managing ReportCard instances in the academic system.
    Base classes:
        - admin.ModelAdmin
    Returns:
        - Display and edit ReportCard fields such as student, term, and year.
        - Provide search and filter capabilities in the admin.
        - Show created and updated timestamps as read-only.
    """
    list_display = ['id', 'student', 'term', 'year', 'created_date', 'updated_date']
    list_display_links = ['id', 'student']
    search_fields = ['student__name', 'year']
    list_filter = ['term', 'year', 'created_date', 'updated_date']
    readonly_fields = ['created_date', 'updated_date']

    fieldsets = (
        ('ReportCard Details', {
            'fields': ('student', 'term', 'year'),
        }),
        ('Timestamps', {
            'fields': ('created_date', 'updated_date'),
        }),
    )

    formfield_overrides = {
        models.CharField: {'widget': admin.widgets.AdminTextInputWidget(attrs={'style': 'width: 100%;'})},
        models.IntegerField: {'widget': admin.widgets.AdminTextInputWidget(attrs={'style': 'width: 100%;'})},
    }


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Mark instances in the academic system.
    Base classes:
        - admin.ModelAdmin
    Returns:
        - Display and edit Mark fields such as report card, subject, and score.
        - Provide search and filter capabilities in the admin.
        - Show created and updated timestamps as read-only.
    """
    list_display = ['id', 'report_card', 'subject', 'score', 'created_date', 'updated_date']
    list_display_links = ['id', 'report_card']
    search_fields = ['report_card__student__name', 'subject__name']
    list_filter = ['subject', 'created_date', 'updated_date']
    readonly_fields = ['created_date', 'updated_date']

    fieldsets = (
        ('Mark Details', {
            'fields': ('report_card', 'subject', 'score'),
        }),
        ('Timestamps', {
            'fields': ('created_date', 'updated_date'),
        }),
    )

    formfield_overrides = {
        models.DecimalField: {'widget': admin.widgets.AdminTextInputWidget(attrs={'style': 'width: 100%;'})},
    }