from django.db import models
from django.contrib.auth.models import User

class MedicalReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='reports/')
    upload_date = models.DateField(auto_now_add=True)
    report_name = models.CharField(max_length=100, default="Routine Check")
    
    # Biomarkers shown in your dashboard
    blood_pressure = models.IntegerField(default=120)
    sugar = models.IntegerField(default=100)
    cholesterol = models.IntegerField(default=200)
    hemoglobin = models.FloatField(default=13.5)

    def __str__(self):
        return f"{self.report_name} - {self.upload_date}"