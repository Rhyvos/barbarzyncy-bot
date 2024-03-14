from django.db import models
from django.core.validators import MaxLengthValidator

class RequirementType(models.Model):
    type_name = models.CharField(max_length=90)
    enabled = models.BooleanField()

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name_plural = "Requirement Types"

class AnswerType(models.Model):
    type_name = models.CharField(max_length=255)

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name_plural = "Answer Types"

class Question(models.Model):
    requirement_type = models.ForeignKey(RequirementType, on_delete=models.CASCADE)
    question_text = models.TextField(validators=[MaxLengthValidator(256)])
    answer_type = models.ForeignKey(AnswerType, on_delete=models.CASCADE, default=lambda: AnswerType.objects.first())
    enabled = models.BooleanField()

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name_plural = "Questions"
