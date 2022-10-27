from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(CBCTestResult)
admin.site.register(CBCTestResultImage)
admin.site.register(CBCTestResultPDF)
admin.site.register(CBCTestResultDocx)
admin.site.register(PromoOptions)
admin.site.register(Payments)