from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    #user — привязывает заметку к конкретному пользователю
    title = models.CharField(max_length=200)                    #title — заголовок заметки
    content = models.TextField(blank=True)                      #content — текст заметки
    created_at = models.DateTimeField(auto_now_add=True)        # created_at — дата создания
    due_date = models.DateField(null=True, blank=True)          # due_date — дедлайн
    is_done = models.BooleanField(default=False)                # is_done — выполнена или нет
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
