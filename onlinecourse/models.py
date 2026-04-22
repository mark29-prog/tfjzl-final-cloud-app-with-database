from django.db import models
from django.conf import settings
from django.utils.timezone import now


# Instructor
class Instructor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


# Learner
class Learner(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'

    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin'),
    ]

    occupation = models.CharField(max_length=20, choices=OCCUPATION_CHOICES, default=STUDENT)
    social_link = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.occupation})"


# Course
class Course(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='course_images/', blank=True)
    description = models.TextField()
    pub_date = models.DateField(null=True, blank=True)
    instructors = models.ManyToManyField(Instructor)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')
    total_enrollment = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# Lesson
class Lesson(models.Model):
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.title


# Enrollment
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'beta'

    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'Beta'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=10, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)

    def __str__(self):
        return f"{self.user} - {self.course}"


# Question
class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    grade = models.IntegerField(default=50)

    def __str__(self):
        return self.content

    def is_get_score(self, selected_ids):
        correct = self.choices.filter(is_correct=True).count()
        selected_correct = self.choices.filter(
            is_correct=True,
            id__in=selected_ids
        ).count()
        return correct == selected_correct


# Choice
class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


# Submission
class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='submissions')
    choices = models.ManyToManyField(Choice, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.enrollment.user} submission"