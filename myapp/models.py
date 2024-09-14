from django.db import models
from django.contrib.auth.models import User

# Doctor Model
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    available_from = models.TimeField()
    available_to = models.TimeField()

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"

# Patient Model
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.get_full_name()

# Appointment Model
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason_for_visit = models.TextField()
    def __str__(self):
      return f"Appointment: {self.patient.user.get_full_name()} with {self.doctor.user.get_full_name()} on {self.appointment_date}"


    # def __str__(self):
    #     return f"Appointment: {self.patient.user.get_full_name()} with {self.doctor.user.get_full_name()} on {self.appointment_date}"
