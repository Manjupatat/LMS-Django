# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404,redirect
from .models import Course,Discussion,UserProgress,Lesson
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from .forms import ContactForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/courses.html', {'courses': courses})

def course_detail(request, course_id, lesson_id=None):  # Ensure this function exists
    course = get_object_or_404(Course, id=course_id)
    lessons=course.lessons.all()
    enrolled = False
    if request.user.is_authenticated:
        enrolled = UserProgress.objects.filter(user=request.user, course=course).exists()
    current_lesson = get_object_or_404(Lesson, id=lesson_id) if lesson_id else lessons.first()
    prev_lesson = lessons.filter(id__lt=current_lesson.id).last()
    next_lesson = lessons.filter(id__gt=current_lesson.id).first()
    return render(request, "courses/course_detail.html", {
        "course": course,
        'lessons':lessons,
        'enrolled':enrolled,
        'current_lesson':current_lesson,
        "next_lesson":next_lesson,
    'prev_lesson':prev_lesson,
    })

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






