from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission


# -----------------------
# Inline classes
# -----------------------
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


# -----------------------
# Course Admin
# -----------------------
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ['name', 'pub_date']
    search_fields = ['name', 'description']


# -----------------------
# Question Admin
# -----------------------
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['content', 'course', 'grade']
    search_fields = ['content']
    list_filter = ['course']


# -----------------------
# Choice Admin
# -----------------------
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct']
    list_filter = ['question', 'is_correct']
    search_fields = ['text']


# -----------------------
# Submission Admin
# -----------------------
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'submitted_at']
    filter_horizontal = ['choices']
    list_filter = ['enrollment']


# -----------------------
# Register models (CLEAN)
# -----------------------
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Submission, SubmissionAdmin)