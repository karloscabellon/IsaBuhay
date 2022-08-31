from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('clientSide/', DisplayClientSide.as_view(), name='DisplayClientSide'),
    path('reports/', DisplayAllCBCTestResult.as_view(), name='DisplayAllCBCTestResult'),
    path('CBCTestResults/<str:pk>/', DisplayCBCTestResult.as_view(), name='DisplayCBCTestResult'),
    path('addingOptions/', DisplayAddingOptions.as_view(), name='DisplayAddingOptions'),
    path('uploadImage/', UploadImage.as_view(), name='UploadImage'),
    path('uploadPDF/', UploadPDF.as_view(), name='UploadPDF'),
    path('uploadDocx/', UploadDocx.as_view(), name='UploadDocx'),
    path('captureImage/', CaptureImage.as_view(), name='CaptureImage'),
    path('CBCTestResult/create/<str:type>/<str:pk>/', CreateCBCTestResult.as_view(), name='CreateCBCTestResult'),
    path('CBCTestResult/update/<str:pk>/', UpdateCBCTestResult.as_view(), name='UpdateCBCTestResult'),
    path('CBCTestResult/delete/<str:pk>/', DeleteCBCTestResult.as_view(), name='DeleteCBCTestResult'),
    path('uploadedImage/delete/<str:pk>/', DeleteUploadedImage.as_view(), name='DeleteUploadedImage'),
    path('capturedImage/delete/<str:pk>/', DeleteCapturedImage.as_view(), name='DeleteCapturedImage'),
    path('pdf/delete/<str:pk>/', DeletePDF.as_view(), name='DeletePDF'),
    path('docx/delete/<str:pk>/', DeleteDocx.as_view(), name='DeleteDocx'),
]
