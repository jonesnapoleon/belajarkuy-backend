from django.views.generic import View
from .models import *
from django.http import HttpResponse, JsonResponse
from .constant import Constant
# from django.utils.decorators import method_decorator
from google.auth.transport import requests
from django.contrib.auth import authenticate
from google.oauth2 import id_token

import os

import json
from tqdm import tqdm
import pandas as pd

import random


def register_social_user(user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email, user_id=user_id)

    if filtered_user_by_email.exists():
        return {
            'name': name,
            'email': email,
        }
    else:
        user = {'name': name, 'email': email, 'user_id': user_id}
        user = User.objects.create(**user)
        user.save()

        return {
            'email': email,
            'name': name,
        }


class AuthView(View):

    def validate_auth_token(self, auth_token):
        try:
            user_data = id_token.verify_oauth2_token(
                auth_token, requests.Request(),
                os.environ.get('GOOGLE_CLIENT_ID')
            )

            user_id = user_data['sub']
            email = user_data['email']
            name = user_data['name']

            return register_social_user(user_id=user_id, email=email, name=name)
        except Exception as e:
            raise e

    def post(self, request):

        body = json.loads(request.body)
        token = body['token']

        if token is None:
            return JsonResponse({'status': False, 'message': 'No token'}, status=400)
        try:
            res = self.validate_auth_token(token)
            print(res)
            return JsonResponse({'status': True, 'message': res}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'status': False, 'message': str(e)}, status=400)


class QuestionView(View):
    def get(self, request):
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
            AssignmentHistory.objects.create(
                user_id=user_id, question_id=question['questions'], status=question['correct'])

        return JsonResponse({
            'status': True,
            'message': '200'
        })


class RecommendationDetailView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        subject = kwargs['subject']

        # histories = AssignmentHistory.objects.filter(question__modules__subject=subject, user__id=user_id, status=False)
        # false_id = [history.question.id for history in histories][:5]

        # recommendations = []
        # for id in tqdm(false_id, total=len(false_id)):
        #     recommendation = settings.MODEL.get_recommendations(id)
        #     recommendations += recommendation

        print('Getting from DB')
        questions = list(Question.objects.filter(
            modules__subject=subject, user__user_id=user_id))
        print('Sampling')
        recommendations = random.sample(questions, 100)

        questions_ret = []
        print('Getting Recommendation')
        for recommendation in recommendations:
            options = []
            if not pd.isnull(recommendation.option_1):
                options.append(recommendation.option_1)
            if not pd.isnull(recommendation.option_2):
                options.append(recommendation.option_2)
            if not pd.isnull(recommendation.option_3):
                options.append(recommendation.option_3)
            if not pd.isnull(recommendation.option_4):
                options.append(recommendation.option_4)

            questions_ret.append({
                'id': recommendation.id,
                'questions': recommendation.questionOnly,
                'options': options,
                'correct_answer': recommendation.answer
            })

        return JsonResponse({
            'status': True,
            'message': '200',
            'questions': questions_ret
        })


class CompetencyView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']

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
        for subject in tqdm(subjects, total=len(subjects)):
            for chapter in Constant.subject_chapters[subject]:
                counter_dict[subject][chapter] = 0
                correct_dict[subject][chapter] = 0

        histories = AssignmentHistory.objects.filter(user__id=user_id)

        for history in tqdm(histories, total=len(histories)):
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
        for subject in tqdm(subjects, total=len(subjects)):
            for chapter in Constant.subject_chapters[subject]:
                if counter_dict[subject][chapter] == 0:
                    continue
                score = correct_dict[subject][chapter] / \
                    counter_dict[subject][chapter]
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
