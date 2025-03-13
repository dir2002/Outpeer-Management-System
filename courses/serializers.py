from rest_framework import serializers

from .models import Course
from users.models import CustomUser


class CourseSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True, required=False)
    
    class Meta:
        model = Course
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ 'first_name', 'last_name', 'role']


class CourseReadSerializer(serializers.ModelSerializer):
   participants = StudentSerializer(many=True)
   class Meta:
        model = Course
        fields = '__all__'