from django import forms  
from .models import Addemployee 

class DateInput(forms.DateInput):
    input_type = 'date'
    
     
class AddemployeeForm(forms.ModelForm):  
    class Meta:  
        model = Addemployee  
        fields = "__all__"  
        
    widgets = {
            'D_O_B': DateInput(),
            'Date_of_join': DateInput(), 
        } 
    
    
from .models import Admin_Login 

class Admin_LoginForm(forms.ModelForm):  
    class Meta:  
        model = Admin_Login  
        fields = "__all__"
        
        
from .models import Leave_App 

class DateInput(forms.DateInput):
    input_type = 'date'
    
     
class Leave_AppForm(forms.ModelForm):  
    class Meta:  
        model = Leave_App  
        fields = "__all__"  
        
    widgets = {
            'From': DateInput(),
            'to': DateInput(), 
        } 
    
    