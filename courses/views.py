from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


from .models import Course
from users.models import CustomUser
from .serializers import CourseSerializer, CourseReadSerializer


class CourseManageAPIView(APIView):
    
    def get(self, request, course_id=None):
        if course_id:
            course = get_object_or_404(Course, pk=course_id)  
            serializer = CourseReadSerializer(course)  
        else:
            courses = Course.objects.all() 
            serializer = CourseReadSerializer(courses, many=True)

        return Response(serializer.data, status=200)
        
    def post(self, request):
        is_list = isinstance(request.data, list) 
        serializer = CourseSerializer(data=request.data, many=is_list)

        if serializer.is_valid():
            course = serializer.save()
            return Response(CourseSerializer(course, many=is_list).data, status=201)
        return Response(serializer.errors, status=400)
       
    def put(self, request, course_id):
        if course_id is None:
            return Response({"error": "ID курса обязателен"}, status=400)
        course = get_object_or_404(Course, pk=course_id)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            return Response(CourseReadSerializer(course).data, status=200)
        return Response({"error": "Ошибка при обновлении информации. Проверьте параметры запроса."}, status=400)

    def patch(self, request, course_id):
        if course_id is None:
            return Response({"error": "ID курса обязателен"}, status=400)
        course = get_object_or_404(Course, pk=course_id)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            course = serializer.save()
            return Response(CourseReadSerializer(course).data, status=200)
        return Response({"error": "Ошибка при обновлении информации. Проверьте параметры запроса."}, status=400)
          
    def delete(self, request, course_id=None):
        if course_id:
            course = get_object_or_404(Course, pk=course_id)
            course.delete()
            return Response({"message": f"Курс {course.course_name} успешно удален"}, status=204)
        else:
            Course.objects.all().delete()
            return Response({"message": f"Все курсы успешно удалены"}, status=204)

class StudentManageAPIView(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        course_name = request.data.get("course_name")
        
        if not course_name:
            return Response({"error": "Проверьте параметры запроса"}, status=400)
        
        course = get_object_or_404(Course, course_name=course_name)

        if course.participants.filter(pk=user.id).exists():
            return Response({"error": f"{user.role} уже записан на данный курс"}, status=400)
        
        course.participants.add(user)
        serializer = CourseReadSerializer(course)
        return Response(serializer.data, status=201)
        
    
    def delete(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        course_name = request.data.get("course_name")
        
        if not course_name:
            return Response({"error": "Проверьте параметры запроса"}, status=400)
        
        course = get_object_or_404(Course, course_name=course_name)
        if not course.participants.filter(pk=user.id).exists():
            return Response({"error": "Студент не записан на данный курс"}, status=400)

        course.participants.remove(user)
        serializer = CourseReadSerializer(course)
        return Response(serializer.data, status=200)