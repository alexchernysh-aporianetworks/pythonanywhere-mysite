from django import forms

class GoogleSheetForm(forms.Form):
    sheet_id = forms.CharField(label='Sheet ID', max_length=100)
    sheet_name = forms.CharField(label='Sheet Name', max_length=100)
    import_number = forms.IntegerField(label='Import Number')
    output_number = forms.IntegerField(label='Output Number')

    # Dropdown for model name choices
    MODEL_CHOICES = [
        ('text-davinci-003', 'text-davinci-003'),
        ('gpt-3.5-turbo', 'gpt-3.5-turbo'),
        ('gpt-4', 'gpt-4'),
        ('gpt-4o', 'gpt-4o'),
        ('gpt-4.1', 'gpt-4.1'),  # Added new model gpt-4o
        ('gpt-4.1-mini', 'gpt-4.1-mini'),  # Added new model gpt-4o
        ('gpt-5-mini', 'gpt-5-mini'),  # Added new model gpt-4o
    ]
    model_name = forms.ChoiceField(choices=MODEL_CHOICES, label='Model Name')

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='Enter Password')

class zemantayes(forms.Form):

    # Dropdown for model name choices
    sheet_CHOICES = [
        ('Zm-Yes', 'Zm-Yes'),
        ('Zm-2D', 'Zm-2D')
    ]
    sheet_name = forms.ChoiceField(choices=sheet_CHOICES, label='sheet Name')

from django import forms
from .models import ScheduledScriptTask

class ScheduledScriptTaskForm(forms.ModelForm):
    class Meta:
        model = ScheduledScriptTask
        fields = ['script_path', 'run_time', 'timezone', 'is_active']
        widgets = {
            'run_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'timezone': forms.TextInput(attrs={'placeholder': 'e.g., UTC'}),
        }