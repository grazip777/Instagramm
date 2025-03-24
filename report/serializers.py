from rest_framework import serializers
from .models import Report, ReportCategory

# Категория
class ReportCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportCategory
        fields = '__all__'

# Жалоба
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

    def validate(self, data):
        if data['user'] == data['to']:
            raise serializers.ValidationError("A user cannot report themselves.")
        return data

    def validate_reason(self, value):
        if not value.strip():
            raise serializers.ValidationError("The reason for reporting cannot be blank or empty.")
        return value
