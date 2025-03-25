from rest_framework.permissions import BasePermission

class IsManager(BasePermission):
    def has_permission(self, request, view):
        print(f"Пользователь: {request.user}")  
        print(f"Аутентифицирован: {request.user.is_authenticated}")
        print(f"Группы: {list(request.user.groups.values_list('name', flat=True))}")

        return request.user.is_authenticated and request.user.role == "Менеджер"