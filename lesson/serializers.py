from rest_framework import serializers
from django.utils.timezone import now
from datetime import timedelta

from .models import Lesson
from courses.models import Course


class LessonSerializer(serializers.ModelSerializer):
    course_name = serializers.SlugRelatedField(slug_field='course_name', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ['id', 'course_name', 'lesson_date', 'lesson_name', 'additional_materials', 'homework', 'hw_deadline']

class LessonCreateUpdateSerializer(serializers.ModelSerializer):
    course_name = serializers.SlugRelatedField(slug_field='course_name', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ['course_name', 'lesson_date', 'lesson_name', 'additional_materials', 'homework', 'hw_deadline']
    
# В качестве тестовой логики для override функций create и update добавил автоматическое проставление срока сдачи домашнего задания 
# при создании или обновлении урока, если он не был передан в запросе
      
    def create(self, validated_data):
        lesson = Lesson.objects.create(**validated_data)
        if lesson.homework and not lesson.hw_deadline: 
            lesson.hw_deadline = lesson.lesson_date + timedelta(days=7)
            lesson.save()
        return lesson
    
    def update(self, instance, validated_data):
        if 'hw_deadline' not in validated_data:
            lesson_date = validated_data.get('lesson_date', instance.lesson_date)
            if 'homework' in validated_data or 'lesson_date' in validated_data:
                instance.hw_deadline = lesson_date + timedelta(days=7)
        return super().update(instance, validated_data)