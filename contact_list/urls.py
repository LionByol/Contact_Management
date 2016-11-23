from django.conf.urls import url

from . import views

urlpatterns = [
# ex: /polls/
url(r'^$', views.index, name='index'),
url(r'^cost/$', views.costView, name='cost'),
url(r'^search/$', views.searchView, name='search'),
url(r'^csvUploadView/$', views.csvUploadView, name='csvUploadView'),
url(r'^csvImportView/$', views.csvImportView, name='csvImportView'),
url(r'^csvComplete/$', views.csvComplete, name='csvComplete'),
]