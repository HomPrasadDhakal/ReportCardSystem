from django.test import TestCase
from datetime import date
from students.models import Student, Subject, ReportCard, Mark, StudentTermSummary

class StudentModelTest(TestCase):
    """
    this call is testcase for the student model
    Args:
        - Baseclass (TestCase)
    Returns:
        - None
    Tests:
        - String representation of Student
        - Unique constraint on email field
        - Correct setting of date_of_birth
        - Auto-setting of created_date and updated_date
        - Model meta options like db_table and ordering
    """
    def setUp(self):
        self.student = Student.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            date_of_birth=date(2000, 1, 1)
        )

    def test_str_method(self):
        self.assertEqual(str(self.student), "John Doe")

    def test_email_unique(self):
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Student.objects.create(
                name="Jane Doe",
                email="john.doe@example.com",
                date_of_birth=date(1999, 12, 12)
            )

    def test_date_of_birth_field(self):
        self.assertEqual(self.student.date_of_birth, date(2000, 1, 1))

    def test_created_and_updated_date_auto_set(self):
        self.assertIsNotNone(self.student.created_date)
        self.assertIsNotNone(self.student.updated_date)
        self.assertEqual(self.student.created_date, self.student.updated_date)

    def test_meta_options(self):
        self.assertEqual(Student._meta.db_table, 'students')
        self.assertEqual(Student._meta.verbose_name, 'Student')
        self.assertEqual(Student._meta.verbose_name_plural, 'Students')
        self.assertEqual(Student._meta.ordering, ['created_date'])


class SubjectModelTest(TestCase):
    """
    This class contains test cases for the Subject model.
    Args:
        - Baseclass (TestCase): Sets up test database and environment
    Returns:
        - None
    Tests:
        - String representation of Subject
        - Unique constraint on code field
        - Auto-setting of created_date and updated_date
        - Model meta options like db_table and ordering
    """
    def setUp(self):
        self.subject = Subject.objects.create(
            name="Mathematics",
            code="MATH101"
        )

    def test_str_method(self):
        self.assertEqual(str(self.subject), "Mathematics - MATH101")

    def test_code_unique(self):
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Subject.objects.create(
                name="Physics",
                code="MATH101"
            )

    def test_created_and_updated_date_auto_set(self):
        self.assertIsNotNone(self.subject.created_date)
        self.assertIsNotNone(self.subject.updated_date)
        self.assertEqual(self.subject.created_date, self.subject.updated_date)

    def test_meta_options(self):
        self.assertEqual(Subject._meta.db_table, 'subjects')
        self.assertEqual(Subject._meta.verbose_name, 'Subject')
        self.assertEqual(Subject._meta.verbose_name_plural, 'Subjects')
        self.assertEqual(Subject._meta.ordering, ['name'])


class ReportCardModelTest(TestCase):
    """
    This class contains test cases for the ReportCard model.
    Args:
        - Baseclass (TestCase): Provides test DB setup/teardown.
    Returns:
        - None
    Tests:
        - String representation of ReportCard
        - Unique constraint on student, term, and year
        - Auto-setting of created_date and updated_date
        - Model meta options like db_table, ordering, unique_together
    """
    def setUp(self):
        self.student = Student.objects.create(
            name="Alice Smith",
            email="alice@example.com",
            date_of_birth=date(2001, 5, 15)
        )
        self.report_card = ReportCard.objects.create(
            student=self.student,
            term="Term 1",
            year=2023
        )

    def test_str_method(self):
        expected_str = f"{self.student.name} - Term 1 - 2023"
        self.assertEqual(str(self.report_card), expected_str)

    def test_unique_together_constraint(self):
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            ReportCard.objects.create(
                student=self.student,
                term="Term 1",
                year=2023
            )

    def test_created_and_updated_date_auto_set(self):
        self.assertIsNotNone(self.report_card.created_date)
        self.assertIsNotNone(self.report_card.updated_date)
        self.assertEqual(self.report_card.created_date, self.report_card.updated_date)

    def test_meta_options(self):
        meta = ReportCard._meta
        self.assertEqual(meta.db_table, 'report_cards')
        self.assertEqual(meta.verbose_name, 'Report Card')
        self.assertEqual(meta.verbose_name_plural, 'Report Cards')
        self.assertEqual(meta.ordering, ['student', 'year', 'term'])
        self.assertIn(('student', 'term', 'year'), meta.unique_together)
        indexes = [index.fields for index in meta.indexes]
        self.assertIn(['student', 'year'], indexes)
        self.assertIn(['student', 'term', 'year'], indexes)


class MarkModelTest(TestCase):
    """
    This class contains test cases for the Mark model.
    Args:
        - Baseclass (TestCase): Provides test DB setup/teardown.
    Returns:
        - None
    Tests:
        - String representation of Mark
        - Unique constraint on report_card and subject
        - Auto-setting of created_date and updated_date
        - Model meta options like db_table, ordering, unique_together, and indexes
    """

    def setUp(self):
        self.student = Student.objects.create(
            name="Bob Johnson",
            email="bob@example.com",
            date_of_birth=date(2000, 7, 20)
        )
        self.subject = Subject.objects.create(
            name="History",
            code="HIST100"
        )
        self.report_card = ReportCard.objects.create(
            student=self.student,
            term="Term 2",
            year=2024
        )
        self.mark = Mark.objects.create(
            report_card=self.report_card,
            subject=self.subject,
            score=88.75
        )

    def test_str_method(self):
        expected_str = f"{self.student.name} - {self.subject.name} - {self.mark.score}"
        self.assertEqual(str(self.mark), expected_str)

    def test_unique_together_constraint(self):
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Mark.objects.create(
                report_card=self.report_card,
                subject=self.subject,
                score=92.00
            )

    def test_created_and_updated_date_auto_set(self):
        self.assertIsNotNone(self.mark.created_date)
        self.assertIsNotNone(self.mark.updated_date)
        self.assertEqual(self.mark.created_date, self.mark.updated_date)

    def test_meta_options(self):
        meta = Mark._meta
        self.assertEqual(meta.db_table, 'marks')
        self.assertEqual(meta.verbose_name, 'Mark')
        self.assertEqual(meta.verbose_name_plural, 'Marks')
        self.assertEqual(meta.ordering, ['report_card', 'subject'])
        self.assertIn(('report_card', 'subject'), meta.unique_together)
        indexes = [index.fields for index in meta.indexes]
        self.assertIn(['report_card', 'subject'], indexes)


class StudentTermSummaryModelTest(TestCase):
    """
    This class tests the StudentTermSummary model.
    Args:
        - Baseclass (TestCase): Provides testing framework and DB setup.
    Returns:
        - None
    Tests:
        - Creating a StudentTermSummary instance
        - unique_together constraint for (student, term, year)
        - Auto update of calculated_date field
        - Meta options validation
    """
    def setUp(self):
        self.student = Student.objects.create(
            name="Alice Smith",
            email="alice@example.com",
            date_of_birth=date(2001, 5, 15)
        )
        self.summary = StudentTermSummary.objects.create(
            student=self.student,
            term="Term 1",
            year=2024,
            total_score=450.50,
            average_score=90.10,
            grade="A"
        )

    def test_create_student_term_summary(self):
        self.assertEqual(self.summary.student, self.student)
        self.assertEqual(self.summary.term, "Term 1")
        self.assertEqual(self.summary.year, 2024)
        self.assertEqual(float(self.summary.total_score), 450.50)
        self.assertEqual(float(self.summary.average_score), 90.10)
        self.assertEqual(self.summary.grade, "A")
        self.assertIsNotNone(self.summary.calculated_date)

    def test_unique_together_constraint(self):
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            StudentTermSummary.objects.create(
                student=self.student,
                term="Term 1",
                year=2024,
                total_score=400,
                average_score=80,
                grade="B"
            )

    def test_meta_options(self):
        meta = StudentTermSummary._meta
        self.assertEqual(meta.db_table, 'student_term_summaries')
        self.assertEqual(meta.verbose_name, 'StudentTermSummary')
        self.assertEqual(meta.verbose_name_plural, 'StudentTermSummary')
        self.assertIn(('student', 'term', 'year'), meta.unique_together)