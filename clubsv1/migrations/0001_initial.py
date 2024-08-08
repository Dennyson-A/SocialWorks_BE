# Generated by Django 5.0.7 on 2024-08-07 04:56

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('batchYear', models.CharField(max_length=20, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('clubname', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(default='', max_length=255)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('role', models.CharField(choices=[('faculty', 'faculty'), ('HOC', 'HOC')], default='faculty', max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='YearData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('year', models.IntegerField(unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('eventName', models.CharField(max_length=100, unique=True)),
                ('eventDate', models.DateField()),
                ('eventTime', models.TimeField()),
                ('eventVenue', models.CharField(max_length=100)),
                ('eventDescription', models.TextField()),
                ('numberOfHours', models.IntegerField()),
                ('batchID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubsv1.batch')),
                ('clubId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubsv1.club')),
                ('collaborators', models.ManyToManyField(blank=True, related_name='events_as_collaborator', to='clubsv1.club')),
                ('yearId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubsv1.yeardata')),
            ],
        ),
        migrations.CreateModel(
            name='Announcements',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('announcement', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('batchId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubsv1.batch')),
                ('clubId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubsv1.club')),
                ('eventId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubsv1.event')),
            ],
        ),
        migrations.AddField(
            model_name='club',
            name='facultyID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubsv1.faculty'),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(default='', max_length=255)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('rollNo', models.CharField(max_length=20)),
                ('registerNumber', models.CharField(max_length=20)),
                ('department', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('phoneNumber', models.CharField(max_length=20)),
                ('role', models.CharField(choices=[('student', 'student'), ('OB', 'OB')], default='student', max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('BatchId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubsv1.batch')),
                ('ClubId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubsv1.club')),
                ('events', models.ManyToManyField(blank=True, to='clubsv1.event')),
            ],
        ),
    ]
