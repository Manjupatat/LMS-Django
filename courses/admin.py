from django.contrib import admin
from .models import *
# Register your models here.


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Number of blank questions to show

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    inlines = [QuestionInline]


admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Quiz,QuizAdmin)
admin.site.register(Question)
admin.site.register(QuizResult)

