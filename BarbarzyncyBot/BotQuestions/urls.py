from django.urls import path
from .views import question_list, answer_type_list, requirement_type_list

urlpatterns = [
    path('questions/', question_list, name='question-list'),
    path('answer-types/', answer_type_list, name='answer-type-list'),
    path('requirement-types/', requirement_type_list, name='requirement-type-list'),
]