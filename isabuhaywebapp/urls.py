from django.urls import path
from .views import *

urlpatterns = [
    path('adminpaylist/', DisplayPaymentList.as_view(), name='DisplayPaymentList'),
    path('adminmain/', DisplayAdminPage.as_view(), name='DisplayAdminPage'),
    path('adminrev/', DisplayRevenueMonth.as_view(), name='DisplayRevenueMonth'),
    path('adminuserlist/', DisplayAllUsers.as_view(), name='DisplayAllUsers'),
    path('adminmonthlyusers/', DisplayUsersMonthly.as_view(), name='DisplayUsersMonthly'),
    path('', DisplayLandingPage.as_view(), name='DisplayLandingPage'),
    
    path('analytics/', DisplayAnalytics.as_view(), name='DisplayAnalytics'),
    path('clientSide/', DisplayClientSide.as_view(), name='DisplayClientSide'),
    path('register/', CreateAccountPage.as_view(), name='CreateAccountPage'),
    path('login/', DisplayLoginPage.as_view(), name='DisplayLoginPage'),
    path('logout/', LogoutView.as_view(), name='LogoutView'),
    path('reset_password/', PasswordResetPage.as_view(), name='reset_password'),
    path('reset_password_sent/', PasswordResetEmailSentPage.as_view(), name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/', PasswordResetConfirmPage.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('account/', DisplayAccountPage.as_view(), name='DisplayAccountPage'),
    path('account/update', UpdateAccountPage.as_view(), name='UpdateAccountPage'),
    path('account/update/change_password', UpdatePasswordPage.as_view(), name='UpdatePasswordPage'),
    path('account/update/change_photo', UpdatePhotoPage.as_view(), name='UpdatePhotoPage'),
    path('account/delete', DeleteAccountPage.as_view(), name='DeleteAccountPage'),
    path('reports/', DisplayAllCBCTestResult.as_view(), name='DisplayAllCBCTestResult'),
    path('CBCTestResults/<str:pk>/', DisplayCBCTestResult.as_view(), name='DisplayCBCTestResult'),
    path('addingOptions/', DisplayAddingOptions.as_view(), name='DisplayAddingOptions'),
    path('paymentMethod/<str:type>/<str:pk>/', PaymentMethod.as_view(), name='PaymentMethod'),
    path('promoOptions/<str:type>/', DisplayAllPromoOptions.as_view(), name='DisplayAllPromoOptions'),
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
    path('complete/', PaymentComplete.as_view(), name="complete"),
]

# class PasswordResetPage(aviews.PasswordResetView):
#     pass

# class PasswordResetEmailSentPage(aviews.PasswordResetDoneView):
#     pass

# class PasswordResetConfirmPage(aviews.PasswordResetConfirmView):
#     pass

# class PasswordResetCompleteView(aviews.PasswordResetCompleteView):
