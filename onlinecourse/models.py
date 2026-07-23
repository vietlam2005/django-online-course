from django.db import models
from django.conf import settings
class Course(models.Model):
    name = models.CharField(max_length=30, default='online course')
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')

    def __str__(self):
        return self.name

class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=None)
    mode = models.CharField(max_length=100, default='audit')

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=50)

    def __str__(self):
        return self.question_text

    def calculate_score(self, selected_ids):
        total_score = 0
        all_choices = self.choice_set.filter(id__in=selected_ids)
        correct_choices = self.choice_set.filter(is_correct=True)
        if set(all_choices) == set(correct_choices):
            total_score = self.grade
        return total_score

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
