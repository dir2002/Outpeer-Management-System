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

class CourseListSerializer(serializers.ModelSerializer):
    number_of_students = serializers.SerializerMethodField()
    teacher_name = serializers.SerializerMethodField()
    number_of_lessons = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'description', 'number_of_students', 'teacher_name', 'number_of_lessons']

    def get_number_of_students(self, obj):
        return obj.participants.filter(role="Студент").count()

    def get_teacher_name(self, obj):
        teachers = obj.participants.filter(role="Учитель")
        if teachers.exists():
           return ", ".join([f"{teacher.first_name} {teacher.last_name}" for teacher in teachers])
        return None
    
    def get_number_of_lessons(self, obj):
        return obj.lessons.count()