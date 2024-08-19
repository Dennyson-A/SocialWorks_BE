from rest_framework import serializers
from .models import Student, Faculty, YearData, Club, Event, Batch, Announcements, OTP

class StudentUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = "__all__"
        
class FacultyUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Faculty
        fields = "__all__"
        
class YearDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearData
        fields = "__all__"
        
class ClubDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = "__all__"
        
class EventDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        
class BatchDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = "__all__"
        
class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'rollNo', 'registerNumber', 'department']
        
class MarkAttendanceSerializer(serializers.Serializer):
    ClubId = serializers.UUIDField()
    BatchId = serializers.UUIDField()
    EventId = serializers.UUIDField()
    StudentIds = serializers.ListField(
        child=serializers.UUIDField()
    )

    def validate(self, data):
        # Validate Club
        try:
            Club.objects.get(id=data['ClubId'])
        except Club.DoesNotExist:
            raise serializers.ValidationError("Invalid ClubId")

        # Validate Batch
        try:
            Batch.objects.get(id=data['BatchId'])
        except Batch.DoesNotExist:
            raise serializers.ValidationError("Invalid BatchId")

        # Validate Event
        try:
            Event.objects.get(id=data['EventId'])
        except Event.DoesNotExist:
            raise serializers.ValidationError("Invalid EventId")

        # Validate Students
        students = Student.objects.filter(id__in=data['StudentIds'])
        if students.count() != len(data['StudentIds']):
            raise serializers.ValidationError("One or more StudentIds are invalid")
        return data
    
class AnnouncementsDataSerializer(serializers.Serializer):
    ClubId = serializers.UUIDField()
    BatchId = serializers.UUIDField()
    EventId = serializers.UUIDField()
    Announcement = serializers.CharField()
    
    def validate(self, data):
        # Validate Club
        try:
            Club.objects.get(id=data['ClubId'])
        except Club.DoesNotExist:
            raise serializers.ValidationError("Invalid ClubId")

        # Validate Batch
        try:
            Batch.objects.get(id=data['BatchId'])
        except Batch.DoesNotExist:
            raise serializers.ValidationError("Invalid BatchId")

        # Validate Event
        try:
            Event.objects.get(id=data['EventId'])
        except Event.DoesNotExist:
            raise serializers.ValidationError("Invalid EventId")
        return data
    
class AnnouncementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcements
        fields = "__all__"
        
class AdminAnnouncementsSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source='eventId.eventName', read_only=True)
    club_name = serializers.CharField(source='clubId.clubname', read_only=True)

    class Meta:
        model = Announcements
        fields = ['id', 'announcement', 'event_name', 'club_name']
        
class StudentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'rollNo', 'registerNumber', 'department', 'dob', 'phoneNumber', 'role', 'noOfHours', 'ClubId', 'BatchId']
        
class FacultyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'email', 'first_name', 'last_name']
        
class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [ 'eventName', 'eventType', 'eventDate', 'eventDescription', 'numberOfHours']
        
class StudentBloodGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'rollNo', 'registerNumber', 'department', 'dob', 'phoneNumber', 'gender']
        
class DepartmentStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'rollNo', 'registerNumber', 'department', 'dob', 'phoneNumber', 'noOfHours']
        
class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['email', 'password', 'first_name', 'last_name', 'otp']
        
class StudentOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'email', 'first_name', 'last_name']