from decimal import Decimal
from django.urls import reverse
from django.db import models
from datetime import date
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from traitlets import default
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, email, firstname, lastname, phone_number, password=None):
        if not username: raise ValueError("Username is required")
        if not email: raise ValueError("Email is required")
        if not firstname: raise ValueError("Firstname is required")
        if not lastname: raise ValueError("Lastname is required")
        if not phone_number: raise ValueError("Phone_number is required")

        user = self.model(
            username = username,
            email = self.normalize_email(email),
            firstname = firstname,
            lastname = lastname,
            phone_number = phone_number
        )
        user.date_created = date.today()
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, firstname, lastname, phone_number, password=None):
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            firstname = firstname,
            lastname = lastname,
            phone_number = phone_number
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.date_created = date.today()
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser):
    username = models.CharField(verbose_name="username", max_length=25, blank=False, null=False, unique=True)
    email = models.EmailField(verbose_name="email address", max_length=50, blank=False, null=False, unique=True)
    firstname = models.CharField(verbose_name="first name", max_length=20, blank=False, null=False)
    lastname = models.CharField(verbose_name="last name", max_length=20, blank=False, null=False)
    phone_number = models.CharField(verbose_name="phone number", max_length=15, blank=False, null=False)

    profile_picture = models.ImageField(verbose_name="profile picture", null=True, blank=True)
    birthdate = models.DateTimeField(verbose_name="birthdate", blank=True, null=True)
    blood_type = models.CharField(verbose_name="blood type", max_length=5, blank=True, null=True)
    height = models.DecimalField(verbose_name="height", decimal_places = 2, max_digits = 6, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True)
    weight = models.DecimalField(verbose_name="weight", decimal_places = 2, max_digits = 6, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_created = models.DateTimeField(verbose_name="date created", blank=True, null=True)

    uploads = models.IntegerField(verbose_name="uploads",blank=False, null=False, default=5)

    USERNAME_FIELD="username"

    REQUIRED_FIELDS = [
        'email',
        'firstname',
        'lastname',
        'phone_number',
    ]

    objects = UserManager()
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

# class Client


# Marc John Corral

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

class PromoOptions(models.Model):
    uploads = models.IntegerField(blank=False, null=False)
    price = models.FloatField(blank=False, null=False)

    def get_absolute_url(self):
        return reverse('PaymentMethod', kwargs={'pk': str(self.pk)})

class Payments(models.Model):
    promo = models.ForeignKey(PromoOptions, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    
class CBCTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    testImage = models.OneToOneField(CBCTestResultImage, on_delete=models.CASCADE, blank=True, null=True)
    testPDF = models.OneToOneField(CBCTestResultPDF, on_delete=models.CASCADE, blank=True, null=True)
    testDocx = models.OneToOneField(CBCTestResultDocx, on_delete=models.CASCADE, blank=True, null=True)
    source = models.CharField(max_length=50, blank=False, null=False)
    labNumber = models.CharField(max_length=50, blank=False, null=False)
    pid = models.CharField(max_length=50, blank=False, null=False)
    dateRequested = models.DateTimeField(blank=True, null=True)
    dateReceived = models.DateTimeField(blank=True, null=True)
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

# Marc John Corral