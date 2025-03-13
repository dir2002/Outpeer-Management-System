from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


from .models import Course
from users.models import CustomUser
from .serializers import CourseSerializer, CourseReadSerializer


class CourseManageAPIView(APIView):
    
    def get(self, request, course_name=None):
        if course_name:
            course = Course.objects.filter(course_name=course_name)
            if not course.exists():
                return Response({"error": "Курс не найден"}, status=status.HTTP_404_NOT_FOUND)
        else:
            course = Course.objects.all()
        serializer = CourseReadSerializer(course, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        is_list = isinstance(data, list)  
        serializer = CourseSerializer(data=data, many=is_list)
        if serializer.is_valid():
            course = serializer.save()
            return Response(CourseReadSerializer(course, many=is_list).data, status=status.HTTP_201_CREATED)
        return Response({"error": "Невозможно добавить курс. Проверьте параметры запроса."}, status=status.HTTP_400_BAD_REQUEST)
  
    def put(self, request, course_name):
        course = get_object_or_404(Course, course_name=course_name)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            return Response(CourseReadSerializer(course).data, status=status.HTTP_200_OK)
        return Response({"error": "Ошибка при обновлении информации. Проверьте параметры запроса."}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, course_name):
        course = get_object_or_404(Course, course_name=course_name)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            course = serializer.save()
            return Response(CourseReadSerializer(course).data, status=status.HTTP_200_OK)
        return Response({"error": "Ошибка при обновлении информации. Проверьте параметры запроса."}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, course_name=None):
        if course_name:
            course = Course.objects.filter(course_name=course_name)
            if not course.exists():
                return Response({"error": f"Курс {course_name} не найден в Базе данных. Проверьте правильность ввода данных."}, status=status.HTTP_404_NOT_FOUND)
            course.delete()
            return Response({"message": f"Курс {course_name} успешно удален"}, status=status.HTTP_204_NO_CONTENT)
        else:
            Course.objects.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class StudentCourseAdd(APIView):
    def post(self, request):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        course_name = request.data.get("course_name")

        if not first_name or not last_name or not course_name:
            return Response({"error": "Проверьте параметры запроса"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(CustomUser, first_name=first_name, last_name=last_name)
        course = get_object_or_404(Course, course_name=course_name)

        if course.participants.filter(id=user.id).exists():
            return Response({"error": "Студент уже записан на данный курс"}, status=status.HTTP_400_BAD_REQUEST)
        
        course.participants.add(user)
        serializer = CourseReadSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        course_name = request.data.get("course_name")

        if not first_name or not last_name or not course_name: 
            return Response({"error": "Проверьте параметры запроса"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(CustomUser, first_name=first_name, last_name=last_name)
        course = get_object_or_404(Course, course_name=course_name)

        if not course.participants.filter(id=user.id).exists():
            return Response({"error": "Студент не записан на данный курс"}, status=status.HTTP_400_BAD_REQUEST)
        
        course.participants.remove(user)
        serializer = CourseReadSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
