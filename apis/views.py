from django.views.generic import View
from .models import AssignmentHistory, Question
from django.http import HttpResponse, JsonResponse
from .constant import Constant

class QuestionView(View):
    def get(self, request):
        entries = Question.objects.all()
        print(entries)
        return HttpResponse('result')

class RecommendationDetailView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs['id']
        subject = kwargs['subject']

        counter_dict = {}
        correct_dict = {}
        for el in Constant.subject_chapters[subject]:
            counter_dict[el] = 0
            correct_dict[el] = 0
        history = AssignmentHistory.objects.filter(question__modules__subject=subject, user__id=user_id)
        print(history)
        return JsonResponse({
            'a': "Hello"
        })

class CompetencyView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs['id']

        counter_dict = {
            'physics': {},
            'chemistry': {},
            'math': {},
            'biology': {}
        }
        correct_dict = {
            'physics': {},
            'chemistry': {},
            'math': {},
            'biology': {}
        }

        subjects = ['math', 'biology', 'chemistry', 'physics']
        for subject in subjects:
            for chapter in Constant.subject_chapters[subject]:
                counter_dict[subject][chapter] = 0
                correct_dict[subject][chapter] = 0
        
        histories = AssignmentHistory.objects.filter(user__id=user_id)
        
        for history in histories:
            subject = history.question.modules.subject
            chapter = history.question.chapter
            status = history.status

            if counter_dict[subject][chapter] >= 100:
                continue

            counter_dict[subject][chapter] += 1
            if status:
                correct_dict[subject][chapter] += 1

        division = {
            'physics': sum(counter_dict['physics'].values()),
            'chemistry': sum(counter_dict['chemistry'].values()),
            'biology': sum(counter_dict['biology'].values()),
            'math': sum(counter_dict['math'].values()),
        }

        scores = {
            'physics': 0,
            'chemistry': 0,
            'math': 0,
            'biology': 0
        }

        for k, v in division.items():
            if v == 0:
                continue
            scores[k] = sum(correct_dict[subject].values()) / v * 100

        weakness = {
            'physics': [],
            'chemistry': [],
            'biology': [],
            'math': []
        }
        threshold = 0.7
        for subject in subjects:
            for chapter in Constant.subject_chapters[subject]:
                if counter_dict[subject][chapter] == 0:
                    continue
                score = correct_dict[subject][chapter] / counter_dict[subject][chapter]
                if score < threshold:
                    weakness[subject].append(chapter)

        physics = {
            'subject': 'physics',
            'progress': scores['physics'],
            'material': weakness['physics']
        }
        chemistry = {
            'subject': 'chemistry',
            'progress': scores['chemistry'],
            'material': weakness['chemistry']
        }
        biology = {
            'subject': 'biology',
            'progress': scores['biology'],
            'material': weakness['biology']
        }
        math = {
            'subject': 'math',
            'progress': scores['math'],
            'material': weakness['math']
        }

        return JsonResponse({
            'status': True,
            'message': '200',
            'results': [physics, chemistry, biology, math]
        })