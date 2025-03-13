from django.urls import path
from .views import CourseManageAPIView, StudentCourseAdd

urlpatterns = [
    path('courses/', CourseManageAPIView.as_view(), name='course-list'),
    path('courses/<str:course_name>/', CourseManageAPIView.as_view(), name='course-manager'),
    path('user-manager/', StudentCourseAdd.as_view(), name='course-user-manager')
       
]
