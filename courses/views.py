# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404,redirect
from .models import Course,Discussion,UserProgress,Lesson,Quiz,Question,QuizResult
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from .forms import ContactForm,QuizForm,QuestionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/courses.html', {'courses': courses,})
@login_required
def course_detail(request, course_id, lesson_id=None):  # Ensure this function exists
    course = get_object_or_404(Course, id=course_id)
    lessons=course.lessons.all()
    enrolled = False
    if request.user.is_authenticated:
        enrolled = UserProgress.objects.filter(user=request.user, course=course).exists()
    current_lesson = get_object_or_404(Lesson, id=lesson_id, course=course) if lesson_id else lessons.first()
    prev_lesson = lessons.filter(id__lt=current_lesson.id).last()
    next_lesson = lessons.filter(id__gt=current_lesson.id).first()
    # progress=None
    # if request.user.is_authenticated:
    progress, _ = UserProgress.objects.get_or_create(user=request.user, course=course)
    completed_count = progress.completed_lessons.count()
    total_count = lessons.count()
    if total_count > 0:
        progress_percent = int((completed_count / total_count) * 100)
    else:
        progress_percent = 0
    return render(request, "courses/course_detail.html", {
        "course": course,
        'lessons':lessons,
        'enrolled':enrolled,
        'current_lesson':current_lesson,
        "next_lesson":next_lesson,
    'prev_lesson':prev_lesson,
        'user_progress': progress,
        'progress_percent': progress_percent,
    })

def profile_view(request):
    user = request.user
    enrolled_courses = Course.objects.filter(enrollment__user=user)  # Adjust if using custom Enrollment model
    progress_data = []

    for course in enrolled_courses:
        lessons = course.lessons.all()
        quizzes = Quiz.objects.filter(course=course)
        progress, created = UserProgress.objects.get_or_create(user=user, course=course)

        total_items = lessons.count() + quizzes.count()
        completed_items = progress.completed_lessons.count() + progress.completed_quizzes.count()

        if total_items > 0:
            percent = int((completed_items / total_items) * 100)
        else:
            percent = 0

        progress_data.append({
            'course': course,
            'progress': percent
        })

    return render(request, 'users/profile.html', {
        'enrolled_courses': enrolled_courses,
        'progress_data': progress_data,
    })


@login_required
def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, created = UserProgress.objects.get_or_create(user=request.user, course=lesson.course)
    progress.completed_lessons.add(lesson)
    return redirect('course_detail', lesson.course.id)
@login_required
def mark_lesson_complete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.course
    progress, created = UserProgress.objects.get_or_create(user=request.user, course=course)
    if request.method == "POST":
        progress.completed_lessons.add(lesson)
        return redirect('course_detail', course.id)

def course_discussion(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    discussions = Discussion.objects.filter(course=course)
    return render(request, "courses/discussion.html", {"course": course, "discussions": discussions})


def generate_certificate(request, course_id):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="certificate.pdf"'
    
    p = canvas.Canvas(response)
    p.drawString(100, 750, "Certificate of Completion")
    p.drawString(100, 730, f"Congratulations, {request.user.username}!")
    p.drawString(100, 710, f"You have completed the course!")
    p.showPage()
    p.save()

    return response
@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    # questions = quiz.questions.all()
    questions=Question.objects.filter(quiz=quiz)
    # Deserialize options field from string to list
    for question in questions:
        question.options = json.loads(question.options)
    score=None
    total=questions.count()
    user_answers={}
    if request.method == 'POST':
        score = 0
        for question in questions:
            selected = request.POST.get(f'question_{question.id}')
            user_answers[question.id]=selected
            if selected == question.correct_answer:
                score += 1
    return render(request, 'courses/take_quiz.html', {
        'quiz': quiz,'questions': questions,'score':score,'total':total,'user_answers':user_answers,})

def create_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save()
            return redirect('add_questions', quiz_id=quiz.id)
    else:
        quiz_form = QuizForm()
    return render(request, 'courses/create_quiz.html', {'form': quiz_form})

def add_questions(request, quiz_id):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = QuestionForm(initial={'quiz': quiz_id})
    return render(request, 'courses/add_question.html', {'form': form})

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    # Check if already enrolled
    progress, created = UserProgress.objects.get_or_create(user=user, course=course)

    if created:
        # User newly enrolled
        messages.success(request, f"You have successfully enrolled in {course.title}!")
    else:
        # User was already enrolled
        messages.info(request, f"You are already enrolled in {course.title}.")

    return redirect('course_detail', course_id=course.id)

# def contact_page(request):
#     form = ContactForm()
#     success_message = ""

#     if request.method == "POST":
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             message = form.cleaned_data['message']
            
#             send_mail(
#                 subject=f"Contact Form Submission from {name}",
#                 message=message,
#                 from_email=email,
#                 recipient_list=['your_email@example.com'],  # Change to your email
#         )

#             success_message = "Your message has been sent successfully!"
#             form = ContactForm()  # Reset the form after submission

#     return render(request, 'contact.html', {'form': form, 'success_message': success_message})



def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        full_message = f"Name: {name}\nEmail: {email}\n\n{message}"

        # Send email (configure EMAIL settings in settings.py)
        send_mail(subject, full_message, email, ['admin@example.com'])

        messages.success(request, 'Your message has been sent successfully!')
    
    return render(request, 'contact.html')






