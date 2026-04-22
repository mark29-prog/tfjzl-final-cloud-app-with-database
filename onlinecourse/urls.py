from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # =========================
    # HOME PAGE
    # =========================
    path('', views.CourseListView.as_view(), name='index'),

    # =========================
    # AUTH
    # =========================
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),

    # =========================
    # COURSE DETAIL
    # =========================
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),

    # =========================
    # ENROLL
    # =========================
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),

    # =========================
    # SUBMIT EXAM
    # =========================
    path('<int:course_id>/submit/', views.submit, name='submit'),

    # =========================
    # EXAM RESULT (EVALUATION)
    # =========================
    path(
        'course/<int:course_id>/submission/<int:submission_id>/result/',
        views.show_exam_result,
        name='show_exam_result'
    ),
]

# =========================
# MEDIA FILES (images, uploads)
# =========================
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)