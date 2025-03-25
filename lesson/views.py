from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from .serializers import LessonSerializer, LessonCreateUpdateSerializer
from courses.serializers import CourseListSerializer
from courses.models import Course
from .models import Lesson
from .permissions import IsManager


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def courses_list(request):
    courses = Course.objects.all()
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data, status=200)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_lesson(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lessons = Lesson.objects.filter(course_name=course)
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    serializer = LessonSerializer(lesson)
    return Response(serializer.data, status=200)

@api_view(['POST'])
@permission_classes([IsManager])
def create_lesson(request):
    is_many = isinstance(request.data, list)
    serializer = LessonCreateUpdateSerializer(data=request.data, many=is_many)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT', 'PATCH'])
def update_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    serializer = LessonCreateUpdateSerializer(lesson, data=request.data, partial=request.method == 'PATCH')

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.delete()
    return Response(status=204)
        