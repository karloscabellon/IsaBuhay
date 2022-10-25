from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', DisplayLandingPage.as_view(), name='DisplayLandingPage'),
    path('clientSide/', DisplayClientSide.as_view(), name='DisplayClientSide'),
    path('register/', CreateAccountPage.as_view(), name='CreateAccountPage'),
    path('login/', DisplayLoginPage.as_view(), name='DisplayLoginPage'),
    path('logout/', LogoutView.as_view(), name="LogoutView"),
    path('account/', DisplayAccountPage.as_view(), name='DisplayAccountPage'),
    path('account/update', UpdateAccountPage.as_view(), name='UpdateAccountPage'),
    path('account/delete', DeleteAccountPage.as_view(), name='DeleteAccountPage'),
    path('reports/', DisplayAllCBCTestResult.as_view(), name='DisplayAllCBCTestResult'),
    path('CBCTestResults/<str:pk>/', DisplayCBCTestResult.as_view(), name='DisplayCBCTestResult'),
    path('addingOptions/', DisplayAddingOptions.as_view(), name='DisplayAddingOptions'),
    path('paymentMethod/<str:pk>/', PaymentMethod.as_view(), name='PaymentMethod'),
    path('promoOptions/', DisplayAllPromoOptions.as_view(), name='DisplayAllPromoOptions'),
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
    path('complete/', views.paymentComplete, name="complete"),
]
