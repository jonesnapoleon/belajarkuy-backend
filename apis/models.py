from django.db import models

# Create your models here.

class Question(models.Model):
    full_question = models.CharField(max_length=233)
    questionOnly = models.CharField(max_length=233)
    option_1 = models.CharField(max_length=233)
    option_2 = models.CharField(max_length=233)
    option_3 = models.CharField(max_length=233)
    option_4 = models.CharField(max_length=233)
    answer = models.CharField(max_length=5)

class Modules(models.Model):
    question = models.ForeignKey(to=Question, related_name='modules', on_delete=models.CASCADE)
    subject = models.CharField(max_length=233)
    classes = models.CharField(max_length=233)
    modules = models.IntegerField()

class User(models.Model):
    name = models.CharField(max_length=233)

class ModulesStatus(models.Model):
    modules = models.ForeignKey(to=Modules, related_name='modules_status', on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, related_name='modules_user', on_delete=models.CASCADE)
    status = models.BooleanField()

class AssignmentHistory(models.Model):
    user = models.ForeignKey(to=User, related_name='assignment_history_user', on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, related_name='assignment_history_question', on_delete=models.CASCADE)
    status = models.BooleanField()
    timestamp = models.DateTimeField()

class Status(models.Model):
    user = models.ForeignKey(to=User, related_name='status_user', on_delete=models.CASCADE)
    chemistry = models.FloatField()
    mathematics = models.FloatField()
    biology = models.FloatField()
    physics = models.FloatField()