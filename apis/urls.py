from django.urls import path
from .views import QuestionView

# Create your views here.
urlpatterns = [
    path('', QuestionView.as_view(), name='question'),
]
