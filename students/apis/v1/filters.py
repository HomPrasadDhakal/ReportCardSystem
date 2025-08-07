import django_filters
from students.models import ReportCard

class ReportCardFilter(django_filters.FilterSet):
    """
    FilterSet for filtering ReportCard queryset based on year, term, and student.
    Args:
        - django_filters.FilterSet: Base class from django-filter used for filtering querysets.
    Returns:
        - django_filters.FilterSet: A filtered queryset based on the provided query parameters.
    """
    class Meta:
        model = ReportCard
        fields = {
            'year': ['exact'],
            'term': ['exact'],
            'student': ['exact'],
        }
