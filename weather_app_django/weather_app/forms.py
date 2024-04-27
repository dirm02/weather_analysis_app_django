from django import forms

class ZipCodeForm(forms.Form):
    zip_code = forms.CharField(label='Enter ZIP code', max_length=10)

class StartDateForm(forms.Form):
    start_date = forms.DateField(label='Enter Start Date', required=False)

class EndDateForm(forms.Form):
    end_date = forms.DateField(label='Enter End Date', required=False)
    
