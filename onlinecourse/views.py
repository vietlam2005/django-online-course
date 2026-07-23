from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Enrollment, Question, Choice, Submission

def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    
    selected_ids = []
    for key, value in request.POST.items():
        if key.startswith('choice_'):
            selected_ids.append(int(value))
            
    for choice_id in selected_ids:
        choice = Choice.objects.get(pk=choice_id)
        submission.choices.add(choice)
        
    return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=([course.id, submission.id])))

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    score = 0
    questions = course.question_set.all()
    selected_choices = submission.choices.all()
    
    for question in questions:
        selected_ids = selected_choices.filter(question=question).values_list('id', flat=True)
        score += question.calculate_score(selected_ids)
        
    return render(request, 'onlinecourse/exam_result_bootstrap.html', {'course': course, 'grade': score, 'submission': submission})
