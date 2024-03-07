from django import forms
from .models import Question, RequirementType, AnswerType

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        widgets = {
            'question_text': forms.Textarea(attrs={'class': 'form-control autosize', 'rows': 1}),
            'requirement_type': forms.Select(attrs={'class': 'form-select'}),
            'answer_type': forms.Select(attrs={'class': 'form-select'}),
            'enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            "question_text": "Question Text",
            "requirement_type": "Requirement Type",
            "answer_type": "Answer Type",
            "enabled": "Enabled",
        }

class RequirementTypeForm(forms.ModelForm):
    class Meta:
        model = RequirementType
        fields = '__all__'
        widgets = {
            'type_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            "type_name": "Requirement Type",
        }

class AnswerTypeForm(forms.ModelForm):
    class Meta:
        model = AnswerType
        fields = '__all__'
        widgets = {
            'type_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            "type_name": "Answer Type",
        }
