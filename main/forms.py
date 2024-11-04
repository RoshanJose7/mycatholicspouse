from django import forms
from django.forms.models import ModelForm

from .models import MatrimonyApplication


class MatrimonyApplicationForm(ModelForm):
    class Meta:
        model = MatrimonyApplication
        fields = ['first_name','last_name','email','addr_1','addr_2','city','state','country','pin_code','middle_name',
            'hs_marks','tenth_marks','grad_marks','post_grad_marks','tenth_school','hs_school','grad_school','post_grad_school', 'other_marks', 'other_school', 'other_type',
            'height','weight','place_of_birth','parish_baptized_at','present_parish','diocese','occupation','place_of_employment','designation','years_of_employment','annual_income','other_income','about_yourself','disability_type', 'health_issues_details',
            'fathers_name','mothers_name','siblings','brothers','sisters','family_members','about_family',
            'no_of_children_1','no_of_sons_1','no_of_daughters_1','additional_details',
            'no_of_children_2','no_of_sons_2','no_of_daughters_2','cause_of_death',
            'lower_age','upper_age','place_of_residence','education','employment','salary_lower', 'salary_upper',
            'passport_photo_1','family_photo_1','your_photo_1_1','your_photo_2_1','your_photo_3_1',
        ]
        # fields = "__all__"
        # exclude = ['gender','education_level','date_of_bith','marriage_date_1','divorce_date','marriage_annulment_date','marriage_date_2','date_of_death','rite','diet','smoke','drink','marital_status','disability','values','widowed','family_values',]

class RadioForm(forms.Form):
    rad = forms.ChoiceField(choices = (('M', 'Male'),('F','Female')), widget = forms.RadioSelect)

class MatrimonyApplicationEditForm(ModelForm):
    class Meta:
        model = MatrimonyApplication
        fields = [
            'first_name','last_name','email','addr_1','addr_2','city','state','country','pin_code','middle_name',
            'height','weight','place_of_birth','parish_baptized_at','present_parish','diocese','occupation','place_of_employment','designation','years_of_employment','annual_income','other_income','about_yourself','disability_type', 'health_issues_details',
            'lower_age','upper_age','place_of_residence','education','employment','salary_lower', 'salary_upper',
            'passport_photo_1','family_photo_1','your_photo_1_1','your_photo_2_1','your_photo_3_1',
        ]

class FilesForm(ModelForm):

    class Meta:
        model = MatrimonyApplication
        fields = [
            'passport_photo','family_photo','your_photo_1','your_photo_2','your_photo_3',
        ]
