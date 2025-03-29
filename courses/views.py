# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from .models import Course,Discussion
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from .forms import ContactForm
from django.contrib import messages


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/courses.html', {'courses': courses})

def course_detail(request, course_id):  # Ensure this function exists
    course = get_object_or_404(Course, id=course_id)
    return render(request, "courses/course_detail.html", {"course": course})

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






