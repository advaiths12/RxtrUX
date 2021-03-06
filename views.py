from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from PIL import Image
from bayersite.models import Document
from bayersite.forms import DocumentForm
from bayersite.Main import *
# Create your views here.
class index(TemplateView):
    template_name = 'index.html'

class xray(TemplateView):
	template_name = 'xray.html'

#get the results 
def results(request):
	template_name = 'results.html'
	return render(request, template_name)

#the csrf cookie crashes any posting of content to server so disable
@csrf_exempt
def xraysubmit(request):
    template_name = 'xray.html'
	#if an image is uploaded
    if(request.method == 'POST'):
		#form = DocumentForm(request.POST, request.FILES)
        print(request.user, "has submitted an X-Ray")
        myfile = request.FILES['myfile']
        print(type(myfile))
		#save the image if it's actually an image
        diagnosisarr = []
        diagnosis = ''
        try:
            img = Image.open(myfile)
			#path
			###	WE TRACK IMPROVEMENT OF THE LUNGS OVER TIME WITH COLLECTION
			### OF PICTURES AS A LOG
            resultpath = 'user_uploaded/' + myfile.name
            imgpath =  'bayersite/static/' + myfile.name 
            img.save(imgpath)
            #img.show()
			#read past file in order to put new on top
            with open('bayersite/image_path_txt/path.txt', 'r') as myfile:
                filestr = myfile.read()
			#write the path
            f = open('bayersite/image_path_txt/path.txt', 'w')
            f.write(imgpath)
			#sentinel the loop in order to guarantee no extra empty line at bottom
            if(len(filestr) > 0):
                f.write('\n')
            f.write(filestr)
            f.close()	#write path to text file for the backend
			#backend
            print("starting backend")
            main()
            print("finished backend")
            #get diagnosis
            with open('diagnosis.txt', 'r') as myfile:
                diagnosisarr = myfile.read().splitlines()
            print(diagnosisarr)
            for line in diagnosisarr:
                diagnosis += line
                diagnosis += '\n'

			
        except:
            raise Exception("image type error")

		#make context based on the backend output
        return render(request, 'results.html', {'diagnosis': diagnosis, 'filename': myfile.name})
    else:
        return render(request, 'xray.html')

