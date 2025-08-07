from celery import shared_task
from core.logs.logger import logger
from django.db.models import Sum, Avg
from students.models import ReportCard
from students.models import StudentTermSummary, Mark

def calculate_grade(score):
    """
    calculate the grade of student according to the score
    Args:
        - score (student marks)
    Returns:
        garde of student
    """
    if score >= 90:
        return 'A+'
    elif score >= 80:
        return 'A'
    elif score >= 70:
        return 'B'
    elif score >= 60:
        return 'C'
    elif score >= 50:
        return 'D'
    else:
        return 'F'


@shared_task
def calculate_student_term_summaries():
    """
    calculate the student terms summaries
    Args:
        -
    Return: create calculated data into StudentTermSummary models
    """
    report_cards = ReportCard.objects.all().select_related('student')
    for rc in report_cards:
        marks = Mark.objects.filter(report_card=rc)
        total = marks.aggregate(total=Sum('score'))['total'] or 0
        average = marks.aggregate(avg=Avg('score'))['avg'] or 0
        grade = calculate_grade(average)
        obj, created = StudentTermSummary.objects.update_or_create(
            student=rc.student,
            term=rc.term,
            year=rc.year,
            defaults={
                'total_score': total,
                'average_score': average,
                'grade': grade,
            }
        )
        if created:
            logger.info(f"Created StudentTermSummary for {rc.student.name}, {rc.term} {rc.year}")
        else:
            logger.info(f"Updated StudentTermSummary for {rc.student.name}, {rc.term} {rc.year}")