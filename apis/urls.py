from django.urls import path
from .views import *

# Create your views here.
urlpatterns = [
    path('', QuestionView.as_view(), name='question'),
    path('module/list', ModuleView.as_view(), name='module'),
    path('module/<str:id>', ModuleDetailView.as_view(), name='module_detail'),
    path('competency/<str:id>/', CompetencyView.as_view(), name='competency_details'),
    path('recommender/<str:id>/<str:subject>', RecommendationDetailView.as_view(), name='recommendation_details'),
]
