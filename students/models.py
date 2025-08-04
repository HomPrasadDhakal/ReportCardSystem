from django.db import models

class Student(models.Model):
    """
    Model representing a student in the academic system.
    Base classes:
        - models.Model
    Returns:
        - Student: A student instance containing personal and metadata information
        such as name, email, and date of birth.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'students'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['created_date']


class Subject(models.Model):
    """
    Model representing a subject name and code.
    Base classes:
        - models.Model
    Returns:
        - Subject: A subject instance containing information such as name and code.
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subjects'
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = ['name']

class ReportCard(models.Model):
    """
    Model representing a report card for a student.
    Base classes:
        - models.Model
    Returns:
        - ReportCard: A report card instance containing the student's performance
        in various subjects.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='report_cards')
    term = models.CharField(max_length=2, choices=[('1', 'Term 1'), ('2', 'Term 2'), ('3', 'Term 3')])
    year = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.name} - {self.term} - {self.year}"

    class Meta:
        db_table = 'report_cards'
        verbose_name = 'Report Card'
        verbose_name_plural = 'Report Cards'
        ordering = ['student', 'year']


class Mark(models.Model):
    """
    Model representing marks obtained by a student in a subject and report_card.
    Base classes:
        - models.Model
    Returns:
        - Mark: A mark instance containing the student's score in a subject.
    """
    report_card = models.ForeignKey(ReportCard, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.report_card.student.name} - {self.subject.name} - {self.score}"

    class Meta:
        db_table = 'marks'
        verbose_name = 'Mark'
        verbose_name_plural = 'Marks'
        ordering = ['report_card', 'subject']