from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import pandas as pd

from .models import Faculty, YearData, Club, Event, Student, Batch, Announcements
from .serializers import FacultyUserSerializer, YearDataSerializer, ClubDataSerializer, EventDataSerializer, StudentUserSerializer, BatchDataSerializer, StudentListSerializer, MarkAttendanceSerializer, AnnouncementsDataSerializer, AnnouncementsSerializer, AdminAnnouncementsSerializer
from .serializers import StudentDataSerializer
from .methods import encrypt_password, faculty_encode_token, ob_encode_token, hoc_encode_token, validate_batch, student_encode_token
from .authentication import HOCTokenAuthentication
from .forms import UploadFileForm
import logging

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
        serializer = FacultyUserSerializer(data=request.data)
        
        if serializer.is_valid():
            raw_password = serializer.validated_data.get('password')
            encrypted_password = encrypt_password(raw_password)
            serializer.save(password=encrypted_password)
            return Response({'data': serializer.data, 'message': "User created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#SIGN UP API / CREATE STUDENT USER API
class StudentSignUpAPIView(APIView):
    # authentication_classes = [HOCTokenAuthentication]
    def post(self, request, *args, **kwargs):
        serializer = StudentUserSerializer(data=request.data)
        if serializer.is_valid():
            raw_password = serializer.validated_data.get('password')
            encrypted_password = encrypt_password(raw_password)
            serializer.save(password=encrypted_password)
            return Response({'data': serializer.data, 'message': "User created successfully"}, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Signup failed: {serializer.errors}")
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
        

class StudentSignInAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            email = data.get("email")
            password = data.get("password")
            user = Student.objects.get(email=email)
            serializedUser = StudentDataSerializer(user)

            if user.password == password:
                if user.role == "student":
                    token = student_encode_token({"id": str(user.id), "role": user.role})
                else:
                    token = ob_encode_token({"id": str(user.id), "role": user.role})
                refresh = RefreshToken.for_user(user)
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
        seerializedClubData = ClubDataSerializer(data=data)
        if seerializedClubData.is_valid():
            seerializedClubData.save()
            return Response({'data': seerializedClubData.data, 'message': "Club created successfully"}, status=status.HTTP_201_CREATED)
        else :
            return Response({'error': seerializedClubData.errors}, status=status.HTTP_400_BAD_REQUEST)
    
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
        
    # def get(self, request, *args, **kwargs):
    #     eventData = Event.objects.all()
    #     serializedEventData = EventDataSerializer(eventData, many=True)
    #     return Response({'data': serializedEventData.data}, status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        club_id = request.query_params.get('clubId')
        if club_id:
            eventData = Event.objects.filter(clubId=club_id)
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
    
   