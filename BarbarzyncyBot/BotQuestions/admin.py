from django.contrib import admin
from .models import RequirementType, AnswerType, Question

@admin.register(RequirementType)
class RequirementTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name', 'enabled')

@admin.register(AnswerType)
class AnswerTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'requirement_type', 'question_text', 'answer_type', 'enabled')
    list_filter = ('requirement_type', 'answer_type', 'enabled')
    search_fields = ('question_text',)
