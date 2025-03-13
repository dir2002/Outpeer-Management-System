from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from datetime import timedelta


class CustomUser(AbstractUser):
    USER_ROLE = [
        ('Студент', 'Студент'),
        ('Менеджер', 'Менеджер'),
        ('Администратор', 'Администратор'),
        ('Учитель', 'Учитель'),
    ]
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    role = models.CharField(max_length=15, choices=USER_ROLE, verbose_name='Роль')
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
   
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"
    

    def save(self, *args, **kwargs):
        if self.is_superuser:  
            self.is_active = True
        super().save(*args, **kwargs)

def generate_token():
    return get_random_string(28)

class EmailActivation(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True, default=generate_token)  
    is_active = models.BooleanField(default=False)
        
    def send_email(self):
        subject = 'Подтверждение email'
        message = f'Подтвердите свой email, перейдя по ссылке http://localhost:8000/users/activate/{self.token}/'
        from_email = 'admin@localhost'
        recipient_list = [self.user.email]

        print(f"Токен для подтверждения почты: {self.token}")

        send_mail(subject, message, from_email, recipient_list)

        print('#' * 20)
        print('Email sent')
        print('#' * 20)

    def activate_user(token: str):
        activation = get_object_or_404(EmailActivation, token=token)
        user = activation.user
        user.is_active = True
        user.save()
        activation.delete()