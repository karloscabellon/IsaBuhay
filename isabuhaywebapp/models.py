from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CBCTestResultImage(models.Model):
    testImage = models.ImageField(upload_to='images/', blank=False, null=False)
    
    def get_absolute_url(self):
        return reverse('CreateCBCTestResult', kwargs={'pk': str(self.pk), 'type': 'image'})

class CBCTestResultPDF(models.Model):
    testPDF = models.FileField(upload_to='pdfs/', blank=False, null=False)
    
    def get_absolute_url(self):
        return reverse('CreateCBCTestResult', kwargs={'pk': str(self.pk), 'type': 'pdf'})

class CBCTestResultDocx(models.Model):
    testDocx = models.FileField(upload_to='docs/', blank=False, null=False)
    
    def get_absolute_url(self):
        return reverse('CreateCBCTestResult', kwargs={'pk': str(self.pk), 'type': 'docx'})

class CBCTestResult(models.Model):
    testImage = models.OneToOneField(CBCTestResultImage, on_delete=models.CASCADE, blank=True, null=True)
    testPDF = models.OneToOneField(CBCTestResultPDF, on_delete=models.CASCADE, blank=True, null=True)
    testDocx = models.OneToOneField(CBCTestResultDocx, on_delete=models.CASCADE, blank=True, null=True)
    source = models.CharField(max_length=50, blank=False, null=False)
    labNumber = models.CharField(max_length=50, blank=False, null=False)
    pid = models.CharField(max_length=50, blank=False, null=False)
    dateRequested = models.DateTimeField(blank=False, null=False)
    dateReceived = models.DateTimeField(blank=False, null=False)
    whiteBloodCells = models.FloatField(blank=False, null=False)
    redBloodCells = models.FloatField(blank=False, null=False)
    hemoglobin = models.FloatField(blank=False, null=False)
    hematocrit = models.FloatField(blank=False, null=False)
    meanCorpuscularVolume = models.FloatField(blank=False, null=False)
    meanCorpuscularHb = models.FloatField(blank=False, null=False)
    meanCorpuscularHbConc = models.FloatField(blank=False, null=False)
    rbcDistributionWidth = models.FloatField(blank=False, null=False)
    plateletCount = models.FloatField(blank=False, null=False)
    segmenters = models.FloatField(blank=False, null=False)
    lymphocytes = models.FloatField(blank=False, null=False)
    monocytes = models.FloatField(blank=False, null=False)
    eosinophils = models.FloatField(blank=False, null=False)
    basophils = models.FloatField(blank=False, null=False)
    bands = models.FloatField(blank=False, null=False)
    absoluteSeg = models.FloatField(blank=False, null=False)
    absoluteLymphocyteCount = models.FloatField(blank=False, null=False)
    absoluteMonocyteCount = models.FloatField(blank=False, null=False)
    absoluteEosinophilCount = models.FloatField(blank=False, null=False)
    absoluteBasophilCount = models.FloatField(blank=False, null=False)
    absoluteBandCount = models.FloatField(blank=False, null=False)

    def get_absolute_url(self):
        return reverse('DisplayCBCTestResult', kwargs={'pk': str(self.pk)})