from django.urls import path
from .views import *

# Create your views here.
urlpatterns = [
    path('', QuestionView.as_view(), name='question'),
    path('auth/', AuthView.as_view(), name='auth'),
    path('module/list', ModuleView.as_view(), name='module'),
    path('module/<str:id>', ModuleDetailView.as_view(), name='module_detail'),
    path('competency/<str:user_id>/', CompetencyView.as_view(),
         name='competency_details'),
    path('recommender/<str:user_id>/<str:subject>',
         RecommendationDetailView.as_view(), name='recommendation_details'),
]
