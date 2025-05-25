from http.cookiejar import debug

from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('/overview', course_overview, name='overview'),
    path('contact/',contact,name="contact"),
    path('', course_list, name='courses'),
    path('course/<int:course_id>/overview/', views.course_overview, name='course_overview'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/lesson/<int:lesson_id>/', views.course_detail, name='course_detail_lesson'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),  # <-- Add this
    path('<int:course_id>/discussion/', views.course_discussion, name='course_discussion'),
    path('lesson/<int:lesson_id>/complete/', views.mark_lesson_complete, name='mark_lesson_complete'),
    path('quiz/<int:quiz_id>/',views.take_quiz,name='take_quiz'),
    path('create-quiz/', views.create_quiz, name='create_quiz'),
    path('add-question/<int:quiz_id>/', views.add_questions, name='add_questions'),
    path('<int:course_id>/certificate/', views.certificate_view, name='get_certificate'),
    path('<int:course_id>/download-certificate/',download_certificate_pdf,name="download_certificate"),
    # path('<int:course_id>/download/',generate_certificate,name="certificate"),
    # path('<int:course_id>/certificate/',views.generate_certificate_image,name="image"),
path('<int:course_id>/assessment/', views.assessment_view, name='course_assessment'),


]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
