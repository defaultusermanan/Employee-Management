from django import forms
from .models import employees

class EmployeeFeedbackForm(forms.ModelForm):
    class Meta:
        model = employees
        fields = ['emp_id', 'name' , 'joined_date' , 'manager_email'] 