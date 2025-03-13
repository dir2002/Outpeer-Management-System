from django.db import models
from users.models import CustomUser

class Course(models.Model):
    course_name = models.CharField(max_length=100, verbose_name='Наименование курса')
    description = models.TextField(verbose_name="Описание курса")
    participants = models.ManyToManyField(CustomUser, verbose_name='Участники курса', related_name='courses')
     

    def __str__(self):
        return f'{self.course_name} - {self.description}'