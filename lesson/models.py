from django.db import models
from courses.models import Course


class Lesson(models.Model):
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='lessons')
    lesson_date = models.DateField(verbose_name='Дата урока', blank=True, null=True)
    lesson_name = models.CharField(max_length=100, verbose_name='Наименование урока')
    additional_materials = models.URLField(verbose_name='Дополнительные материалы', blank=True, null=True)
    homework = models.TextField(verbose_name='Домашнее задание', blank=True)
    hw_deadline = models.DateField(verbose_name='Срок сдачи', blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course_name', 'lesson_name'], name='unique_lesson_per_course')
        ]
    
    def __str__(self):
        return f'{self.course}-{self.lesson_date}-{self.lesson_name}-{self.hw_deadline}'