from django import forms
class CostForm(forms.Form):
	email = forms.CharField()
	name = forms.CharField()
	company = forms.CharField()

class UploadFileForm(forms.Form):
	# title = forms.CharField(max_length=50)
	file = forms.FileField()


		