from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CBCTestResult)
admin.site.register(CBCTestResultImage)
admin.site.register(CBCTestResultPDF)
admin.site.register(CBCTestResultDocx)