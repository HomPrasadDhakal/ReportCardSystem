from rest_framework import serializers
from students.models import Student, Subject, ReportCard, Mark


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer representing a student in the academic system with validation.
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
