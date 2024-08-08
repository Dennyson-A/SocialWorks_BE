from django.urls import path
from .views import AdminSignUPAPIView, EventAttendanceAPIView, FacultySignUpAPIView, SignInAPIView, YearAPIView, ClubAPIView, EventAPIView, StudentSignUpAPIView, BatchAPIView, UploadStudentsAPIView, MarkAttendanceAPIView, StudentListAPIView, AnnouncementsAPIView
from .views import AdminAnnouncementsListAPIView, ViewAttendanceAPIView, StudentDataAPIView, StudentSignInAPIView
urlpatterns = [
    path('login/', SignInAPIView.as_view(), name='userlogin'),
    path('admin/signup/', AdminSignUPAPIView.as_view(), name='adminsignup'),
    path('faculty/signup/', FacultySignUpAPIView.as_view(), name='facultysignup'),   
    path('student/signup/', StudentSignUpAPIView.as_view(), name='studentsignup'),
    path('student/signin/', StudentSignInAPIView.as_view(), name='studentsignin'),
    path('yeardata/', YearAPIView.as_view(), name='year'), 
    path('club/', ClubAPIView.as_view(), name='club'),
    path('event/', EventAPIView.as_view(), name='event'),
    path('batch/', BatchAPIView.as_view(), name='batch'),
    path('uploadfile/', UploadStudentsAPIView.as_view(), name='upload'),
    path('studentlist/', StudentListAPIView.as_view(), name='studentlist'),
    path('markattendance/', MarkAttendanceAPIView.as_view(), name='markattendance'),
    path('eventattendance/', EventAttendanceAPIView.as_view(), name='eventattendance'),
    path('announcements/', AnnouncementsAPIView.as_view(), name='announcements'),
    path('adminannouncements/', AdminAnnouncementsListAPIView.as_view(), name='adminannouncements'),
    path('viewattendance/', ViewAttendanceAPIView.as_view(), name='viewattendance'),
    path('studentdata/', StudentDataAPIView.as_view(), name='studentdata'),
]