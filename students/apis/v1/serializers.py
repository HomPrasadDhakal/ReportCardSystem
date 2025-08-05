from rest_framework import serializers
from students.models import Student, Subject, ReportCard, Mark


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer representing a student model with validation.
    Base classes:
        - serializers.ModelSerializer
    Returns:
        - StudentSerializer: A serializer instance for Student fields.
    """
    class Meta:
        model = Student
        fields = ['name', 'email', 'date_of_birth']

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name is required.")
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("Name must not contain numbers.")
        return value
    
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        if not value.endswith(".com"):
            raise serializers.ValidationError("Email must end with '.com'.")
        return value
    
    def validate_date_of_birth(self, value):
        if not value:
            raise serializers.ValidationError("Date of birth is required.")
        if value.year < 1930:
            raise serializers.ValidationError("Date of birth year is too far in the past.")
        if value.year > 2025:
            raise serializers.ValidationError("Date of birth year cannot be in the future.")
        return value


class SubjectSerializer(serializers.ModelSerializer):
    """
        Serializer representing a subject model with validation.
        Base classes:
            - serializers.ModelSerializer
        Returns:
            - SubjectSerializer: A serializer instance for Subject fields.
    """
    class Meta:
        model = Subject
        fields = ['name', 'code']

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name is required.")
        return value
    
    def validate_code(self, value):
        if not value:
            raise serializers.ValidationError("Code is requried.")
        return value

class MarkSerializer(serializers.ModelSerializer):
    """
        Serializer representing a report model with validation.
        Base classes:
            - serializers.ModelSerializer
        Returns:
            - ReportSerializer: A serializer instance for report fields.
    """

    class Meta:
        model = Mark
        fields = ['id', 'subject', 'score']

class ReportCardSerializer(serializers.ModelSerializer):
    """
        Serializer representing a report model with validation.
        Base classes:
            - serializers.ModelSerializer
        Returns:
            - ReportSerializer: A serializer instance for report fields.
    """
    marks = MarkSerializer(many=True)

    class Meta:
        model = ReportCard
        fields = ['id', 'student', 'year', 'term', 'marks']

    def create(self, validated_data):
        marks_data = validated_data.pop('marks')
        report_card = ReportCard.objects.create(**validated_data)
        for mark in marks_data:
            Mark.objects.create(report_card=report_card, **mark)
        return report_card

    def update(self, instance, validated_data):
        marks_data = validated_data.pop('marks')
        instance.term = validated_data.get('term', instance.term)
        instance.year = validated_data.get('year', instance.year)
        instance.save()

        for mark_data in marks_data:
            Mark.objects.update_or_create(
                report_card=instance,
                subject=mark_data['subject'],
                defaults={'score': mark_data['score']}
            )

        return instance