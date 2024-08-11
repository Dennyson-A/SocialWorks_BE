from django.db import models
from django.utils import timezone
import uuid

class Student(models.Model):
    Roles = ( ('student', 'student'), ('OB', 'OB') )
    Dept = ( ('CSE', 'CSE'), ('ECE', 'ECE'), ('EEE', 'EEE'), ('MECH', 'MECH'), ('IT', 'IT'), ('AIDS', 'AIDS') )
    Gend = (('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others'))
    BloodTypes = (('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, default="")
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    bloodGroup = models.CharField(max_length=10, choices=BloodTypes, default="nil")
    gender = models.CharField(max_length=10, choices=Gend, default="Others")
    rollNo = models.CharField(max_length=20)
    registerNumber = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.CharField(max_length=100, choices=Dept, default="SNH")
    dob = models.DateField()
    phoneNumber = models.CharField(max_length=20)
    role = models.CharField(max_length=255,choices=Roles, default="student")
    noOfHours = models.IntegerField(default=0)
    ClubId = models.ForeignKey('Club', on_delete=models.CASCADE)
    BatchId = models.ForeignKey('Batch', on_delete=models.CASCADE)
    events = models.ManyToManyField('Event', blank=True, related_name='students')  
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
    
class Faculty(models.Model):
    Roles = ( ('faculty', 'faculty'), ('HOC', 'HOC') )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, default="")
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255,choices=Roles, default="faculty")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True)
    clubId = models.ForeignKey('Club', on_delete=models.CASCADE, blank=True, null=True)

class Event(models.Model):
    Type = ( ('Workshop', 'Workshop'), ('Seminar', 'Seminar'), ('Training', 'Training'), ('Community Service', 'Community Service'), 
            ('Volunter Service', 'Volunter Service'), ('Camp', 'Camp'), ('Outreach', 'Outreach'), ('Others', 'Others') )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clubId = models.ForeignKey('Club', on_delete=models.CASCADE)
    yearId = models.ForeignKey('YearData', on_delete=models.CASCADE)
    eventName = models.CharField(max_length=100, unique=True)
    eventType = models.CharField(max_length=100, choices=Type, default="Others")
    eventDate = models.DateField()
    eventTime = models.TimeField()
    eventVenue = models.CharField(max_length=100)
    eventDescription = models.TextField()
    numberOfHours = models.IntegerField()
    collaborators = models.ManyToManyField('Club', blank=True, related_name='events_as_collaborator')
    allBatches = models.ManyToManyField('Batch', blank=True, related_name='events_as_allBatches')

class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clubname = models.CharField(max_length=100, unique=True)
    facultyID = models.ForeignKey('Faculty', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True)
    facultyIDs = models.ManyToManyField('Faculty', blank=True, related_name='clubs_as_faculty')
    
class Batch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batchYear = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

class YearData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    year = models.IntegerField(unique=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

class Announcements(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clubId = models.ForeignKey('Club', on_delete=models.CASCADE)
    batchId = models.ForeignKey('Batch', on_delete=models.CASCADE)
    eventId = models.ForeignKey('Event', on_delete=models.CASCADE)
    announcement = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True)