from django.urls import path, include
from lesson.views import (courses_list, course_lesson, lesson_detail, 
                         create_lesson, update_lesson, delete_lesson)

urlpatterns = [
    path('courses/', courses_list, name='courses-list'),
    path('courses/<int:course_id>/', course_lesson, name='course-lessons-list'),
    path('lesson/<int:lesson_id>/', lesson_detail, name='lesson-detail'),
    path('create/', create_lesson, name='create-lesson'),
    path('update/<int:lesson_id>/', update_lesson, name='update-lesson'),
    path('delete/<int:lesson_id>/', delete_lesson, name='delete-lesson'),
]
