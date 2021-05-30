from django.views.generic import View
from .models import Question
from django.http import HttpResponse


class QuestionView(View):
    def get(self, request):
        entries = Question.objects.all()
        print(entries)
        return HttpResponse('result')

# class ModulesView(view):