from django.db import models

# Create your models here.


class Question(models.Model):
    questionId = models.CharField(max_length=233)
    full_question = models.CharField(max_length=233)
    option_1 = models.CharField(max_length=233)
    option_2 = models.CharField(max_length=233)
    option_3 = models.CharField(max_length=233)
    option_4 = models.CharField(max_length=233)
    answer = models.CharField(max_length=5)
