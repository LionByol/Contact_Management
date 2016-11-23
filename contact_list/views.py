from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader, RequestContext
from django.views import generic
from contact_list.models import Question, Choice, Contactlist, UploadFileModel
from .forms import CostForm
from .forms import UploadFileForm
import csv
import io
import codecs

def index(request):    
    contactdata = Contactlist.objects.all()
    showcontact = 25
    number = 0
    totalcontact = len(contactdata)
    return render(request, "polls/index.html", {"contactdata":contactdata,"showcontact":showcontact,
        "totalcontact":totalcontact,"number":number})

def csvUploadView(request):
    return render(request, "polls/csvUpload.html", {})

def csvComplete(request):
    # get data from uploaded file    
    f=open('tmp/test.csv')
    data = csv.reader(f)
    data = list(data)
    length=len(data)
    # save into database
    contactlist=Contactlist()
    for i in range(1,length-1):
        contactlist.email = data[i][0]
        contactlist.name = data[i][1]
        contactlist.company = data[i][2]
        contactlist.source = "csv"
        contactlist.save()

    return render(request, "polls/csvComplete.html", {"length":length-1})
    # return redirect("/contact_list/")

def csvImportView(request):    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)        
        if form.is_valid():
            # file upload
            instance = UploadFileModel(file=request.FILES['file'])
            instance.save()
            # make array
            csvfile = instance.file            
            dialect = csv.Sniffer().sniff(codecs.EncodedFile(csvfile, "utf-8").read(1024))
            csvfile.open()
            data = csv.reader(codecs.EncodedFile(csvfile, "utf-8"), delimiter=',', dialect=dialect)
            data = list(data)
            
            return render(request, 'polls/csvImport.html', {'data10': data[1][0],'data11': data[1][1],'data12': data[1][2],'data20': data[2][0],'data21': data[2][1],'data22': data[2][2],'data30': data[3][0],'data31': data[3][1],'data32': data[3][2],'data40': data[4][0],'data41': data[4][1],'data42': data[4][2]})            
    else:
        form = UploadFileForm()
    return render(request, 'polls/csvImport.html', {'form': form})

def searchView(request):    
    if request.method == 'POST':
        search = request.POST.get('search','')
        if search == '':
            contactdata = Contactlist.objects.all()
        else:
            contactdata = Contactlist.objects.filter(name=search)
        showcontact = 25
        number = 0
        totalcontact = len(contactdata)
        return render(request, "polls/index.html", {"contactdata":contactdata,"showcontact":showcontact,"totalcontact":totalcontact,"number":number})
        # return render_to_response('polls/index.html', {'details': details})
    else:
        contactdata = Contactlist.objects.all()
        showcontact = 25
        number = 0
        totalcontact = len(contactdata)
        # return redirect("http://127.0.0.1:8000/contact_list/")
        return render(request, "polls/index.html", {"contactdata":contactdata,"showcontact":showcontact,
            "totalcontact":totalcontact,"number":number})
def costView(request):
    if request.method == 'POST':
        form = CostForm(request.POST)
        if form.is_valid():
            email1 = request.POST.get('email','')
            name1 = request.POST.get('name','')
            company1 = request.POST.get('company','')
            cost_obj = Contactlist(email = email1, name = name1, company = company1 ,source = "manual")
            cost_obj.save()
            # return HttpResponseRedirect(reverse('contact_list:cost'))
            # return HttpResponseRedirect('.')
            # return redirect('polls/index.html')
            # return redirect("http://127.0.0.1:8000/contact_list/")
            contactdata = Contactlist.objects.all()
            showcontact = 25
            number = 1
            totalcontact = len(contactdata)
            return render(request, "polls/index.html", {"contactdata":contactdata,"showcontact":showcontact,"totalcontact":totalcontact,"number":number,"form":form})
        else:
            form = CostForm()

        return render(request, 'contact_list:cost',{'form':form,})

def crudops(request):
    #Creating an entry
    contactlist=Contactlist(email="kkl@.com", name="dragon",
    company="sorex", source="manual", lasttouch="07/30/16", nexttouch="07/31/16")
    contactlist.save()
    #Read ALL entries
    objects = Contactlist.objects.all()
    res ='Printing all Dreamreal entries in the DB : <br>'
    for elt in objects:
        res+=elt.email+"  "+elt.name+"  "+elt.company+"<br>"
    #Read a specific entry:
    sorex = Contactlist.objects.get(name="sorex")
    res += 'Printing One entry <br>'
    res += sorex.name
    #Delete an entry
    res += '<br> Deleting an entry <br>'
    sorex.delete()
    #Update
    contactlist=Contactlist(email="www.@.com", name="sore_polo",
    company="sorex", source="manual", lasttouch="07/29/16", nexttouch="07/30/16")
    contactlist.save()
    res += 'Updating entry<br>'
    contactlist = Contactlist.objects.get(name='sorex')
    contactlist.name = 'thierry'
    contactlist.save()
    return HttpResponse(res)