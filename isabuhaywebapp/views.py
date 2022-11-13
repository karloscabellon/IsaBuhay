import cv2
import numpy as np
import pytesseract
import re
import PyPDF4
import docx2txt as d2t
from urllib.request import urlopen
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import *
from isabuhaywebapp.models import *
from django.shortcuts import *
from .forms import *
from datetime import datetime
from django.contrib.auth.views import LoginView
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.mixins import LoginRequiredMixin
from IsabuhayWebsite import settings
import json
import os
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q

class DisplayLandingPage(TemplateView):
    template_name = 'displayLandingPage.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('DisplayClientSide'))
        return super().get(request, *args, **kwargs)

class CreateAccountPage(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'createAccountPage.html'
    success_url = reverse_lazy('DisplayLoginPage')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('DisplayClientSide'))
        return super().get(request, *args, **kwargs)

class DisplayLoginPage(LoginView):
    template_name = 'loginPage.html'
    next_page = 'DisplayClientSide'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('DisplayClientSide'))
        return super().get(request, *args, **kwargs)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)

class DisplayClientSide(LoginRequiredMixin, TemplateView):
    template_name = 'displayClientSide.html'

class DisplayAccountPage(LoginRequiredMixin, TemplateView):
    template_name = 'displayAccountPage.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        self.request.user.birthdate = None if self.request.user.birthdate is None else datetime.strftime(self.request.user.birthdate, "%Y-%m-%d")
        return self.render_to_response(context)

   
class UpdateAccountPage(LoginRequiredMixin, UpdateView):
    template_name = 'updateAccountPage.html'
    model = User
    form_class = UpdateAccountForm
    success_url = reverse_lazy('DisplayAccountPage')

    def get_object(self, queryset = None):
        userObject = self.request.user
        userObject.birthdate = None if self.request.user.birthdate is None else datetime.strftime(self.request.user.birthdate, "%Y-%m-%d")
        return userObject

class UpdatePasswordPage(LoginRequiredMixin, PasswordChangeView):
    template_name = 'updatePasswordPage.html'
    success_url = reverse_lazy('UpdateAccountPage')

class UpdatePhotoPage(LoginRequiredMixin, UpdateView):
    template_name = 'updatePhotoPage.html'
    model = User
    form_class = UpdatePhotoForm
    success_url = reverse_lazy('UpdateAccountPage')

    def get_object(self, queryset = None):
        return self.request.user

class DeleteAccountPage(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('DisplayLoginPage')

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy('DisplayClientSide'))

    def get_object(self, queryset = None):
        return self.request.user
    

# Marc John Corral

class DisplayAllCBCTestResult(LoginRequiredMixin, View):
    template_name = 'displayAllCBCTestResult.html'
    model = User

    def get(self, request, *args, **kwargs):
        user = self.model.objects.get(id=request.user.id)
        object_list = user.cbctestresult_set.all()
        context = {'object_list': object_list}
        return render(request, self.template_name, context)

class DisplayCBCTestResult(LoginRequiredMixin, View):
    template_name = 'displayCBCTestResult.html'
    redirect_template_name = 'DisplayAllCBCTestResult'
    error_message = 'The record was not found.'
    model = User

    def get(self, request, pk, *args, **kwargs):
        user = self.model.objects.get(id=request.user.id)
        try:
            object = user.cbctestresult_set.get(id=pk)
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_template_name)
        
        if object == None:
            messages.error(request, self.error_message)
            return redirect(self.redirect_template_name)
        context = {'object': object}
        return render(request, self.template_name, context)

class DisplayAddingOptions(LoginRequiredMixin, View):
    template_name = 'displayAddingOptions.html'
    model = User
    
    def get(self, request,  *args, **kwargs):
        object = self.model.objects.get(id=request.user.id)
        context = {'object': object}
        return render(request, self.template_name, context)


class PaymentComplete(LoginRequiredMixin, View):
    redirect_template_name = 'PaymentMethod'
    error_message = 'Their something went wrong.'
    success_message = 'Payment Successful!'
    user_model = User
    promo_model = PromoOptions
    payment_model = Payments

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        
        try:
            promo = self.promo_model.objects.get(id=body['promoId'])
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_template_name)
        
        if object == None:
            messages.error(request, self.error_message)
            return redirect(self.redirect_template_name)
        
        user = self.user_model.objects.get(id=request.user.id)
        user.uploads = user.uploads + promo.uploads
        user.save()
        self.payment_model.objects.create( promo=promo, user=user)

        messages.success(request, self.success_message)
        return JsonResponse('Payment completed!', safe=False)

class PaymentMethod(LoginRequiredMixin, View):
    template_name = 'paymentMethod.html'
    redirect_template_name = 'DisplayAllCBCTestResult'
    error_message = 'The record was not found.'
    model = PromoOptions

    def get(self, request, type, pk, *args, **kwargs):
        try:
            object = self.model.objects.get(id=pk)
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_template_name)

        if type != 'pdf' and type != 'docx' and type != 'picture' and type != 'image' and type != 'pay':
            messages.error(request, self.error_message)
            return redirect(self.redirect_template_name)

        context = {'type': type, 'object': object}
        return render(request, self.template_name, context)

class DisplayAllPromoOptions(LoginRequiredMixin, View):
    template_name = 'promoOptions.html'
    redirect_results_template_name = 'DisplayAllCBCTestResult'
    redirect_pdf_template_name = 'UploadPDF'
    redirect_docx_template_name = 'UploadDocx'
    redirect_image_template_name = 'UploadImage'
    redirect_picture_template_name = 'CaptureImage'
    user_model = User
    promo_model = PromoOptions

    def get(self, request, type, *args, **kwargs):
        user = self.user_model.objects.get(id=request.user.id)
        if user.uploads <= 0 or type == 'pay':
            object_list = self.promo_model.objects.all()
            context = {'type': type, 'object_list': object_list}
            return render(request, self.template_name, context)
        elif type == 'pdf':
            return redirect(self.redirect_pdf_template_name)
        elif type == 'docx':
            return redirect(self.redirect_docx_template_name)
        elif type == 'picture':
            return redirect(self.redirect_picture_template_name)
        elif type == 'image':
            return redirect(self.redirect_image_template_name)
        else:
            messages.error(request, 'There was something wrong!')
            return redirect(self.redirect_results_template_name)

class UploadPDF(LoginRequiredMixin, View):
    template_name = 'uploadCBCTestResult.html'
    redirect_create_template_name = 'CreateCBCTestResult'
    redirect_promo_template_name = 'DisplayAllPromoOptions'
    error_message = 'You have no more uploads!'
    success_message = 'Upload PDF Successful!'
    user_model = User
    pdf_model = CBCTestResultPDF

    def post(self, request, *args, **kwargs):
        user = self.user_model.objects.get(id=request.user.id)
        if user.uploads != 0:
            user.uploads = user.uploads - 1
            user.save()
        object = self.pdf_model()
        object.set_testPDF(request.FILES.get('testPDF'))
        object.save()

        messages.success(request, self.success_message)

        return redirect(self.redirect_create_template_name, type = 'pdf', pk = object.pk)

    def get(self, request, *args, **kwargs):
        user = self.user_model.objects.get(id=request.user.id)
        if user.uploads <= 0:
            messages.error(request, self.error_message)
            return redirect(self.redirect_promo_template_name, type='pdf')
            
        context = {'type': 'pdf'}
        return render(request, self.template_name, context)

class UploadDocx(LoginRequiredMixin, View):
    template_name = 'uploadCBCTestResult.html'
    redirect_create_template_name = 'CreateCBCTestResult'
    redirect_promo_template_name = 'DisplayAllPromoOptions'
    error_message = 'You have no more uploads!'
    success_message = 'Upload Docx Successful!'
    user_model = User
    docx_model = CBCTestResultDocx

    def post(self, request, *args, **kwargs):
        user = self.user_model.objects.get(id=request.user.id)
        if user.uploads != 0:
            user.uploads = user.uploads - 1
            user.save()
        object = self.docx_model()
        object.set_testDocx(request.FILES.get('testDocx'))
        object.save()

        messages.success(request, self.success_message)

        return redirect(self.redirect_create_template_name, type = 'docx', pk = object.pk)

    def get(self, request, *args, **kwargs):
        user = self.user_model.objects.get(id=request.user.id)
        if user.uploads <= 0:
            messages.error(request, self.error_message)
            return redirect(self.redirect_promo_template_name, type='docx')

        context = {'type': 'docx'}
        return render(request, self.template_name, context)

class UploadImage(LoginRequiredMixin, View):
    template_name = 'uploadCBCTestResult.html'
    redirect_create_template_name = 'CreateCBCTestResult'
    redirect_promo_template_name = 'DisplayAllPromoOptions'
    error_message = 'You have no more uploads!'
    success_message = 'Upload Image Successful!'
    user_model = User
    image_model = CBCTestResultImage

    def post(self, request, *args, **kwargs):
        user = self.user_model.objects.get(id=request.user.id)
        if user.uploads != 0:
            user.uploads = user.uploads - 1
            user.save()
        object = self.image_model()
        object.set_testImage(request.FILES.get('testImage'))
        object.save()

        messages.success(request, self.success_message)

        return redirect(self.redirect_create_template_name, type = 'image', pk = object.pk)

    def get(self, request, *args, **kwargs):
        user = self.user_model.objects.get(id=request.user.id)
        if user.uploads <= 0:
            messages.error(request, self.error_message)
            return redirect(self.redirect_promo_template_name, type='image')

        context = {'type': 'image'}
        return render(request, self.template_name, context)

class CaptureImage(LoginRequiredMixin, View):
    template_name = 'captureImage.html'
    redirect_create_template_name = 'CreateCBCTestResult'
    redirect_promo_template_name = 'DisplayAllPromoOptions'
    error_message = 'You have no more uploads!'
    success_message = 'Capture Image Successful!'
    user_model = User
    image_model = CBCTestResultImage

    def post(self, request, *args, **kwargs):
        user = self.user_model.objects.get(id=request.user.id)
        if user.uploads != 0:
            user.uploads = user.uploads - 1
            user.save()
        image_path = request.POST["src"] 
        image = NamedTemporaryFile()
        image.write(urlopen(image_path).read())
        image.flush()
        image = File(image)
        name = str(image.name).split('\\')[-1]
        name += '.png' 
        image.name = name
        obj = self.image_model.objects.create() 
        obj.set_testImage(image)
        obj.save()

        messages.success(request, self.success_message)
        return redirect(self.redirect_create_template_name, pk = obj.pk, type = 'picture')
    
    def get(self, request, *args, **kwargs):
        user = self.user_model.objects.get(id=request.user.id)
        if user.uploads <= 0:
            messages.error(request, self.error_message)
            return redirect(self.redirect_promo_template_name, type='picture')

        return render(request, self.template_name)

class CreateCBCTestResult(LoginRequiredMixin, View):
    def post(self, request, type, pk, *args, **kwargs):
        object = CBCTestResult()
        if type == 'docx':
            try:
                object.set_testDocx(CBCTestResultDocx.objects.get(id=pk)) 
            except:
                messages.error(request, 'Their something went wrong.')
                return redirect('DisplayAddingOptions')
        elif type == 'pdf':
            try: 
                object.set_testPDF(CBCTestResultPDF.objects.get(id=pk))
            except:
                messages.error(request, 'Their something went wrong.')
                return redirect('DisplayAddingOptions')
        elif type == 'image' or type == 'picture':
            try:
                object.set_testImage(CBCTestResultImage.objects.get(id=pk))
            except:
                messages.error(request, 'Their something went wrong.')
                return redirect('DisplayAddingOptions')
        else:
            messages.error(request, 'There was something wrong!')
            return redirect('DisplayAddingOptions')

        date_time_str = request.POST.get('dateRequested')
        try:
            object.set_dateRequested(datetime.strptime(date_time_str, '%m-%d-%Y %H:%M %p')) 
        except:
            object.set_dateRequested(None)
        
        date_time_str = request.POST.get('dateReceived')
        try:
            object.set_dateReceived(datetime.strptime(date_time_str, '%m-%d-%Y %H:%M %p'))
        except:
            object.set_dateReceived(None)

        object.set_user(User.objects.get(id=request.user.id))
        object.set_source(request.POST.get('source')) 
        object.set_labNumber(request.POST.get('labNumber')) 
        object.set_pid(request.POST.get('pid')) 
        object.set_whiteBloodCells(request.POST.get('whiteBloodCells')) 
        object.set_redBloodCells(request.POST.get('redBloodCells')) 
        object.set_hemoglobin(request.POST.get('hemoglobin')) 
        object.set_hematocrit( request.POST.get('hematocrit')) 
        object.set_meanCorpuscularVolume(request.POST.get('meanCorpuscularVolume')) 
        object.set_meanCorpuscularHb(request.POST.get('meanCorpuscularHb')) 
        object.set_meanCorpuscularHbConc(request.POST.get('meanCorpuscularHbConc')) 
        object.set_rbcDistributionWidth(request.POST.get('rbcDistributionWidth')) 
        object.set_plateletCount(request.POST.get('plateletCount')) 
        object.set_segmenters(request.POST.get('segmenters')) 
        object.set_lymphocytes(request.POST.get('lymphocytes')) 
        object.set_monocytes(request.POST.get('monocytes')) 
        object.set_eosinophils(request.POST.get('eosinophils')) 
        object.set_basophils(request.POST.get('basophils')) 
        object.set_bands(request.POST.get('bands')) 
        object.set_absoluteSeg(request.POST.get('absoluteSeg')) 
        object.set_absoluteLymphocyteCount(request.POST.get('absoluteLymphocyteCount')) 
        object.set_absoluteMonocyteCount(request.POST.get('absoluteMonocyteCount')) 
        object.set_absoluteEosinophilCount(request.POST.get('absoluteEosinophilCount')) 
        object.set_absoluteBasophilCount(request.POST.get('absoluteBasophilCount')) 
        object.set_absoluteBandCount(request.POST.get('absoluteBandCount')) 
        object.save()

        messages.success(request, 'Create CBC Test Result Successful!')

        return redirect('DisplayCBCTestResult', pk=object.pk)

    def get(self, request, type, pk, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        data = {}
        if type == 'docx':
            try:
                docxObject = CBCTestResultDocx.objects.get(id=pk)
                data['object'] = docxObject
                FILE_PATH = str(docxObject.get_testDocx().url[1:])
                txt = d2t.process(FILE_PATH)

                numericalValues = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", txt)
                values = re.split('\s+',txt)
                data['source'] = values[15] + " " + values[16] + " " + values[17] 
                data['labNumber'] = values[29] 
                data['pid'] = values[7]
                data['dateRequested'] = values[23] + " " + values[24] + " " + values[25]
                data['dateReceived'] = values[43] + " " + values[44] + " " + values[45] 
                data['whiteBloodCells'] = numericalValues[18] 
                data['redBloodCells'] = numericalValues[23] 
                data['hemoglobin'] = numericalValues[28] 
                data['hematocrit'] = numericalValues[31] 
                data['meanCorpuscularVolume'] = numericalValues[34] 
                data['meanCorpuscularHb'] = numericalValues[37] 
                data['meanCorpuscularHbConc'] = numericalValues[40] 
                data['rbcDistributionWidth'] = numericalValues[43] 
                data['plateletCount'] = numericalValues[46] 
                data['segmenters'] = numericalValues[51] 
                data['lymphocytes'] = numericalValues[54] 
                data['monocytes'] = numericalValues[57] 
                data['eosinophils'] = numericalValues[60] 
                data['basophils'] = numericalValues[63] 
                data['bands'] = numericalValues[66] 
                data['absoluteSeg'] = numericalValues[69] 
                data['absoluteLymphocyteCount'] = numericalValues[74] 
                data['absoluteMonocyteCount'] = numericalValues[79] 
                data['absoluteEosinophilCount'] = numericalValues[83] 
                data['absoluteBasophilCount'] = numericalValues[87] 
                data['absoluteBandCount'] = numericalValues[91]

                if data['source'] == None or data['labNumber'] == None or data['pid'] == None: 
                    os.remove(str(docxObject.get_testDocx().url)[1:]) 

                    messages.error(request, 'There was something wrong with your document or you uploaded the wrong document. Please try another one!')
                    user.uploads = user.uploads + 1
                    user.save()
                    
                    return redirect('UploadPDF')
            except:
                if docxObject != None: 
                    os.remove(str(docxObject.get_testDocx().url)[1:]) 
                messages.error(request, 'There was something wrong with your document. Please try another one!')
                user.uploads = user.uploads + 1
                user.save()
                return redirect('UploadDocx')
        elif type == 'pdf':
            try:
                pdfObject = CBCTestResultPDF.objects.get(id=pk)
                data['object'] = pdfObject
                FILE_PATH = str(pdfObject.get_testPDF().url[1:])

                with open(FILE_PATH, mode='rb') as f:
                    reader = PyPDF4.PdfFileReader(f)
                    page = reader.getPage(0)
                    txt = page.extractText()

                numericalValues = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", txt)
                values = re.split("\n",txt)
                data['source'] = values[35] + values[36] + values[37]
                data['labNumber'] = numericalValues[7] 
                data['pid'] = values[16] + values[17]
                data['dateRequested'] = values[47] + values[48] + values[49] + values[50] + values[51]
                data['dateReceived'] = values[85] + values[86] + values[87] + values[88] + values[89]
                data['whiteBloodCells'] = numericalValues[18] 
                data['redBloodCells'] = numericalValues[23] 
                data['hemoglobin'] = numericalValues[28] 
                data['hematocrit'] = numericalValues[31] 
                data['meanCorpuscularVolume'] = numericalValues[34] 
                data['meanCorpuscularHb'] = numericalValues[37] 
                data['meanCorpuscularHbConc'] = numericalValues[40] 
                data['rbcDistributionWidth'] = numericalValues[43] 
                data['plateletCount'] = numericalValues[46] 
                data['segmenters'] = numericalValues[51] 
                data['lymphocytes'] = numericalValues[54] 
                data['monocytes'] = numericalValues[57] 
                data['eosinophils'] = numericalValues[60] 
                data['basophils'] = numericalValues[63] 
                data['bands'] = numericalValues[66] 
                data['absoluteSeg'] = numericalValues[69] 
                data['absoluteLymphocyteCount'] = numericalValues[74] 
                data['absoluteMonocyteCount'] = numericalValues[79] 
                data['absoluteEosinophilCount'] = numericalValues[83] 
                data['absoluteBasophilCount'] = numericalValues[87] 
                data['absoluteBandCount'] = numericalValues[91]

                if data['source'] == None or data['labNumber'] == None or data['pid'] == None: 
                    os.remove(str(pdfObject.get_testPDF().url)[1:]) 

                    messages.error(request, 'There was something wrong with your pdf or you uploaded the wrong pdf. Please try another one!')
                    user.uploads = user.uploads + 1
                    user.save()
                    
                    return redirect('UploadPDF')
            except:
                if pdfObject != None: 
                    os.remove(str(pdfObject.get_testPDF().url)[1:]) 
                messages.error(request, 'There was something wrong with your pdf. Please try another one!')
                user.uploads = user.uploads + 1
                user.save()
                return redirect('UploadPDF')
        elif type == 'image' or type == 'picture':
            try:

                imgObject = CBCTestResultImage.objects.get(id=pk)
                data['object'] = imgObject
               
            except:
                if imgObject != None: 
                    os.remove(str(imgObject.get_testImage().url)[1:]) 
                messages.error(request, 'There was something wrong with your image. Please try another one!')
                user.uploads = user.uploads + 1
                user.save()
                if type == 'image':
                    return redirect('UploadImage')
                elif type == 'picture':
                    return redirect('CaptureImage')
        else:
            messages.error(request, 'There was something wrong!')
            return redirect('DisplayAddingOptions')

        data['type'] = type

        return render(request, 'createCBCTestResult.html', data)



class UpdateCBCTestResult(LoginRequiredMixin, View):
    template_name = 'updateCBCTestResult.html'
    redirect_results_template_name = 'DisplayAllCBCTestResult'
    redirect_result_template_name = 'DisplayCBCTestResult'
    error_message = 'The record was not found.'
    succes_message = 'Update CBC Test Result Successful!'
    model = CBCTestResult

    def post(self, request, pk, *args, **kwargs):
        try:
            object = self.model.objects.get(id=pk)
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_results_template_name)

        if object != None:
            object.set_whiteBloodCells(request.POST.get('whiteBloodCells')) 
            object.set_redBloodCells(request.POST.get('redBloodCells')) 
            object.set_hemoglobin(request.POST.get('hemoglobin')) 
            object.set_hematocrit( request.POST.get('hematocrit')) 
            object.set_meanCorpuscularVolume(request.POST.get('meanCorpuscularVolume')) 
            object.set_meanCorpuscularHb(request.POST.get('meanCorpuscularHb')) 
            object.set_meanCorpuscularHbConc(request.POST.get('meanCorpuscularHbConc')) 
            object.set_rbcDistributionWidth(request.POST.get('rbcDistributionWidth')) 
            object.set_plateletCount(request.POST.get('plateletCount')) 
            object.set_segmenters(request.POST.get('segmenters')) 
            object.set_lymphocytes(request.POST.get('lymphocytes')) 
            object.set_monocytes(request.POST.get('monocytes')) 
            object.set_eosinophils(request.POST.get('eosinophils')) 
            object.set_basophils(request.POST.get('basophils')) 
            object.set_bands(request.POST.get('bands')) 
            object.set_absoluteSeg(request.POST.get('absoluteSeg')) 
            object.set_absoluteLymphocyteCount(request.POST.get('absoluteLymphocyteCount')) 
            object.set_absoluteMonocyteCount(request.POST.get('absoluteMonocyteCount')) 
            object.set_absoluteEosinophilCount(request.POST.get('absoluteEosinophilCount')) 
            object.set_absoluteBasophilCount(request.POST.get('absoluteBasophilCount')) 
            object.set_absoluteBandCount(request.POST.get('absoluteBandCount')) 
            object.save()

            messages.success(request, self.succes_message)
            return redirect(self.redirect_result_template_name, pk=pk)
        elif object == None:
            messages.error(request, self.error_message)
            return redirect(self.redirect_results_template_name)
            

        context = {'object': object}
        return render(request, self.template_name, context)

    def get(self, request, pk, *args, **kwargs):
        try:
            object = self.model.objects.get(id=pk)
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_results_template_name)
        
        if object == None:
            messages.error(request, self.error_message)
            return redirect(self.redirect_results_template_name)
        context = {'object': object}
        return render(request, self.template_name, context)

class DeleteCBCTestResult(LoginRequiredMixin, View):
    template_name = 'deleteCBCTestResult.html'
    redirect_template_name = 'DisplayAllCBCTestResult'
    error_message = 'The record was not found.'
    success_message = 'Delete CBC Test Result Successful!'
    model = CBCTestResult

    def post(self, request, pk, *args, **kwargs):
        try:
            object = self.model.objects.get(id=pk)
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_template_name)

        if object != None:
            object.delete()

            if object.get_testPDF() != None:
                os.remove(str(object.get_testPDF().get_testPDF().url)[1:]) 
            elif object.get_testDocx() != None:
                os.remove(str(object.get_testDocx().get_testDocx().url)[1:]) 
            elif object.get_testImage() != None:
                os.remove(str(object.get_testImage().get_testImage().url)[1:]) 

            messages.success(request, self.success_message)

            return redirect(self.redirect_template_name)
        elif object == None:
            messages.error(request, self.error_message)
            return redirect(self.redirect_template_name)

        context = {'object': object, 'type': 'record'}
        return render(request, self.template_name, context)

    def get(self, request, pk, *args, **kwargs):
        try:
            object = self.model.objects.get(id=pk)
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_template_name)

        if object == None:
            messages.error(request, self.error_message)
            return redirect(self.redirect_template_name)

        context = {'object': object, 'type': 'record'}
        return render(request, self.template_name, context)

class DeleteUploadedImage(LoginRequiredMixin, View):
    template_name = 'deleteCBCTestResult.html'
    redirect_adding_template_name = 'DisplayAddingOptions'
    redirect_upload_template_name = 'UploadImage'
    error_message = 'The image was not found.'
    success_message = 'Delete Image Successful!'
    image_model = CBCTestResultImage
    user_model = User

    def post(self, request, pk, *args, **kwargs):
        try:
            object = self.image_model.objects.get(id=pk)
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_adding_template_name)
        
        if object != None:
            object.delete()
            os.remove(str(object.get_testImage().url)[1:]) 
            user = self.user_model.objects.get(id=request.user.id)
            user.uploads = user.uploads + 1
            user.save()

            messages.success(request, self.success_message)

            return redirect(self.redirect_upload_template_name)
        elif object == None:
            messages.error(request, self.error_message)
            return redirect(self.redirect_adding_template_name)
        
        context = {'object': object, 'type': 'image'}
        return render(request, self.template_name, context)

    def get(self, request, pk, *args, **kwargs):
        try:
            object = self.image_model.objects.get(id=pk)
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_adding_template_name)

        if object == None:
            messages.error(request, self.error_message)
            return redirect(self.redirect_adding_template_name)

        context = {'object': object, 'type': 'image'}
        return render(request, self.template_name, context)
    
class DeleteCapturedImage(LoginRequiredMixin, View):
    template_name = 'deleteCBCTestResult.html'
    redirect_adding_template_name = 'DisplayAddingOptions'
    redirect_upload_template_name = 'CaptureImage'
    error_message = 'The image was not found.'
    success_message = 'Delete Image Successful!'
    image_model = CBCTestResultImage
    user_model = User

    def post(self, request, pk, *args, **kwargs):
        try:
            object = self.image_model.objects.get(id=pk)
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_adding_template_name)

        if object != None:
            object.delete()
            os.remove(str(object.get_testImage().url)[1:]) 
            user = self.user_model.objects.get(id=request.user.id)
            user.uploads = user.uploads + 1
            user.save()

            messages.success(request, self.success_message)

            return redirect(self.redirect_upload_template_name)
        elif object == None:
            messages.error(request, self.error_message)
            return redirect(self.redirect_adding_template_name)
        
        context = {'object': object, 'type': 'picture'}
        return render(request, self.template_name, context)

    def get(self, request, pk, *args, **kwargs):
        try:
            object = self.image_model.objects.get(id=pk)
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_adding_template_name)

        if object == None:
            messages.error(request, self.error_message)
            return redirect(self.redirect_adding_template_name)

        context = {'object': object, 'type': 'picture'}
        return render(request,  self.template_name, context)

class DeletePDF(LoginRequiredMixin, View):
    template_name = 'deleteCBCTestResult.html'
    redirect_adding_template_name = 'DisplayAddingOptions'
    redirect_upload_template_name = 'UploadPDF'
    error_message = 'The pdf was not found.'
    success_message = 'Delete PDF Successful!'
    pdf_model = CBCTestResultPDF
    user_model = User

    def post(self, request, pk, *args, **kwargs):
        try:
            object = self.pdf_model.objects.get(id=pk)
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_adding_template_name)

        if object != None:
            object.delete()
            os.remove(str(object.get_testPDF().url)[1:]) 
            user = self.user_model.objects.get(id=request.user.id)
            user.uploads = user.uploads + 1
            user.save()

            messages.success(request, self.success_message)

            return redirect(self.redirect_upload_template_name)
        elif object == None:
            messages.error(request, self.error_message)
            return redirect(self.redirect_adding_template_name)

        context = {'object': object, 'type': 'pdf'}
        return render(request, self.template_name, context)

    def get(self, request, pk, *args, **kwargs):
        try:
            object = self.pdf_model.objects.get(id=pk)
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_adding_template_name)

        if object == None:
            messages.error(request, self.error_message)
            return redirect(self.redirect_adding_template_name)

        context = {'object': object, 'type': 'pdf'}
        return render(request, self.template_name, context)

class DeleteDocx(LoginRequiredMixin, View):
    template_name = 'deleteCBCTestResult.html'
    redirect_adding_template_name = 'DisplayAddingOptions'
    redirect_upload_template_name = 'UploadDocx'
    error_message = 'The document was not found.'
    success_message = 'Delete Docx Successful!'
    docx_model = CBCTestResultDocx
    user_model = User

    def post(self, request, pk, *args, **kwargs):
        try:
            object = self.docx_model.objects.get(id=pk)
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_adding_template_name)

        if object != None:
            object.delete()
            os.remove(str(object.get_testDocx().url)[1:]) 
            user = self.user_model.objects.get(id=request.user.id)
            user.uploads = user.uploads + 1
            user.save()

            messages.success(request, self.success_message)

            return redirect(self.redirect_upload_template_name)
        elif object == None:
            messages.error(request, self.error_message)
            return redirect(self.redirect_adding_template_name)
        
        context = {'object': object, 'type': 'docx'}
        return render(request, self.template_name, context)

    def get(self, request, pk, *args, **kwargs):
        try:
            object = CBCTestResultDocx.objects.get(id=pk)
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_adding_template_name)

        if object == None:
            messages.error(request, self.error_message)
            return redirect(self.redirect_adding_template_name)

        context = {'object': object, 'type': 'docx'}
        return render(request, self.template_name, context)

class ShowRoom(LoginRequiredMixin, View):
    redirect_contacts_template_name = 'contacts'
    redirect_chat_template_name = 'newChat'
    model = User

    def get(self, request, *args, **kwargs):
        user = self.model.objects.get(id=request.user.id)
        if user.is_superuser:
            return redirect(self.redirect_contacts_template_name)
        else:
            return redirect(self.redirect_chat_template_name)

class NewChat(LoginRequiredMixin, View):
    template_name = 'newChat.html'
    redirect_template_name = 'chatbox'
    user_model = User
    room_model = Room

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user = self.user_model.objects.get(id=request.user.id)
        if user.room_set.first():
            room = user.room_set.first()
            return redirect(self.redirect_template_name, pk = room.get_id())
        else:
            new_room = self.room_model.objects.create()
            new_room.set_owner(user)
            new_room.save()
            return redirect(self.redirect_template_name, pk =new_room.get_id())

class ChatBox(LoginRequiredMixin, View):
    template_name = 'chatbox.html'
    redirect_template_name = 'showRoom'
    error_message = 'Something went wrong.'
    user_model = User
    room_model = Room

    def get(self, request, pk,  *args, **kwargs):
        try:
            room_details = self.room_model.objects.get(id=pk)
            user = self.user_model.objects.get(id=request.user.id)
            room_details.message_set.filter(~Q(user__username=user.username)&Q(read=False)).update(read=True)
            return render(request, self.template_name, {
                'room_details': room_details
            })
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_template_name)

class Contacts(LoginRequiredMixin, View):
    template_name = 'contacts.html'
    user_model = User
    room_model = Room

    def get(self, request, *args, **kwargs):
        user = self.user_model.objects.get(id=request.user.id)
        rooms = self.room_model.objects.filter(~Q(owner__username=user.username))
        return render(request, self.template_name, {'rooms': rooms})

class GetContactNotifications(LoginRequiredMixin, View):
    user_model = User
    room_model = Room
    admin_name = 'admin'

    def get(self, request, *args, **kwargs):
        context = {}
        user = self.user_model.objects.get(id=request.user.id)
        if user.is_superuser:
            rooms = self.room_model.objects.filter(~Q(owner__username=user.username))
            i = 0
            for room in rooms:
                count = room.message_set.filter(~Q(user__username=user.username)&Q(read=False)).count()
                i += 1
                context[str(i)] = [room.get_owner().username, count, room.get_id()]
        else:
            if user.room_set.first():
                room = user.room_set.first()
                count = room.message_set.filter(~Q(user__username=user.username)&Q(read=False)).count()
                context['0'] = [self.admin_name, count]

        return JsonResponse({"messages":context})      

class Send(LoginRequiredMixin, View):
    user_model = User
    room_model = Room
    message_model = Message

    def post(self, request, *args, **kwargs):
        message = request.POST.get('message')
        user = self.user_model.objects.get(id=request.user.id)
        room_id = request.POST.get('room_id')
        room = self.room_model.objects.get(id=room_id)
        new_message = self.message_model.objects.create(value=message, user=user, room=room)
        new_message.save()
        
        return HttpResponse('Message sent successfully')

class GetMessages(LoginRequiredMixin, View):
    redirect_template_name = 'showRoom'
    error_message = 'Something went wrong.'
    user_model = User
    room_model = Room

    def get(self, request, pk, *args, **kwargs):
        try:
            room = self.room_model.objects.get(id=pk)
            messages = room.message_set.all()
            user = self.user_model.objects.get(id=request.user.id)
            room.message_set.filter(~Q(user__username=user.username)&Q(read=False)).update(read=True)
            username = user.username
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_template_name)
        return JsonResponse({"messages":list(messages.values('user__username', 'value', 'date', 'read', 'id')), "username": username})

class DeleteMessage(LoginRequiredMixin, View):
    redirect_chat_template_name = 'chatbox'
    redirect_room_template_name = 'showRoom'
    error_message = 'Something went wrong.'
    message_model = Message
    
    def get(self, request, pk, *args, **kwargs):
        try:
            message = Message.objects.get(id=pk)

            if message.user.id == request.user.id:
                message.delete()
            
            return redirect(self.redirect_chat_template_name, pk =message.room.get_id())
        except:
            messages.error(request, self.error_message)
            return redirect(self.redirect_room_template_name)
        
        

# Marc John Corral