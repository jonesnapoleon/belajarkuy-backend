from django.views.generic import View
from .models import AssignmentHistory, Question, Modules
from django.http import HttpResponse, JsonResponse
from .constant import Constant
from django.conf import settings

import json
from tqdm import tqdm
import pandas as pd

class QuestionView(View):
    def get(self, request):
        entries = Question.objects.all()
        print(entries)
        return HttpResponse('result')

class ModuleView(View):
    def get(self, request):
        modules = Modules.objects.all()
        
        modules_ret = []
        for module in modules:
            modules_ret.append({
                'id': module.id,
                'subject': module.subject,
                'total_questions': module.total,
                'duration': 6000,
            })

        return JsonResponse({
            'status': True,
            'message': '200',
            'modules': modules_ret
        })

class ModuleDetailView(View):
    def get(self, request, *args, **kwargs):
        module_id = kwargs['id']

        questions = Question.objects.filter(modules__id=module_id)

        questions_ret = []
        for question in questions:
            options = []
            if question.option_1 is not None:
                options.append(question.option_1)
            if question.option_2 is not None:
                options.append(question.option_2)
            if question.option_3 is not None:
                options.append(question.option_3)
            if question.option_4 is not None:
                options.append(question.option_4)

            questions_ret.append({
                'id': question.id,
                'questions': question.questionOnly,
                'options': options,
                'correct_answer': question.answer
            })

        return JsonResponse({
            'status': True,
            'message': '200',
            'questions': questions_ret
        })
    
    def post(self, request, *args, **kwargs):
        raw_body = request.body.decode('utf-8')
        body = json.loads(raw_body)
        user_id = kwargs['id']

        for question in body:
            AssignmentHistory.objects.create(user_id=user_id, question_id=question['questions'], status=question['correct'])
        
        return JsonResponse({
            'status': True,
            'message': '200'
        })

class RecommendationDetailView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs['id']
        subject = kwargs['subject']
        
        histories = AssignmentHistory.objects.filter(question__modules__subject=subject, user__id=user_id, status=False)
        false_id = [history.question.id for history in histories][:5]
        
        recommendations = []
        for id in tqdm(false_id, total=len(false_id)):
            recommendation = settings.MODEL.get_recommendations(id)
            recommendations += recommendation
        
        questions = []
        for recommendation in recommendations:
            options = []
            if not pd.isnull(recommendation['opt1']):
                options.append(recommendation['opt1'])
            if not pd.isnull(recommendation['opt2']):
                options.append(recommendation['opt2'])
            if not pd.isnull(recommendation['opt3']):
                options.append(recommendation['opt3'])
            if not pd.isnull(recommendation['opt4']):
                options.append(recommendation['opt4'])

            questions.append({
                'id': recommendation['q_id'],
                'questions': recommendation['questions'],
                'options': options,
                'correct_answer': recommendation['ans']
            })
        
        return JsonResponse({
            'status': True,
            'message': '200',
            'questions': questions
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