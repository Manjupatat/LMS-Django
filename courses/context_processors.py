from .models import Course
from django.db.models import Count

def popular_courses(request):
    courses = Course.objects.annotate(
        enrollments_count=Count('userprogress')
    ).order_by('-enrollments_count')[:4]  # Adjust logic as needed
    return {'popular_courses': courses}
