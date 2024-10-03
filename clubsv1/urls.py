from django.urls import path
from .views import ( AdminSignUPAPIView, EventAttendanceAPIView, FacultySignUpAPIView, SignInAPIView, YearAPIView, 
                    ClubAPIView, EventAPIView, StudentSignUpAPIView, BatchAPIView, UploadStudentsAPIView, MarkAttendanceAPIView, StudentListAPIView, AnnouncementsAPIView,
                    AdminAnnouncementsListAPIView, ViewAttendanceAPIView, StudentDataAPIView, StudentSignInAPIView, FacultyListAPIView, 
                    EventTypeCountAPIView, BloodGroupListAPIView, DepartmentListAPIView, EventStudentsListAPIView, UpcomingAnnouncementsAPIView,
                    UpcomingEventsAPIView, EventClubListAPIView, StudentOTPAPIView, StudentOTPVerifyAPIView, QuotaCreateAPIView, QuotaAPIView )

urlpatterns = [
    path('login/', SignInAPIView.as_view(), name='userlogin'),
    path('admin/signup/', AdminSignUPAPIView.as_view(), name='adminsignup'),
    path('faculty/signup/', FacultySignUpAPIView.as_view(), name='facultysignup'),   
    path('otp/', StudentOTPAPIView.as_view(), name='otp'),
    path('otpverify/', StudentOTPVerifyAPIView.as_view(), name='otpverify'),
    path('student/signup/', StudentSignUpAPIView.as_view(), name='studentsignup'),
    path('student/signin/', StudentSignInAPIView.as_view(), name='studentsignin'),
    path('batch/', BatchAPIView.as_view(), name='batch'),       
    path('departments/', DepartmentListAPIView.as_view(), name='departments'),
    path('get-quota/', QuotaAPIView.as_view(), name='quotasubmit'), 

    path('uploadfile/', UploadStudentsAPIView.as_view(), name='upload'), ##admin
    path('eventattendance/', EventAttendanceAPIView.as_view(), name='eventattendance'), ## admin
    path('adminannouncements/', AdminAnnouncementsListAPIView.as_view(), name='adminannouncements'), ##admin
    path('facultylist/', FacultyListAPIView.as_view(), name='facultylist'), ##admin

    path('event/', EventAPIView.as_view(), name='event'),       ## faculty
    path('studentlist/', StudentListAPIView.as_view(), name='studentlist'),  ##faculty
    path('markattendance/', MarkAttendanceAPIView.as_view(), name='markattendance'), ## faculty
    path('announcements/', AnnouncementsAPIView.as_view(), name='announcements'),  ## faculty
    path('eventtypes/', EventTypeCountAPIView.as_view(), name='eventtypes'), ## faculty
    path('eventclubs/', EventClubListAPIView.as_view(), name='eventclubs'), ##faculty
    path('bloodgroups/', BloodGroupListAPIView.as_view(), name='bloodgroups'), ##faculty
    path('eventstudents/', EventStudentsListAPIView.as_view(), name='eventstudents'),  ##faculty
    path('quota/', QuotaCreateAPIView.as_view(), name='quota'), ##faculty
    
    path('yeardata/', YearAPIView.as_view(), name='year'),      ##admin, faculty
    path('club/', ClubAPIView.as_view(), name='club'),          ##admin, faculty

    path('viewattendance/', ViewAttendanceAPIView.as_view(), name='viewattendance'), ##student
    path('studentdata/', StudentDataAPIView.as_view(), name='studentdata'), ##student
    path('upcomingannouncements/', UpcomingAnnouncementsAPIView.as_view(), name='upcomingannouncements'),  ##students
    path('upcomingevents/', UpcomingEventsAPIView.as_view(), name='upcomingevents'), ##students
]