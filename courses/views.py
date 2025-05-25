# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404,redirect
from .models import Course,Discussion,UserProgress,Lesson,Quiz,Question,QuizResult, Enrollment
from django.http import HttpResponse,JsonResponse
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from .forms import ContactForm,QuizForm,QuestionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone
from xhtml2pdf import pisa
from django.template.loader import get_template
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io,qrcode, os
from django.conf import settings
from io import BytesIO
from django.templatetags.static import static
from datetime import datetime
from PIL import Image,ImageDraw,ImageFont
from courses.models import Course

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
    # quiz_for_lesson = None
    # if current_lesson:
    #     quiz_for_lesson = Quiz.objects.filter(course=course, title=current_lesson.title).first()
    quiz = Quiz.objects.filter(lesson=current_lesson).first()
    if request.GET.get("next") == "true" and quiz:
        return redirect('take_quiz', quiz_id=quiz.id)

    return render(request, "courses/course_detail.html", {
        "course": course,
        'lessons':lessons,
        'enrolled':enrolled,
        'current_lesson':current_lesson,
        "next_lesson":next_lesson,
    'prev_lesson':prev_lesson,
        'user_progress': progress,
        'progress_percent': progress_percent,
        # 'quiz_for_lesson': quiz_for_lesson,
    })


def course_overview(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    return render(request, 'courses/course_overview.html', {
        'course': course,
        'lessons': lessons,
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
    # response = HttpResponse(content_type="application/pdf")
    # response["Content-Disposition"] = 'attachment; filename="certificate.pdf"'
    #
    # p = canvas.Canvas(response)
    # p.drawString(100, 750, "Certificate of Completion")
    # p.drawString(100, 730, f"Congratulations, {request.user.username}!")
    # p.drawString(100, 710, f"You have completed the course!")
    # p.showPage()
    # p.save()
    #
    # return response

    # name = "John Doe"
    # date = "May 11, 2025"
    #
    # # Create HTTP response with PDF headers
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = f'attachment; filename="{name}_certificate.pdf"'
    #
    # # Create canvas
    # p = canvas.Canvas(response, pagesize=landscape(A4))
    # width, height = landscape(A4)
    #
    # # Load background image from static files
    # image_path = os.path.join('static/images/background.png')
    # image = ImageReader(image_path)
    # p.drawImage(image, 0, 0, width=width, height=height)
    #
    # # Add recipient name
    # p.setFont("Helvetica-Bold", 28)
    # p.setFillColorRGB(0.12, 0.16, 0.34)  # dark navy color
    # p.drawCentredString(width / 2, height / 2 + 30, name)
    #
    # # Add date
    # p.setFont("Helvetica", 14)
    # p.setFillColorRGB(0, 0, 0)
    # p.drawString(100, 100, f"Date: {date}")

    # Add signature (text placeholder)
    # p.drawString(width - 200, 100, "Signature")

    # Finalize
    # p.showPage()
    # p.save()
    # return response

    user = request.user
    name = user.get_full_name() or user.username
    date = datetime.now().strftime("%B %d, %Y")

    course = Course.objects.get(id=course_id)  # Optional, for course title

    context = {
        'name': name,
        'date': date,
        'course_title': course.title if course else "Course Title"
    }
    return render(request, 'courses/certificate.html', context)


@login_required
def certificate_view(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.user in course.students.all():  # Assuming enrolled users are in `course.students`
        context = {
                'user': request.user,
                'course': course,
                'date': timezone.now().date()
            }

        return render(request, 'courses/certificate.html', context)
    else:
        return redirect('course_detail',course_id=course_id)

@login_required
# def download_certificate_pdf(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     if request.user in course.students.all():
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename=certificate_{request.user.username}.pdf'
#
#         buffer = io.BytesIO()
#         page_size = landscape(A4)
#         p = canvas.Canvas(buffer, pagesize=page_size)
#         width, height = page_size
#
#         # === Background and Border ===
#         margin = 40
#         p.setStrokeColor(colors.HexColor("#004080"))
#         p.setLineWidth(6)
#         p.rect(margin, margin, width - 2 * margin, height - 2 * margin)
#
#         inner_margin = 50
#         p.setStrokeColor(colors.lightgrey)
#         p.setLineWidth(1)
#         p.rect(inner_margin, inner_margin, width - 2 * inner_margin, height - 2 * inner_margin)
#
#         logo_path = os.path.join(settings.BASE_DIR, 'static/images/logo.png')
#         if os.path.exists(logo_path):
#             p.drawImage(logo_path, x=40, y=height - 120, width=100, height=60, mask='auto')
#
#         p.setFont("Helvetica-Bold", 26)
#         p.drawCentredString(width / 2, height - 100, "Certificate of Completion")
#
#         p.setFont("Helvetica", 18)
#         p.drawCentredString(width / 2, height - 180, "This certifies that")
#
#         p.setFont("Helvetica-Bold", 22)
#         p.drawCentredString(width / 2, height - 220, request.user.get_full_name() or request.user.username)
#
#         p.setFont("Helvetica", 18)
#         p.drawCentredString(width / 2, height - 260, "has successfully completed the course")
#
#         p.setFont("Helvetica-Bold", 20)
#         p.drawCentredString(width / 2, height - 300, f"\"{course.title}\"")
#
#         p.setFont("Helvetica", 14)
#         p.drawCentredString(width / 2, height - 350, f"Date: {timezone.now().strftime('%B %d, %Y')}")
#
#         p.showPage()
#         p.save()
#         pdf = buffer.getvalue()
#         buffer.close()
#         response.write(pdf)
#         return response
#
#     return redirect('course_detail', course_id=course_id)

def download_certificate_pdf(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user in course.students.all():
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=certificate_{request.user.username}.pdf'

        buffer = io.BytesIO()
        page_size = landscape(A4)
        p = canvas.Canvas(buffer, pagesize=page_size)
        width, height = page_size

        # === Background and Border ===
        margin = 40
        p.setStrokeColor(colors.HexColor("#004080"))
        p.setLineWidth(6)
        p.rect(margin, margin, width - 2*margin, height - 2*margin)

        inner_margin = 50
        p.setStrokeColor(colors.lightgrey)
        p.setLineWidth(1)
        p.rect(inner_margin, inner_margin, width - 2*inner_margin, height - 2*inner_margin)

        # === Logo ===
        # logo_path = os.path.join(settings.BASE_DIR, 'static/images/logo.png')
        # if os.path.exists(logo_path):
        #     logo_width = 120
        #     logo_height = 60
        #     logo_x = (width - logo_width) / 2
        #     logo_y = height - 60 - 10
        #     p.drawImage(logo_path, x=logo_x, y=logo_y, width=logo_width, height=logo_height, mask='auto')
        #
        #     content_start_y=logo_y-30

        # else:
        content_start_y=height-100

        # === Title ===
        p.setFillColor(colors.HexColor("#003366"))
        p.setFont("Helvetica-Bold", 40)
        p.drawCentredString(width / 2, content_start_y, "Certificate of Completion")

        # === Subtitle ===
        p.setFillColor(colors.black)
        p.setFont("Helvetica-Oblique", 22)
        p.drawCentredString(width / 2, content_start_y - 50, "This certificate is proudly presented to")

        # === User Name ===
        user_name = request.user.get_full_name() or request.user.username
        p.setFont("Helvetica-Bold", 32)
        p.setFillColor(colors.HexColor("#004080"))
        p.drawCentredString(width / 2, content_start_y - 100, user_name)

        # === Course info ===
        p.setFont("Helvetica", 20)
        p.drawCentredString(width / 2, content_start_y - 150, "for successfully completing the course")

        p.setFont("Helvetica-BoldOblique", 26)
        p.setFillColor(colors.darkblue)
        p.drawCentredString(width / 2, content_start_y - 200, f"\"{course.title}\"")

        # === Date ===
        p.setFont("Helvetica-Oblique", 16)
        p.setFillColor(colors.black)
        p.drawCentredString(width / 2, content_start_y - 240, f"Issued on: {timezone.now().strftime('%B %d, %Y')}")

        # === Signature placeholders ===
        # p.setLineWidth(1)
        # p.line(width / 4 - 60, height - 420, width / 4 + 60, height - 420)
        # p.line(3 * width / 4 - 60, height - 420, 3 * width / 4 + 60, height - 420)

        # p.setFont("Helvetica", 14)
        # p.drawCentredString(width / 4, height - 440, "Instructor Signature")
        # p.drawCentredString(3 * width / 4, height - 440, "Coordinator Signature")

        # === Finalize ===
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    return redirect('course_detail', course_id=course_id)

# def download_certificate_pdf(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     if request.user in course.students.all():
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename=certificate_{request.user.username}.pdf'
#
#         buffer = io.BytesIO()
#         p = canvas.Canvas(buffer, pagesize=landscape(A4))
#         width, height = landscape(A4)
#
#         # Border
#         p.setStrokeColor(colors.HexColor("#000080"))
#         p.setLineWidth(4)
#         p.rect(20, 20, width - 40, height - 40)
#
#         # Header logos
#         left_logo = os.path.join(settings.BASE_DIR, 'static/images/left_logo.png')
#         main_logo = os.path.join(settings.BASE_DIR, 'static/images/technologics_logo.png')
#         seal_logo = os.path.join(settings.BASE_DIR, 'static/images/seal.png')
#
#         if os.path.exists(left_logo):
#             p.drawImage(left_logo, 40, height - 130, width=80, height=80, mask='auto')
#         if os.path.exists(main_logo):
#             p.drawImage(main_logo, width/2 - 60, height - 120, width=120, height=60, mask='auto')
#
#         # Title
#         p.setFont("Helvetica-Bold", 28)
#         p.drawCentredString(width / 2, height - 160, "Internship Certificate")
#
#         # Subtitle
#         p.setFont("Helvetica-Oblique", 14)
#         p.drawCentredString(width / 2, height - 190, "This certificate is proudly presented to")
#
#         # Recipient name
#         user_name = request.user.get_full_name() or request.user.username
#         p.setFont("Helvetica-Bold", 24)
#         p.drawCentredString(width / 2, height - 220, user_name)
#
#         # Body content
#         p.setFont("Helvetica", 16)
#         p.drawCentredString(width / 2, height - 260, f"for successful completion of Internship in")
#         p.setFont("Helvetica-Bold", 18)
#         p.drawCentredString(width / 2, height - 290, course.title)
#
#         p.setFont("Helvetica", 16)
#         p.drawCentredString(width / 2, height - 320, "under the guidance of TECHNOLOGICS GLOBAL RESEARCH LAB")
#         p.drawCentredString(width / 2, height - 350, f"Conducted between 03-02-2025 to 12-05-2025")
#         p.drawCentredString(width / 2, height - 380, "for the student of NIE Institute of Technology, Mysore")
#
#         # Seal
#         if os.path.exists(seal_logo):
#             p.drawImage(seal_logo, width - 200, 50, width=120, height=120, mask='auto')
#
#         # Signature line
#         p.line(width - 250, 70, width - 100, 70)
#         p.setFont("Helvetica", 10)
#         p.drawCentredString(width - 175, 55, "Signature of Authority")
#
#         # Footer
#         p.setFont("Helvetica-Oblique", 8)
#         p.drawCentredString(width / 2, 30, "Technologics Global, 10th Main Road, Jayanagar, Bengaluru - www.technologicsglobal.com")
#
#         p.showPage()
#         p.save()
#         pdf = buffer.getvalue()
#         buffer.close()
#         response.write(pdf)
#         return response
#
#     return redirect('course_detail', course_id=course_id)



# @login_required
# def download_certificate_pdf(request, course_id):
#     course = Course.objects.get(id=course_id)
#     user = request.user
#     date = timezone.now().strftime('%d %B, %Y')
#
#     # Setup PDF
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer, pagesize=A5)
#     width, height = A5
#
#     # Background and border (optional)
#     p.setStrokeColorRGB(0.2, 0.5, 0.3)
#     p.setLineWidth(4)
#     p.rect(30, 30, width - 60, height - 60)
#
#     # Logo (top center)
#     logo_path = 'media/logo.png'  # Adjust path as needed
#     p.drawImage(logo_path, width/2 - 80, height - 120, width=160, preserveAspectRatio=True)
#
#     # Title
#     p.setFont("Helvetica-Bold", 26)
#     p.drawCentredString(width / 2, height - 160, "Certificate of Completion")
#
#     # Recipient
#     p.setFont("Helvetica", 16)
#     p.drawCentredString(width / 2, height - 200, "This is to certify that")
#     p.setFont("Helvetica-Bold", 20)
#     p.drawCentredString(width / 2, height - 230, f"{user.get_full_name() or user.username}")
#
#     # Course Name
#     p.setFont("Helvetica", 16)
#     p.drawCentredString(width / 2, height - 270, "has successfully completed the course")
#     p.setFont("Helvetica-Bold", 18)
#     p.drawCentredString(width / 2, height - 300, f"{course.title}")
#
#     # Date
#     p.setFont("Helvetica", 14)
#     p.drawCentredString(width / 2, height - 340, f"Date: {date}")
#
#     # Footer or signature (optional)
#     p.setFont("Helvetica-Oblique", 12)
#     p.drawString(40, 40, "E-learning Platform - EduVerse")
#
#     p.showPage()
#     p.save()
#
#     buffer.seek(0)
#     return HttpResponse(buffer, content_type='application/pdf')

@login_required
def generate_certificate_image(request, course_id):
    user = request.user
    name = user.get_full_name() or user.username
    date = datetime.now().strftime("%B %d, %Y")
    #
    # # ✅ Fetch course title
    course = get_object_or_404(Course, id=course_id)
    course_title = course.title
    #
    # # Load certificate background
    bg_path = os.path.join("static/images/Certificate_Template.png")
    cert = Image.open(bg_path).convert("RGB")
    width, height = cert.size
    draw = ImageDraw.Draw(cert)
    width, height = cert.size
    #
    # # ✅ Load logo image and resize
    logo_path = os.path.join("static/images/logo.png")
    logo = Image.open(logo_path).convert("RGBA")
    logo_width = 80
    logo.thumbnail((logo_width, logo_width), Image.LANCZOS)
    #
    # # Paste logo (top center)
    # logo_x = (width - logo.width) // 2
    logo_y = 80
    cert.paste(logo, (logo_y, logo_y), logo)
    #
    # # Load fonts (adjust as needed)
    title_font = ImageFont.truetype("static/fonts/arialbd.ttf", 48)
    subtitle_font = ImageFont.truetype("static/fonts/arial.ttf", 32)
    name_font = ImageFont.truetype("static/fonts/arialbd.ttf", 44)
    course_font = ImageFont.truetype("static/fonts/ariali.ttf", 32)
    small_font = ImageFont.truetype("static/fonts/arial.ttf", 24)
    #
    # # Draw certificate text
    # text_start_y=logo_y + logo.height + 30
    # draw.text((width / 2, text_start_y), "Certificate of Completion", fill=(10, 10, 80), font=title_font, anchor="mm")
    # draw.text((width / 2, text_start_y + 70), "This certifies that", fill=(0, 0, 0), font=subtitle_font, anchor="mm")
    # draw.text((width / 2, text_start_y + 130), name, fill=(20, 20, 20), font=name_font, anchor="mm")
    # draw.text((width / 2, text_start_y + 190), "has successfully completed the course:", fill=(0, 0, 0),
    #           font=subtitle_font, anchor="mm")
    # draw.text((width / 2, text_start_y + 250), course_title, fill=(0, 0, 150), font=course_font, anchor="mm")
    #
    # draw.text((80, height - 70), f"Date: {date}", fill=(0, 0, 0), font=small_font)
    # draw.line([(width - 300, height - 100), (width - 100, height - 100)], fill=(0, 0, 0), width=2)
    # draw.text((width - 200, height - 70), "Authorized Signature", fill=(0, 0, 0), font=small_font, anchor="mm")
    #
    # # Save to buffer
    # buffer = BytesIO()
    # cert.save(buffer, format="JPEG")
    # buffer.seek(0)
    #
    # # Return response
    # response = HttpResponse(buffer, content_type="image/jpeg")
    # response["Content-Disposition"] = f'attachment; filename="{name}_certificate.jpg"'
    # return response



    # Load fonts
    # font_path = os.path.join(settings.BASE_DIR, 'static/fonts/Roboto-Bold.ttf')
    # font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    # title_font = ImageFont.truetype(font_path, 60)
    # subtitle_font = ImageFont.truetype(font_path, 40)
    # name_font = ImageFont.truetype(font_path, 55)
    # small_font = ImageFont.truetype(font_path, 30)

    # Add logo (optional)

    # Write Text
    center_x = width // 2
    y = 300
    draw.text((center_x, y), "Certificate of Completion", fill="black", font=title_font, anchor="mm")
    y += 100
    draw.text((center_x, y), "This certifies that", fill="black", font=subtitle_font, anchor="mm")
    y += 80
    draw.text((center_x, y), name, fill="black", font=name_font, anchor="mm")
    y += 80
    draw.text((center_x, y), "has successfully completed the course:", fill="black", font=subtitle_font, anchor="mm")
    y += 70
    draw.text((center_x, y), course_title, fill="navy", font=subtitle_font, anchor="mm")

    # Date and signature
    draw.text((80, height - 100), f"Date: {date}", fill="black", font=small_font)
    draw.text((width - 300, height - 100), "Authorized Signature", fill="black", font=small_font)

    # Return response
    response = HttpResponse(content_type='image/jpeg')
    cert.convert('RGB').save(response, 'JPEG')
    response['Content-Disposition'] = 'attachment; filename=certificate.jpg'
    return response


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    course=quiz.course
    # questions = quiz.questions.all()
    questions=Question.objects.filter(quiz=quiz)
    # Deserialize options field from string to list
    for question in questions:
        if isinstance(question.options, str):
            question.options = json.loads(question.options)
    score=None
    percent=0
    passed=False
    total=questions.count()
    user_answers={}
    if request.method == 'POST':
        score = 0
        for question in questions:
            selected = request.POST.get(f'question_{question.id}')
            user_answers[question.id]=selected
            if selected == question.correct_answer:
                score += 1

        total = questions.count()
        percent = int((score / total) * 100) if total > 0 else 0
        passed = percent >= 80

        return render(request, 'courses/take_quiz.html', {
                'quiz': quiz,
            'questions': questions,
            'score':score,
            'total':total,
            'user_answers':user_answers,
            'passed':passed,
            'percent':percent,
            'course_id':quiz.course.id,
        'cpurse':course,})
    # return redirect('course_detail_lesson', course_id=quiz.course.id, lesson_id=quiz.lesson.id + 1)

@login_required
def assessment_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    quiz = Quiz.objects.filter(course=course).first()  # assumes one quiz per course
    questions=Question.objects.filter(quiz=quiz)
    score = None
    percent = 0
    passed = False
    total = questions.count()
    user_answers = {}
    if request.method == "POST":
        correct = 0
        for q in questions:
            if isinstance(q.options, str):
                q.options=json.loads(q.options)
            selected = request.POST.get(f"question_{q.id}")
            user_answers[q.id] = selected
            if selected == q.correct_answer:
                correct += 1

        score = correct
        percent = int((score / total) * 100)
        passed = percent >= 80

        # Save result
        QuizResult.objects.create(user=request.user, quiz=quiz, score=score)

    return render(request, "courses/assessment.html", {
        "course": course,
        "quiz": quiz,
        "questions": questions,
        "user_answers": user_answers,
        "score": score,
        "percent": percent,
        "passed": passed
    })
    # if not quiz:
    #     messages.warning(request, "No quiz available for this course.")
    #     return redirect('course_detail', course_id=course.id)
    #
    # return redirect('take_quiz', quiz_id=quiz.id)

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






