from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView

from .models import Course, Enrollment, Submission, Choice, Question


# =========================
# COURSE LIST (HOME PAGE)
# =========================
class CourseListView(ListView):
    model = Course
    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'


# =========================
# COURSE DETAIL PAGE
# =========================
class CourseDetailView(DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail.html'
    context_object_name = 'course'


# =========================
# REGISTRATION
# =========================
def registration_request(request):
    return render(request, 'onlinecourse/registration.html')


# =========================
# LOGIN
# =========================
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')

    return render(request, 'onlinecourse/login.html')


# =========================
# LOGOUT
# =========================
def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


# =========================
# ENROLL IN COURSE
# =========================
@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )

    return redirect('onlinecourse:course_details', course.id)


# =========================
# SUBMIT EXAM
# =========================
@login_required
def submit(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    enrollment = get_object_or_404(
        Enrollment,
        user=request.user,
        course=course
    )

    submission = Submission.objects.create(enrollment=enrollment)

    # collect selected answers
    for key in request.POST:
        if key.startswith('choice_'):
            for choice_id in request.POST.getlist(key):
                choice = Choice.objects.get(id=choice_id)
                submission.choices.add(choice)

    submission.save()

    return redirect(
        'onlinecourse:show_exam_result',
        course_id=course.id,
        submission_id=submission.id
    )


# =========================
# EXAM RESULT / EVALUATION
# =========================
def show_exam_result(request, course_id, submission_id):

    course = get_object_or_404(Course, id=course_id)
    submission = get_object_or_404(Submission, id=submission_id)

    selected_choices = submission.choices.all()

    total_score = 0
    results = []

    for question in course.question_set.all():

        selected_ids = selected_choices.filter(
            question=question
        ).values_list('id', flat=True)

        is_correct = question.is_get_score(selected_ids)

        if is_correct:
            total_score += question.grade

        results.append({
            'question': question,
            'selected_ids': selected_ids,
            'is_correct': is_correct
        })

    max_score = sum(q.grade for q in course.question_set.all())
    passed = total_score >= (0.5 * max_score)

    return render(request, 'onlinecourse/exam_result.html', {
        'course': course,
        'submission': submission,
        'results': results,
        'total_score': total_score,
        'max_score': max_score,
        'passed': passed
    })