from django.urls import path
from .views import QuestionView, RecommendationDetailView, CompetencyView

# Create your views here.
urlpatterns = [
    path('', QuestionView.as_view(), name='question'),
    path('competency/<str:id>/', CompetencyView.as_view(), name='competency_details'),
    path('recommender/<str:id>/<str:subject>', RecommendationDetailView.as_view(), name='recommendation_details'),
]
