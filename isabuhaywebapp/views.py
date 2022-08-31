from lib2to3.refactor import get_all_fix_names
from urllib import request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from isabuhaywebapp.models import *
from django.shortcuts import *
from .forms import *
from datetime import datetime
import cv2
import numpy as np
import pytesseract
import os
import re
import PyPDF4
import docx2txt as d2t
from urllib.request import urlopen
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile

class DisplayClientSide(TemplateView):
    template_name = 'displayClientSide.html'

class DisplayAllCBCTestResult(ListView):
    model = CBCTestResult
    ordering = ['-dateRequested']
    template_name = 'displayAllCBCTestResult.html'

class DisplayCBCTestResult(DetailView):
    model = CBCTestResult
    template_name = 'displayCBCTestResult.html'

class DisplayAddingOptions(TemplateView):
    template_name = 'DisplayAddingOptions.html'

class UploadPDF(CreateView):
    model = CBCTestResultPDF
    form_class = CBCTestResultPDFForm
    template_name = 'uploadCBCTestResult.html'

    def get_context_data(self, **kwargs):
        context = super(UploadPDF, self).get_context_data(**kwargs)
        context['type'] = 'pdf'
        return context

class UploadDocx(CreateView):
    model = CBCTestResultDocx
    form_class = CBCTestResultDocxForm
    template_name = 'uploadCBCTestResult.html'

    def get_context_data(self, **kwargs):
        context = super(UploadDocx, self).get_context_data(**kwargs)
        context['type'] = 'docx'
        return context

class UploadImage(CreateView):
    model = CBCTestResultImage
    form_class = CBCTestResultImageForm
    template_name = 'uploadCBCTestResult.html'

    def get_context_data(self, **kwargs):
        context = super(UploadImage, self).get_context_data(**kwargs)
        context['type'] = 'image'
        return context

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

class CreateCBCTestResult(CreateView):
    model = CBCTestResult
    form_class = CBCTestResultForm
    template_name = 'createCBCTestResult.html'

    def get_context_data(self, **kwargs):
        context = super(CreateCBCTestResult, self).get_context_data(**kwargs)
        context['type'] = self.kwargs['type']
        if self.kwargs['type'] == 'docx':
            context['docxObject'] = CBCTestResultDocx.objects.get(pk = int(self.kwargs['pk']))
        elif self.kwargs['type'] == 'pdf':
            context['pdfObject'] = CBCTestResultPDF.objects.get(pk = int(self.kwargs['pk']))
        elif self.kwargs['type'] == 'image' or self.kwargs['type'] == 'picture':
            context['imgObject'] = CBCTestResultImage.objects.get(pk = int(self.kwargs['pk']))
        return context

    def get_initial(self, *args, **kwargs):
        initial = super(CreateCBCTestResult, self).get_initial(**kwargs)
        data = {}
        if self.kwargs['type'] == 'docx':
            docxObject = CBCTestResultDocx.objects.get(pk = int(self.kwargs['pk']))
            initial['testImage'] = None
            initial['testPDF'] = None
            initial['testDocx'] = docxObject
            FILE_PATH = 'D:/Django Projects/IsabuhayWebsite'+str(docxObject.testDocx.url)
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
        elif self.kwargs['type'] == 'pdf':
            pdfObject = CBCTestResultPDF.objects.get(pk = int(self.kwargs['pk']))
            initial['testPDF'] = pdfObject
            initial['testImage'] = None
            initial['testDocx'] = None
            FILE_PATH = 'D:/Django Projects/IsabuhayWebsite'+str(pdfObject.testPDF.url)

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
        elif self.kwargs['type'] == 'image' or self.kwargs['type'] == 'picture':
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
            
            imgQ = cv2.imread('D:\\Django Projects\\IsabuhayWebsite\\imageQuery\\sample.png')
            h,w,c = imgQ.shape
            gray_image = grayscale(imgQ)
            thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)

            orb = cv2.ORB_create(1000)
            kp1, des1 = orb.detectAndCompute(im_bw, None)

            imgObject = CBCTestResultImage.objects.get(pk = int(self.kwargs['pk']))
            initial['testImage'] = imgObject
            initial['testPDF'] = None
            initial['testDocx'] = None
            img = cv2.imread('D:/Django Projects/IsabuhayWebsite'+str(imgObject.testImage.url))
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

        initial['source'] = data['source']
        initial['labNumber'] = data['labNumber']
        initial['pid'] = data['pid']
        date_time_str = data['dateRequested']
        try:
            initial['dateRequested'] = datetime.strptime(date_time_str, '%m-%d-%Y %H:%M %p')
        except:
            initial['dateRequested'] = None
        date_time_str = data['dateReceived']
        try:
            initial['dateReceived'] = datetime.strptime(date_time_str, '%m-%d-%Y %H:%M %p')
        except:
            initial['dateReceived'] = None
        initial['whiteBloodCells'] = data['whiteBloodCells']
        initial['redBloodCells'] = data['redBloodCells']
        initial['hemoglobin'] = data['hemoglobin']
        initial['hematocrit'] = data['hematocrit']
        initial['meanCorpuscularVolume'] = data['meanCorpuscularVolume']
        initial['meanCorpuscularHb'] = data['meanCorpuscularHb']
        initial['meanCorpuscularHbConc'] = data['meanCorpuscularHbConc']
        initial['rbcDistributionWidth'] = data['rbcDistributionWidth']
        initial['plateletCount'] = data['plateletCount']
        initial['segmenters'] = data['segmenters']
        initial['lymphocytes'] = data['lymphocytes']
        initial['monocytes'] = data['monocytes']
        initial['eosinophils'] = data['eosinophils']
        initial['basophils'] = data['basophils']
        initial['bands'] = data['bands']
        initial['absoluteSeg'] = data['absoluteSeg']
        initial['absoluteLymphocyteCount'] = data['absoluteLymphocyteCount']
        initial['absoluteMonocyteCount'] = data['absoluteMonocyteCount']
        initial['absoluteEosinophilCount'] = data['absoluteEosinophilCount']
        initial['absoluteBasophilCount'] = data['absoluteBasophilCount']
        initial['absoluteBandCount'] = data['absoluteBandCount']
        return initial

class UpdateCBCTestResult(UpdateView):
    model = CBCTestResult
    form_class = CBCTestResultForm
    template_name = 'updateCBCTestResult.html'

class DeleteCBCTestResult(DeleteView):
    model = CBCTestResult
    template_name = 'deleteCBCTestResult.html'
    success_url = reverse_lazy('DisplayAllCBCTestResult')

    def get_context_data(self, **kwargs):
        context = super(DeleteCBCTestResult, self).get_context_data(**kwargs)
        context['type'] = 'record'
        return context

class DeleteUploadedImage(DeleteView):
    model = CBCTestResultImage
    template_name = 'deleteCBCTestResult.html'
    success_url = reverse_lazy('UploadImage')

    def get_context_data(self, **kwargs):
        context = super(DeleteUploadedImage, self).get_context_data(**kwargs)
        context['type'] = 'image'
        return context
    
class DeleteCapturedImage(DeleteView):
    model = CBCTestResultImage
    template_name = 'deleteCBCTestResult.html'
    success_url = reverse_lazy('CaptureImage')

    def get_context_data(self, **kwargs):
        context = super(DeleteCapturedImage, self).get_context_data(**kwargs)
        context['type'] = 'picture'
        return context

class DeletePDF(DeleteView):
    model = CBCTestResultPDF
    template_name = 'deleteCBCTestResult.html'
    success_url = reverse_lazy('UploadPDF')

    def get_context_data(self, **kwargs):
        context = super(DeletePDF, self).get_context_data(**kwargs)
        context['type'] = 'pdf'
        return context

class DeleteDocx(DeleteView):
    model = CBCTestResultDocx
    template_name = 'deleteCBCTestResult.html'
    success_url = reverse_lazy('UploadDocx')

    def get_context_data(self, **kwargs):
        context = super(DeleteDocx, self).get_context_data(**kwargs)
        context['type'] = 'docx'
        return context
