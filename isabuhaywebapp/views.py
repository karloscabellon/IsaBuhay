import cv2
import numpy as np
import pytesseract
import re
import PyPDF4
import docx2txt as d2t
from urllib.request import urlopen
from django.contrib.auth import logout
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

class DisplayLandingPage(TemplateView):
    template_name = 'displayLandingPage.html'

class CreateAccountPage(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'createAccountPage.html'
    success_url = reverse_lazy('DisplayLoginPage')

class DisplayLoginPage(LoginView):
    template_name = 'loginPage.html'
    next_page = 'DisplayClientSide'

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)

class DisplayClientSide(LoginRequiredMixin, TemplateView):
    template_name = 'displayClientSide.html'

class DisplayAccountPage(TemplateView):
    template_name = 'displayAccountPage.html'

class UpdateAccountPage(TemplateView):
    template_name = 'updateAccountPage.html'

class DeleteAccountPage(TemplateView):
    template_name = 'deleteAccountPage.html'

# Marc John Corral

class PaymentComplete(View):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        promo = PromoOptions.objects.get(id=body['promoId'])
        Payments.objects.create(
            promo=promo
            )
        return JsonResponse('Payment completed!', safe=False)

class DisplayAllCBCTestResult(ListView):
    model = CBCTestResult
    ordering = ['-dateRequested']
    template_name = 'displayAllCBCTestResult.html'

class DisplayCBCTestResult(DetailView):
    model = CBCTestResult
    template_name = 'displayCBCTestResult.html'

class DisplayAddingOptions(TemplateView):
    template_name = 'DisplayAddingOptions.html'

class PaymentMethod(View):
    def get(self, request, type, pk, *args, **kwargs):
        object = PromoOptions.objects.get(id=pk)
        context = {'type': type, 'object': object}
        return render(request, 'paymentMethod.html', context)

class DisplayAllPromoOptions(View):
    def get(self, request, type, *args, **kwargs):
        object_list = PromoOptions.objects.all()
        context = {'type': type, 'object_list': object_list}
        return render(request, 'promoOptions.html', context)

class UploadPDF(View):
    def post(self, request, *args, **kwargs):
        object = CBCTestResultPDF()
        object.testPDF = request.FILES.get('testPDF')
        object.save()
        return redirect('CreateCBCTestResult', type = 'pdf', pk = object.pk)

    def get(self, request, *args, **kwargs):
        context = {'type': 'pdf'}
        return render(request, 'uploadCBCTestResult.html', context)

class UploadDocx(CreateView):
    model = CBCTestResultDocx
    form_class = CBCTestResultDocxForm
    template_name = 'uploadCBCTestResult.html'

    def get_context_data(self, **kwargs):
        context = super(UploadDocx, self).get_context_data(**kwargs)
        context['type'] = 'docx'
        return context

class UploadImage(View):
    def post(self, request, *args, **kwargs):
        object = CBCTestResultImage()
        object.testImage = request.FILES.get('testImage')
        object.save()
        return redirect('CreateCBCTestResult', type = 'image', pk = object.pk)

    def get(self, request, *args, **kwargs):
        context = {'type': 'image'}
        return render(request, 'uploadCBCTestResult.html', context)

class CaptureImage(TemplateView):
    template_name = 'captureImage.html'

    def post(self, request, *args, **kwargs):
        image_path = request.POST["src"] 
        image = NamedTemporaryFile()
        image.write(urlopen(image_path).read())
        image.flush()
        image = File(image)
        name = str(image.name).split('\\')[-1]
        name += '.png' 
        image.name = name
        obj = CBCTestResultImage.objects.create(testImage=image) 
        obj.save()
        return redirect('CreateCBCTestResult', pk = obj.pk, type = 'picture')


class CreateCBCTestResult(View):
    def post(self, request, type, pk, *args, **kwargs):
        object = CBCTestResult()
        if type == 'docx':
            object.testDocx = CBCTestResultDocx.objects.get(id=pk)
        elif type == 'pdf':
            object.testPDF = CBCTestResultPDF.objects.get(id=pk)
        elif type == 'image' or type == 'picture':
            object.testImage = CBCTestResultImage.objects.get(id=pk)

        date_time_str = request.POST.get('dateRequested')
        try:
            object.dateRequested = datetime.strptime(date_time_str, '%m-%d-%Y %H:%M %p')
        except:
            object.dateRequested = None
        
        date_time_str = request.POST.get('dateReceived')
        try:
            object.dateReceived = datetime.strptime(date_time_str, '%m-%d-%Y %H:%M %p')
        except:
            object.dateReceived = None

        object.source = request.POST.get('source')
        object.labNumber = request.POST.get('labNumber')
        object.pid = request.POST.get('pid')
        object.whiteBloodCells = request.POST.get('whiteBloodCells')
        object.redBloodCells = request.POST.get('redBloodCells')
        object.hemoglobin = request.POST.get('hemoglobin')
        object.hematocrit = request.POST.get('hematocrit')
        object.meanCorpuscularVolume = request.POST.get('meanCorpuscularVolume')
        object.meanCorpuscularHb = request.POST.get('meanCorpuscularHb')
        object.meanCorpuscularHbConc = request.POST.get('meanCorpuscularHbConc')
        object.rbcDistributionWidth = request.POST.get('rbcDistributionWidth')
        object.plateletCount = request.POST.get('plateletCount')
        object.segmenters = request.POST.get('segmenters')
        object.lymphocytes = request.POST.get('lymphocytes')
        object.monocytes = request.POST.get('monocytes')
        object.eosinophils = request.POST.get('eosinophils')
        object.basophils = request.POST.get('basophils')
        object.bands = request.POST.get('bands')
        object.absoluteSeg = request.POST.get('absoluteSeg')
        object.absoluteLymphocyteCount = request.POST.get('absoluteLymphocyteCount')
        object.absoluteMonocyteCount = request.POST.get('absoluteMonocyteCount')
        object.absoluteEosinophilCount = request.POST.get('absoluteEosinophilCount')
        object.absoluteBasophilCount = request.POST.get('absoluteBasophilCount')
        object.absoluteBandCount = request.POST.get('absoluteBandCount')
        object.save()
        return redirect('DisplayCBCTestResult', pk=object.pk)

    def get(self, request, type, pk, *args, **kwargs):
        data = {'type': type}
        if type == 'docx':
            docxObject = CBCTestResultDocx.objects.get(id=pk)
            data['object'] = docxObject
            FILE_PATH = 'D:\\WEB Development Projects\\DJANGO PROJECTS\\repo\\IsaBuhay'+str(docxObject.testDocx.url)
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
        elif type == 'pdf':
            pdfObject = CBCTestResultPDF.objects.get(id=pk)
            data['object'] = pdfObject
            FILE_PATH = 'D:\\WEB Development Projects\\DJANGO PROJECTS\\repo\\IsaBuhay'+str(pdfObject.testPDF.url)

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
        elif type == 'image' or type == 'picture':
            roi = [ [(250, 235), (837, 293), 'text', 'source'],
                [(1193, 89), (1500, 144), 'text', 'labNumber'], 
                [(253, 143), (590, 190), 'text', 'pid'], 
                [(376, 374), (739, 425), 'text', 'dateRequested'],
                [(1158,381), (1512, 434), 'text', 'dateReceived'],
                [(645, 675), (803, 730), 'float', 'whiteBloodCells'], 
                [(645, 735), (803, 790), 'float', 'redBloodCells'], 
                [(645, 795), (803, 850), 'float', 'hemoglobin'], 
                [(645, 855), (803, 910), 'float', 'hematocrit'], 
                [(645, 915), (803, 970), 'float', 'meanCorpuscularVolume'], 
                [(645, 973), (803, 1028), 'float', 'meanCorpuscularHb'], 
                [(645, 1034), (803, 1089), 'float', 'meanCorpuscularHbConc'], 
                [(645, 1093), (803, 1146), 'float', 'rbcDistributionWidth'], 
                [(645, 1153), (803, 1208), 'float', 'plateletCount'], 
                [(645, 1270), (803, 1327), 'float', 'segmenters'], 
                [(645, 1327), (803, 1384), 'float', 'lymphocytes'], 
                [(645, 1386), (803, 1443), 'float', 'monocytes'], 
                [(645, 1445), (803, 1505), 'float', 'eosinophils'], 
                [(645, 1506), (803, 1560), 'float', 'basophils'], 
                [(645, 1562), (803, 1619), 'float', 'bands'], 
                [(645, 1684), (803, 1741), 'float', 'absoluteSeg'], 
                [(645, 1743), (803, 1800), 'float', 'absoluteLymphocyteCount'], 
                [(645, 1802), (803, 1863), 'float', 'absoluteMonocyteCount'], 
                [(645, 1860), (803, 1919), 'float', 'absoluteEosinophilCount'], 
                [(645, 1920), (803, 1978), 'float', 'absoluteBasophilCount'], 
                [(645, 1978), (803, 2036), 'float', 'absoluteBandCount']
            ]

            def grayscale(image):
                return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            per = 25
            pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
            
            imgQ = cv2.imread('D:\\WEB Development Projects\\DJANGO PROJECTS\\repo\\IsaBuhay\\imageQuery\\sample.png')
            h,w,c = imgQ.shape
            gray_image = grayscale(imgQ)
            thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)

            orb = cv2.ORB_create(1000)
            kp1, des1 = orb.detectAndCompute(im_bw, None)

            imgObject = CBCTestResultImage.objects.get(id=pk)
            data['object'] = imgObject
            img = cv2.imread('D:\\WEB Development Projects\\DJANGO PROJECTS\\repo\\IsaBuhay'+str(imgObject.testImage.url))
            gray_image = grayscale(img)
            thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
            kp2, des2 = orb.detectAndCompute(im_bw, None)
            bf = cv2.BFMatcher(cv2.NORM_HAMMING)
            matches = bf.match(des2, des1)
            list(matches).sort(key= lambda x: x.distance)
            good = matches[:int(len(matches) * (per/100))]

            srcPoints = np.float32([kp2[m.queryIdx].pt for m in good]).reshape(-1,1,2)
            dstPoints = np.float32([kp1[m.trainIdx].pt for m in good]).reshape(-1,1,2)

            M, _ = cv2.findHomography(srcPoints, dstPoints, cv2.RANSAC, 5.0)
            imgScan = cv2.warpPerspective(img, M, (w,h))
            imgShow = imgScan.copy()
            imgMask = np.zeros_like(imgShow)

            for x, r in enumerate(roi):
                cv2.rectangle(imgMask, (r[0][0], r[0][1]), (r[1][0], r[1][1]), (0, 255, 0), cv2.FILLED)
                imgShow = cv2.addWeighted(imgShow, 0.99, imgMask, 0.1, 0)
                imgCrop = imgScan[r[0][1]:r[1][1], r[0][0]:r[1][0]]

                if r[2] == 'float':
                    text = pytesseract.image_to_string(imgCrop)
                    value = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", text)
                    if len(value) != 0:
                        data[r[3]] = float(value[0])
                    else:
                        data[r[3]] = None
                elif r[2] == 'text':
                    text = pytesseract.image_to_string(imgCrop)
                    newText = re.sub(r"[^a-zA-Z0-9-(): ]","",text)
                    if newText != '':
                        data[r[3]] = newText
                    else:
                        data[r[3]] = None

        return render(request, 'createCBCTestResult.html', data)



class UpdateCBCTestResult(View):
    def post(self, request, pk, *args, **kwargs):
        object = CBCTestResult.objects.get(id=pk)
        if object != None:
            object.whiteBloodCells = request.POST.get('whiteBloodCells')
            object.redBloodCells = request.POST.get('redBloodCells')
            object.hemoglobin = request.POST.get('hemoglobin')
            object.hematocrit = request.POST.get('hematocrit')
            object.meanCorpuscularVolume = request.POST.get('meanCorpuscularVolume')
            object.meanCorpuscularHb = request.POST.get('meanCorpuscularHb')
            object.meanCorpuscularHbConc = request.POST.get('meanCorpuscularHbConc')
            object.rbcDistributionWidth = request.POST.get('rbcDistributionWidth')
            object.plateletCount = request.POST.get('plateletCount')
            object.segmenters = request.POST.get('segmenters')
            object.lymphocytes = request.POST.get('lymphocytes')
            object.monocytes = request.POST.get('monocytes')
            object.eosinophils = request.POST.get('eosinophils')
            object.basophils = request.POST.get('basophils')
            object.bands = request.POST.get('bands')
            object.absoluteSeg = request.POST.get('absoluteSeg')
            object.absoluteLymphocyteCount = request.POST.get('absoluteLymphocyteCount')
            object.absoluteMonocyteCount = request.POST.get('absoluteMonocyteCount')
            object.absoluteEosinophilCount = request.POST.get('absoluteEosinophilCount')
            object.absoluteBasophilCount = request.POST.get('absoluteBasophilCount')
            object.absoluteBandCount = request.POST.get('absoluteBandCount')
            object.save()
            return redirect('DisplayCBCTestResult', pk=pk)
        context = {'object': object}
        return render(request, 'updateCBCTestResult.html', context)

    def get(self, request, pk, *args, **kwargs):
        object = CBCTestResult.objects.get(id=pk)
        context = {'object': object}
        return render(request, 'updateCBCTestResult.html', context)

class DeleteCBCTestResult(View):
    def post(self, request, pk, *args, **kwargs):
        object = CBCTestResult.objects.get(id=pk)
        if object != None:
            object.delete()

            if object.testPDF != None:
                os.remove('D:\\WEB Development Projects\\DJANGO PROJECTS\\repo\\IsaBuhay'+str(object.testPDF.url)) 
            elif object.testDocx != None:
                os.remove('D:\\WEB Development Projects\\DJANGO PROJECTS\\repo\\IsaBuhay'+str(object.testDocx.url)) 
            elif object.testImage != None:
                os.remove('D:\\WEB Development Projects\\DJANGO PROJECTS\\repo\\IsaBuhay'+str(object.testImage.url)) 

            return redirect('DisplayAllCBCTestResult')

        context = {'object': object}
        return render(request, 'deleteCBCTestResult.html', context)

    def get(self, request, pk, *args, **kwargs):
        object = CBCTestResult.objects.get(id=pk)
        context = {'object': object}
        return render(request, 'deleteCBCTestResult.html', context)

class DeleteUploadedImage(View):
    def post(self, request, pk, *args, **kwargs):
        object = CBCTestResultImage.objects.get(id=pk)
        if object != None:
            object.delete()
            os.remove('D:\\WEB Development Projects\\DJANGO PROJECTS\\repo\\IsaBuhay'+str(object.testImage.url)) 
            return redirect('UploadImage')
        context = {'object': object}
        return render(request, 'deleteCBCTestResult.html', context)

    def get(self, request, pk, *args, **kwargs):
        object = CBCTestResultImage.objects.get(id=pk)
        context = {'object': object, 'type': 'image'}
        return render(request, 'deleteCBCTestResult.html', context)
    
class DeleteCapturedImage(DeleteView):
    model = CBCTestResultImage
    template_name = 'deleteCBCTestResult.html'
    success_url = reverse_lazy('CaptureImage')

    def get_context_data(self, **kwargs):
        context = super(DeleteCapturedImage, self).get_context_data(**kwargs)
        context['type'] = 'picture'
        return context

class DeletePDF(DeleteView):
    def post(self, request, pk, *args, **kwargs):
        object = CBCTestResultPDF.objects.get(id=pk)
        if object != None:
            object.delete()
            os.remove('D:\\WEB Development Projects\\DJANGO PROJECTS\\repo\\IsaBuhay'+str(object.testPDF.url)) 
            return redirect('UploadPDF')
        context = {'object': object}
        return render(request, 'deleteCBCTestResult.html', context)

    def get(self, request, pk, *args, **kwargs):
        object = CBCTestResultPDF.objects.get(id=pk)
        context = {'object': object, 'type': 'pdf'}
        return render(request, 'deleteCBCTestResult.html', context)

class DeleteDocx(DeleteView):
    def post(self, request, pk, *args, **kwargs):
        object = CBCTestResultDocx.objects.get(id=pk)
        if object != None:
            object.delete()
            os.remove('D:\\WEB Development Projects\\DJANGO PROJECTS\\repo\\IsaBuhay'+str(object.testDocx.url)) 
            return redirect('UploadDocx')
        context = {'object': object}
        return render(request, 'deleteCBCTestResult.html', context)

    def get(self, request, pk, *args, **kwargs):
        object = CBCTestResultDocx.objects.get(id=pk)
        context = {'object': object, 'type': 'docx'}
        return render(request, 'deleteCBCTestResult.html', context)


# Marc John Corral