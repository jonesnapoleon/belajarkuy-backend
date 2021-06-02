from django.db import models

# Create your models here.

class Modules(models.Model):
    subject = models.CharField(max_length=255)
    classes = models.CharField(max_length=255)
    total = models.IntegerField()
    modules = models.IntegerField()

class Question(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    modules = models.ForeignKey(to=Modules, related_name='question_modules', on_delete=models.CASCADE)
    full_question = models.CharField(max_length=255)
    questionOnly = models.CharField(max_length=255)
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    answer = models.CharField(max_length=5)
    chapter = models.CharField(max_length=255)

class User(models.Model):
    name = models.CharField(max_length=255)

class ModulesStatus(models.Model):
    user = models.ForeignKey(to=User, related_name='modules_user', on_delete=models.CASCADE)
    modules = models.ForeignKey(to=Modules, related_name='modulesstatus_modules', on_delete=models.CASCADE)
    status = models.BooleanField()

class AssignmentHistory(models.Model):
    user = models.ForeignKey(to=User, related_name='assignment_history_user', on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, related_name='assignment_history_question', on_delete=models.CASCADE)
    status = models.BooleanField()