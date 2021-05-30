from django.db import models

# Create your models here.

class Modules(models.Model):
    subject = models.CharField(max_length=512)
    classes = models.CharField(max_length=512)
    modules = models.IntegerField()

class Question(models.Model):
    id = models.CharField(max_length=512, primary_key=True)
    modules = models.ForeignKey(to=Modules, related_name='question_modules', on_delete=models.CASCADE)
    full_question = models.CharField(max_length=512)
    questionOnly = models.CharField(max_length=512)
    option_1 = models.CharField(max_length=512)
    option_2 = models.CharField(max_length=512)
    option_3 = models.CharField(max_length=512)
    option_4 = models.CharField(max_length=512)
    answer = models.CharField(max_length=5)
    chapter = models.CharField(max_length=512)

class User(models.Model):
    name = models.CharField(max_length=512)

class ModulesStatus(models.Model):
    user = models.ForeignKey(to=User, related_name='modules_user', on_delete=models.CASCADE)
    modules = models.ForeignKey(to=Modules, related_name='modulesstatus_modules', on_delete=models.CASCADE)
    status = models.BooleanField()

class AssignmentHistory(models.Model):
    user = models.ForeignKey(to=User, related_name='assignment_history_user', on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, related_name='assignment_history_question', on_delete=models.CASCADE)
    status = models.BooleanField()