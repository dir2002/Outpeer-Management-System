from django.urls import path, include
from .views import CourseManageAPIView, StudentManageAPIView

urlpatterns = [
    path('courses/', CourseManageAPIView.as_view(), name='course-list'),
    path('courses/<int:course_id>/', CourseManageAPIView.as_view(), name='course-manager'),
    path('user-manage/<int:user_id>/', StudentManageAPIView.as_view(), name='course-user-manager'),
          
]
