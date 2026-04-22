from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ['name', 'pub_date']


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['content', 'course', 'grade']


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct']


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'submitted_at']
    filter_horizontal = ['choices']


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Submission, SubmissionAdmin)