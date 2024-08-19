from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import pandas as pd

from .models import Faculty, YearData, Club, Event, Student, Batch, Announcements, OTP
from .serializers import FacultyUserSerializer, YearDataSerializer, ClubDataSerializer, EventDataSerializer, StudentUserSerializer, BatchDataSerializer, StudentListSerializer, MarkAttendanceSerializer, AnnouncementsDataSerializer, AnnouncementsSerializer, AdminAnnouncementsSerializer
from .serializers import StudentDataSerializer, FacultyViewSerializer, EventTypeSerializer, StudentBloodGroupSerializer, DepartmentStudentsSerializer, OTPSerializer, StudentOTPSerializer
from .methods import encrypt_password, faculty_encode_token, ob_encode_token, hoc_encode_token, validate_batch, student_encode_token, send_email, generate_otp
from .authentication import HOCTokenAuthentication
from .forms import UploadFileForm
import logging
from django.db.models import Count
from django.utils import timezone

logger = logging.getLogger(__name__)

#SIGN UP API / CREATE ADMIN USER API
class AdminSignUPAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FacultyUserSerializer(data=request.data)
        if serializer.is_valid() and serializer.validated_data.get('role') == 'HOC':
            raw_password = serializer.validated_data.get('password')
            encrypted_password = encrypt_password(raw_password)
            serializer.save(password=encrypted_password)
            return Response({'data': serializer.data, 'message': "Admin User created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#SIGN UP API / CREATE FACULTY USER API
class FacultySignUpAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        serializer = FacultyUserSerializer(data=request.data)
        
        if serializer.is_valid():
            raw_password = serializer.validated_data.get('password')
            encrypted_password = encrypt_password(raw_password)
            user = serializer.save(password=encrypted_password)
            
            # Generate and send OTP
            otp = generate_otp()
            request.session['otp'] = otp
            request.session['user_id'] = str(user.id)
            send_email(email, "Your OTP", f"Your OTP code is {otp}")
            return Response({'data': serializer.data, 'message': "User created successfully, OTP has been send to your email"}, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Signup failed: {serializer.errors}")
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
#SIGN UP API / CREATE STUDENT USER API
class StudentSignUpAPIView(APIView):
    # authentication_classes = [HOCTokenAuthentication]
    def post(self, request, *args, **kwargs):
        serializer = StudentUserSerializer(data=request.data)
        if serializer.is_valid():
            raw_password = serializer.validated_data.get('password')
            serializer.save(password=raw_password)
            return Response({'data': serializer.data, 'message': "User created successfully"}, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Signup failed: {serializer.errors}")
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, *args, **kwargs):
        student_id = request.data.get('id')  # Get the `id` from the request data
        
        if not student_id:
            return Response({'error': 'ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentUserSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': "User updated successfully"}, status=status.HTTP_200_OK)
        else:
            logger.error(f"Update failed: {serializer.errors}")
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
#SIGN IN API Faculty and HOC
class SignInAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            email = data.get("email")
            password = data.get("password")
            user = Faculty.objects.get(email=email)
            encryptPassword = encrypt_password(password)
            serializedUser = FacultyUserSerializer(user)

            if user.password == encryptPassword:
                if user.role == "faculty":
                    token = faculty_encode_token({"id": str(user.id), "role": user.role})
                else:
                    token = hoc_encode_token({"id": str(user.id), "role": user.role})
                refresh = RefreshToken.for_user(user)
                logger.info(f"User logged in successfully: {serializedUser.data}")
                print(serializedUser.data)
                return Response(
                    {
                        "token": str(token),
                        "access": str(refresh.access_token),
                        "data": serializedUser.data,
                        "message": "User logged in successfully",
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        except Faculty.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            logger.error(e)
            return Response({"message": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        
#VIEW FACULTY API
class FacultyListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        faculty = Faculty.objects.filter(role='faculty')
        serializedFaculty = FacultyViewSerializer(faculty, many=True)
        return Response({'data': serializedFaculty.data}, status=status.HTTP_200_OK)

#SIGN IN API Student
class StudentSignInAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            email = data.get("email")
            password = data.get("password")
            print(email, password)
            user = Student.objects.get(email=email)
            serializedUser = StudentDataSerializer(user)

            if user.password == password:
                if user.role == "student":
                    token = student_encode_token({"id": str(user.id), "role": user.role})
                else:
                    token = ob_encode_token({"id": str(user.id), "role": user.role})
                refresh = RefreshToken.for_user(user)
                print(serializedUser.data)
                logger.info(f"User logged in successfully: {serializedUser.data}")
                return Response(
                    {
                        "token": str(token),
                        "access": str(refresh.access_token),
                        "data": serializedUser.data,
                        "message": "User logged in successfully",
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        except Faculty.DoesNotExist:
            return Response(
                {"message": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            logger.error(e)
            return Response({"message": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

# YEAR API
class YearAPIView(APIView):
    # authentication_classes = [HOCTokenAuthentication]
    def post(self, request, *args, **kwargs):
        data = request.data
        seerializedYearData = YearDataSerializer(data=data)
        if seerializedYearData.is_valid():
            seerializedYearData.save()
            return Response({'data': seerializedYearData.data, 'message': "Year created successfully"}, status=status.HTTP_201_CREATED)
        else :
            return Response({'error': seerializedYearData.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):
        yearData = YearData.objects.all()
        serializedYearData = YearDataSerializer(yearData, many=True)
        return Response({'data': serializedYearData.data}, status=status.HTTP_200_OK)
        
#CLUB API
class ClubAPIView(APIView):
    # authentication_classes = [HOCTokenAuthentication]

    def post(self, request, *args, **kwargs):
        data = request.data
        facultyId = data.get('facultyID')  # Correct key to match your front-end data
        serializedClubData = ClubDataSerializer(data=data)

        if serializedClubData.is_valid():
            # Save the Club instance
            club_instance = serializedClubData.save()

            # Update the Faculty model with the new club ID
            try:
                faculty_instance = Faculty.objects.get(id=facultyId)
                faculty_instance.clubId = club_instance
                faculty_instance.save()

                return Response({'data': serializedClubData.data, 'message': "Club created and Faculty updated successfully"}, status=status.HTTP_201_CREATED)
            except Faculty.DoesNotExist:
                return Response({'error': 'Faculty not found'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'error': serializedClubData.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def get(self, request, *args, **kwargs):
        clubData = Club.objects.all()
        serializedClubData = ClubDataSerializer(clubData, many=True)
        return Response({'data': serializedClubData.data}, status=status.HTTP_200_OK)
        
#EVENT API
class EventAPIView(APIView):
    # authentication_classes = [HOCTokenAuthentication]
    def post(self, request, *args, **kwargs):
        data = request.data
        seerializedEventData = EventDataSerializer(data=data)
        if seerializedEventData.is_valid():
            seerializedEventData.save()
            return Response({'data': seerializedEventData.data, 'message': "Event created successfully"}, status=status.HTTP_201_CREATED)
        else :
            return Response({'error': seerializedEventData.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        club_id = request.query_params.get('clubId')
        batch_id = request.query_params.get('batchId')
        if club_id:
            eventData = Event.objects.filter(clubId=club_id, allBatches=batch_id)
            serializedEventData = EventDataSerializer(eventData, many=True)
            return Response({'data': serializedEventData.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'clubId parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
        data = request.data
        event_id = data.get('eventId')
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            return Response({'message': 'Event deleted successfully'}, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({'error': 'Invalid EventId'}, status=status.HTTP_400_BAD_REQUEST)
        
#CREATE BATCH API
class BatchAPIView(APIView):
    # authentication_classes = [HOCTokenAuthentication]
    def post(self, request, *args, **kwargs):
        data = request.data
        if not validate_batch(data.get('batchYear')):
            return Response({'error': "Invalid batch year format"}, status=status.HTTP_400_BAD_REQUEST)
        serializedBatchData = BatchDataSerializer(data=data)
        if serializedBatchData.is_valid():
            serializedBatchData.save()
            return Response({'data': serializedBatchData.data, 'message': "Batch created successfully"}, status=status.HTTP_201_CREATED)
        else :
            return Response({'error': serializedBatchData.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):
        batchData = Batch.objects.all()
        serializedBatchData = BatchDataSerializer(batchData, many=True)
        return Response({'data': serializedBatchData.data}, status=status.HTTP_200_OK)

# UPLOAD STUDENTS API
class UploadStudentsAPIView(APIView):
   def post(self, request, *args, **kwargs):
        print(request.FILES)
        print(request.POST)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            club_id = form.cleaned_data['ClubId']
            batch_id = form.cleaned_data['BatchId']
            file = form.cleaned_data['file']
            
            print(club_id, batch_id, file)
            
            try:
                club = Club.objects.get(id=club_id)
                batch = Batch.objects.get(id=batch_id)
            except Club.DoesNotExist:
                return Response({'error': 'Invalid ClubId'}, status=400)
            except Batch.DoesNotExist:
                return Response({'error': 'Invalid BatchId'}, status=400)
            
            try:
                df = pd.read_excel(file)
            except Exception as e:
                return Response({'error': str(e)}, status=400)

            for index, row in df.iterrows():
                try:
                    Student.objects.create(
                        email=row['email'],
                        password=row['rollNo'],  
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        bloodGroup=row['bloodGroup'],
                        gender=row['gender'],
                        ClubId=club,
                        BatchId=batch,
                        rollNo=row['rollNo'],
                        registerNumber=row['registerNumber'],
                        department=row['department'],
                        dob=row['dob'],
                        phoneNumber=row['phoneNumber']
                    )
                except Exception as e:
                    return Response({'error': str(e)}, status=400)

            return Response({'message': 'Students created successfully'}, status=201)
        else:
            return Response({'error': form.errors}, status=400)
        
# STUDENT LIST API
class StudentListAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        club_id = data.get('ClubId')
        batch_id = data.get('BatchId')
        try:
            club = Club.objects.get(id=club_id)
            batch = Batch.objects.get(id=batch_id)
        except Club.DoesNotExist:
            return Response({'error': 'Invalid ClubId'}, status=400)
        except Batch.DoesNotExist:
            return Response({'error': 'Invalid BatchId'}, status=400)
        
        students = Student.objects.filter(ClubId=club, BatchId=batch)
        serializedStudents = StudentListSerializer(students, many=True)
        return Response({'data': serializedStudents.data}, status=200)

# MARK ATTENDANCE API
class MarkAttendanceAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MarkAttendanceSerializer(data=request.data)
        if serializer.is_valid():
            club_id = serializer.validated_data['ClubId']
            batch_id = serializer.validated_data['BatchId']
            event_id = serializer.validated_data['EventId']
            student_ids = serializer.validated_data['StudentIds']
            
            event = Event.objects.get(id=event_id)
            hours = event.numberOfHours
            
            # Mark attendance for each student
            for student_id in student_ids:
                student = Student.objects.get(id=student_id)
                student.events.add(event)
                student.noOfHours += hours
                student.save()
                
            return Response({'message': 'Students marked with event successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# EVENT ATTENDANCE API
class EventAttendanceAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        batch_id = data.get('BatchId')
        event_id = data.get('EventId')
        
        try:
            batch = Batch.objects.get(id=batch_id)
            event = Event.objects.get(id=event_id)
        except Batch.DoesNotExist:
            return Response({'error': 'Invalid BatchId'}, status=400)
        except Event.DoesNotExist:
            return Response({'error': 'Invalid EventId'}, status=400)
        
        students = Student.objects.filter(BatchId=batch, events=event)
        serializedStudents = StudentListSerializer(students, many=True)
        return Response({'data': serializedStudents.data}, status=200)
    
# ANNOUNCEMENTS API
class AnnouncementsAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        data = request.data
        club_id = data.get('clubId')
        batch_id = data.get('batchId')
        event_id = data.get('eventId')
        announcement = data.get('announcement')
        
        try:
            club = Club.objects.get(id=club_id)
            batch = Batch.objects.get(id=batch_id)
            event = Event.objects.get(id=event_id)
        except Club.DoesNotExist:
            return Response({'error': 'Invalid ClubId'}, status=400)
        except Batch.DoesNotExist:
            return Response({'error': 'Invalid BatchId'}, status=400)
        except Event.DoesNotExist:
            return Response({'error': 'Invalid EventId'}, status=400)
        
        announcementSerializer = AnnouncementsSerializer(data=data)
        if announcementSerializer.is_valid():
            announcementSerializer.save()
            return Response({'data': announcementSerializer.data, 'message': "Announcement created successfully"}, status=status.HTTP_201_CREATED)
        
        return Response({'error': announcementSerializer.errors}, status=400)
    
    def get(self, request, *args, **kwargs):
        club_id = request.query_params.get('clubId')
        
        if club_id:
            announcements = Announcements.objects.filter(clubId=club_id)
            serializedAnnouncements = AnnouncementsSerializer(announcements, many=True)
            return Response({'data': serializedAnnouncements.data}, status=200)
        return Response({'error': 'clubId parameter is required'}, status=400)
    
# ADMIN ANNOUNCEMENTS LIST API
class AdminAnnouncementsListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        announcements = Announcements.objects.all()
        serializedAnnouncements = AdminAnnouncementsSerializer(announcements, many=True)
        return Response({'data': serializedAnnouncements.data}, status=200)
    
# VIEW ATTENDANCE API
class ViewAttendanceAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        club_id = data.get('clubId')
        student_id = data.get('studentId')
        
        clubevents = Event.objects.filter(clubId=club_id)
        studentevent = Student.objects.get(id=student_id).events.all()
        hoursCompleted = Student.objects.get(id=student_id).noOfHours
        
        present = []
        absent = []
        attendancePercentage = 0
        for clubevent in clubevents:
            if clubevent in studentevent:
                present.append(clubevent.eventName)
            else:
                absent.append(clubevent.eventName)
        
        if len(clubevents) != 0:
            attendancePercentage = (len(present)/len(clubevents)) * 100
            
        responseData = {
            'present': present,
            'absent': absent,
            'attendancePercentage': attendancePercentage,
            'hoursCompleted': hoursCompleted
        }
        
        return Response({'data': responseData}, status=200)
    
# STUDENT DATA API
class StudentDataAPIView(APIView):
    def get(self, request, *args, **kwargs):
        student_id = request.query_params.get('studentId')
        student = Student.objects.get(id=student_id)
        serializedStudent = StudentDataSerializer(student)
        return Response({'data': serializedStudent.data}, status=200)
    
class StudentOTPAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        otp = generate_otp()
        send_email(email,"Your OTP", f"Your OTP code is {otp}")
        data['otp'] = otp
        serializedOTP = OTPSerializer(data=data)
        if serializedOTP.is_valid():
            serializedOTP.save()
            return Response({'data': serializedOTP.data, 'message': "OTP sent successfully"}, status=200)
        else:
            logger.error(f"OTP sending failed: {serializedOTP.errors}")
            return Response({'error': serializedOTP.errors, 'message':"otp with this email already exists"}, status=400)
        
class StudentOTPVerifyAPIView(APIView):
    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email')
        otp = request.query_params.get('otp')
        first_name = request.query_params.get('first_name')
        last_name = request.query_params.get('last_name')
        password = request.query_params.get('password')
        
        try:
            otp_instance = OTP.objects.get(email=email, otp=otp)
            otp_instance.delete()
            student = Student.objects.create(email=email, password=password, first_name=first_name, last_name=last_name)
            serializedStudent = StudentOTPSerializer(student)
            return Response({'data':serializedStudent.data, 'message': 'OTP verified successfully'}, status=200)
        except OTP.DoesNotExist:
            return Response({'error': 'Invalid OTP'}, status=400)

#SORTING FILTERS
class EventTypeCountAPIView(APIView):
    def get(self, request, *args, **kwargs):
        clubId = request.query_params.get('clubId')
        event_type_counts = Event.objects.filter(clubId=clubId).values('eventType').annotate(count=Count('eventType')).order_by('-count')
        # Preparing the response data
        response_data = [
            {'eventType': event['eventType'], 'count': event['count']}
            for event in event_type_counts
        ]
        return Response({'data': response_data}, status=200)
    
class BloodGroupListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try :
            bloodGroup = request.query_params.get('bloodGroup')
            batchId = request.query_params.get('batchId')
            bloodGroupStudents = Student.objects.filter(bloodGroup=bloodGroup, BatchId=batchId)
            serializedBloodGroupStudents = StudentBloodGroupSerializer(bloodGroupStudents, many=True)
            return Response({'data': serializedBloodGroupStudents.data}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    
class DepartmentListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        department = request.query_params.get('department')
        batchId = request.query_params.get('batchId')
        departmentStudents = Student.objects.filter(department=department, BatchId=batchId)
        serializedDepartmentStudents = DepartmentStudentsSerializer(departmentStudents, many=True)
        return Response({'data': serializedDepartmentStudents.data}, status=200)
    
class EventClubListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        clubId = request.query_params.get('clubId')
        events = list(Event.objects.filter(clubId=clubId))
        eventsCoolab = list(Event.objects.filter(collaborators=clubId))
        combined_events = events + [event for event in eventsCoolab if event not in events]
        serializedEvents = EventDataSerializer(combined_events, many=True)
        return Response({'data': serializedEvents.data}, status=200)
        
class EventStudentsListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        eventId = request.query_params.get('eventId')
        clubId = request.query_params.get('clubId')

        try:
            event = Event.objects.get(id=eventId)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)
        students = Student.objects.filter(
            events=event,
            ClubId=clubId
        )

        serializedStudents = StudentListSerializer(students, many=True)
        return Response({'data': serializedStudents.data}, status=status.HTTP_200_OK)
    
class UpcomingAnnouncementsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        club_id = request.query_params.get('clubId')
        current_datetime = timezone.now()  
        announcements = Announcements.objects.filter(
            clubId=club_id,
            eventId__eventDate__gte=current_datetime.date() 
        )
        serializedAnnouncements = AnnouncementsSerializer(announcements, many=True)
        return Response({'data': serializedAnnouncements.data}, status=200)
    
class UpcomingEventsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        club_id = request.query_params.get('clubId')
        current_datetime = timezone.now()  
        events = Event.objects.filter(
            clubId=club_id,
            eventDate__gte=current_datetime.date()  
        )
        serializedEvents = EventDataSerializer(events, many=True)
        return Response({'data': serializedEvents.data}, status=200)
