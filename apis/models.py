from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
# from .managers import UserManager


class Modules(models.Model):
    subject = models.CharField(max_length=255)
    classes = models.CharField(max_length=255)
    total = models.IntegerField()
    modules = models.IntegerField()


class Question(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    modules = models.ForeignKey(
        to=Modules, related_name='question_modules', on_delete=models.CASCADE)
    full_question = models.CharField(max_length=255)
    questionOnly = models.CharField(max_length=255)
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)
    answer = models.CharField(max_length=5)
    chapter = models.CharField(max_length=255)


class User(models.Model):
    user_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    # username = None
    # first_name = None
    # last_name = None
    # password = models.CharField(max_length=128, blank=True, null=True)
    # is_active = models.BooleanField(default=True)
    # is_superuser = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    # objects = UserManager()

    def __str__(self):
        return "{} - {}".format(self.user_id, self.email)


class ModulesStatus(models.Model):
    user = models.ForeignKey(
        to=User, related_name='modules_user', on_delete=models.CASCADE)
    modules = models.ForeignKey(
        to=Modules, related_name='modulesstatus_modules', on_delete=models.CASCADE)
    status = models.BooleanField()


class AssignmentHistory(models.Model):
    user = models.ForeignKey(
        to=User, related_name='assignment_history_user', on_delete=models.CASCADE)
    question = models.ForeignKey(
        to=Question, related_name='assignment_history_question', on_delete=models.CASCADE)
    status = models.BooleanField()
