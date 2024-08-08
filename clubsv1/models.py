from django.db import models
from django.utils import timezone
import uuid

class Student(models.Model):
    Roles = ( ('student', 'student'), ('OB', 'OB') )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, default="")
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    ClubId = models.ForeignKey('Club', on_delete=models.CASCADE)
    BatchId = models.ForeignKey('Batch', on_delete=models.CASCADE)
    rollNo = models.CharField(max_length=20)
    registerNumber = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    dob = models.DateField()
    phoneNumber = models.CharField(max_length=20)
    role = models.CharField(max_length=255,choices=Roles, default="student")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True)
    noOfHours = models.IntegerField(default=0)
    events = models.ManyToManyField('Event', blank=True)

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clubId = models.ForeignKey('Club', on_delete=models.CASCADE)
    yearId = models.ForeignKey('YearData', on_delete=models.CASCADE)
    batchID = models.ForeignKey('Batch', on_delete=models.CASCADE)
    eventName = models.CharField(max_length=100, unique=True)
    eventDate = models.DateField()
    eventTime = models.TimeField()
    eventVenue = models.CharField(max_length=100)
    eventDescription = models.TextField()
    numberOfHours = models.IntegerField()
    collaborators = models.ManyToManyField('Club', blank=True, related_name='events_as_collaborator')

class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clubname = models.CharField(max_length=100, unique=True)
    facultyID = models.ForeignKey('Faculty', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True)
    
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