from django.urls import path, include
from lesson.views import (CourseListApiView, LessonCourseApiView, LessonDetailRetrieveApiView, 
                          CreateLessonsCreateAPIView, UpdateLessonUpdateApiView, DeleteLessonDestroyAPIView)

urlpatterns = [
    path('courses/', CourseListApiView.as_view(), name='courses-list'),
    path('course/<str:course_name>/', LessonCourseApiView.as_view(), name='course-lessons-list'),
    path('lesson/<str:lesson_name>/', LessonDetailRetrieveApiView.as_view(), name='lesson-detail'),
    path('create/', CreateLessonsCreateAPIView.as_view(), name='create-lesson'),
    path('update/', UpdateLessonUpdateApiView.as_view(), name='update-lesson'),
    path('delete/<str:course_name>/<str:lesson_name>/', DeleteLessonDestroyAPIView.as_view(), name='delete-lesson'),
]
