from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from .serializers import LessonSerializer, LessonCreateUpdateSerializer
from courses.serializers import CourseListSerializer
from courses.models import Course
from .models import Lesson


class CourseListApiView(ListAPIView):
    serializer_class = CourseListSerializer
    queryset = Course.objects.all()
   
class LessonCourseApiView(APIView):
    def get(self, request, course_name):
        course = Course.objects.get(course_name=course_name)
        lessons = Lesson.objects.filter(course=course)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
    
class LessonDetailRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = 'lesson_name'
   
class CreateLessonsCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonCreateUpdateSerializer
  

class UpdateLessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonCreateUpdateSerializer
    
    def get_object(self):
        course_name = self.request.data.get("course")
        lesson_name = self.request.data.get("lesson_name")
        course = get_object_or_404(Course, course_name=course_name)
        lesson = get_object_or_404(Lesson, course=course, lesson_name=lesson_name)
        return lesson
            

class DeleteLessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    
    def get_object(self):
        course_name = self.kwargs.get("course_name")
        lesson_name = self.kwargs.get("lesson_name")
        course = get_object_or_404(Course, course_name=course_name)
        return get_object_or_404(Lesson, course=course, lesson_name=lesson_name)
    
        