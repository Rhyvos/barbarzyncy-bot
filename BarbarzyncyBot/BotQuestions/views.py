from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .models import Question, RequirementType, AnswerType
from .forms import QuestionForm, RequirementTypeForm, AnswerTypeForm

def process_formset(request, formset, template_name, redirect_url):
    if request.method == 'POST':
        formset_instance = formset(request.POST)
        if formset_instance.is_valid():
            formset_instance.save()
            return redirect(redirect_url)
        else:
            error_message = "Formularz zawiera błędy. Sprawdź wprowadzone dane:"
            return render(request, template_name, {'formset': formset_instance, 'error_message': error_message})
    else:
        formset_instance = formset(queryset=formset.model.objects.all())
    return render(request, template_name, {'formset': formset_instance})

QuestionFormSet = modelformset_factory(Question, form=QuestionForm, can_delete=True, extra=1)
RequirementTypeFormSet = modelformset_factory(RequirementType, form=RequirementTypeForm, can_delete=True, extra=1)
AnswerTypeFormSet = modelformset_factory(AnswerType, form=AnswerTypeForm, can_delete=True, extra=1)

@login_required
def question_list(request):
    return process_formset(request, QuestionFormSet, 'question_list.html', 'question-list')

@login_required
def requirement_type_list(request):
    return process_formset(request, RequirementTypeFormSet, 'requirement_type_list.html', 'requirement-type-list')

@login_required
def answer_type_list(request):
    return process_formset(request, AnswerTypeFormSet, 'answer_type_list.html', 'answer-type-list')
