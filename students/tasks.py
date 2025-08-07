from celery import shared_task
from django.db.models import Avg
from students.models import ReportCard
from django.core.serializers.json import DjangoJSONEncoder
import json

@shared_task
def avg_calculation_of_reportcard_by_student_by_year(student_id, year):
    print("start celery task....")
    report_cards = ReportCard.objects.select_related('student').defer(
        'created_date', 'updated_date',
        'student__created_date', 'student__updated_date'
    ).filter(student_id=student_id, year=year)
    subject_averages_qs = report_cards.values('marks__subject').annotate(avg_score=Avg('marks__score'))
    subject_averages = list(subject_averages_qs)
    overall_avg = report_cards.aggregate(overall_avg=Avg('marks__score'))['overall_avg']
    report_card_data = list(report_cards.values('id', 'student_id', 'year'))
    result = {
        "subject_averages": list(subject_averages),
        "overall_avg": str(overall_avg) if overall_avg is not None else None,
        "report_cards": list(report_cards.values('id', 'student_id', 'year')),
    }
    # return response
    return json.loads(json.dumps(result, cls=DjangoJSONEncoder))