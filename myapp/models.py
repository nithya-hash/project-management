from django.db import models




class Study(models.Model):
    PHASE_CHOICES = [
        ('Planning', 'Planning'),
        ('Development', 'Development'),
        ('Testing', 'Testing'),
        ('Deployment', 'Deployment'),
    ]
    STATUS_CHOICES = [
        ('Planned', 'Planned'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    ]

    study_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='Default Project Name')
    description = models.TextField(null=True, blank=True)
    phase = models.CharField(max_length=20, choices=PHASE_CHOICES)
    sponsor_name = models.CharField(max_length=100, default='Unknown Sponsor')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Planned')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class CustomUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)