# from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.timezone import now,datetime
import json
from django.core.exceptions import ValidationError


class Course(models.Model):
    title = models.CharField(max_length=255)
    id=models.AutoField(primary_key=True)
    description = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )

    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses_instructed'
        ,null=True,
    )

    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='enrolled_courses',
        null=True
    )

    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    created_at = models.DateTimeField( default=datetime.now)
    image = models.ImageField(upload_to="course_images/", null=True, blank=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    video_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title



class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=255)
    options = models.TextField()

    # def clean(self):
    #     try:
    #         options = json.loads(self.options)
    #         if not isinstance(options, list):
    #             raise ValidationError("Options must be a list.")
    #         if self.correct_answer not in options:
    #             raise ValidationError("Correct answer must be one of the options.")
    #     except json.JSONDecodeError:
    #         raise ValidationError("Options must be valid JSON.")

    def clean(self):
        if isinstance(self.options, list):
            # Convert list to JSON string before saving
            self.options = json.dumps(self.options)
        try:
            opts = json.loads(self.options)
            if not isinstance(opts, list):
                raise ValidationError("Options must be a list.")
            if self.correct_answer not in opts:
                raise ValidationError("Correct answer must be one of the options.")
        except json.JSONDecodeError:
            raise ValidationError("Options must be valid JSON.")

class QuizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()

class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_lessons = models.ManyToManyField(Lesson, blank=True)
    completed_quizzes = models.ManyToManyField(Quiz, blank=True)


class Discussion(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    enrolled_at=models.DateTimeField(auto_now_add=True)