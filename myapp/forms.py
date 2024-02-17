from django import forms
from .models import Client, Car, RegisterLocation


## Cadastra Cliente    
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        
    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  
        for field_name, field in self.fields.items():   
              field.widget.attrs['class'] = 'form-control'



class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


## Cadastra um Imovel
class CarForm(forms.ModelForm):
    car = MultipleFileField(label='Select files', required=False)

    class Meta:
        model = Car
        fields = '__all__'
        exclude = ('is_locate',)
        
    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  
        for field_name, field in self.fields.items():   
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


## Registra Locação do Imovel    
class RegisterLocationForm(forms.ModelForm):
    dt_start = forms.DateTimeField(widget=forms.DateInput(format='%d-%m-%Y',attrs={'type': 'date',}))
    dt_end = forms.DateTimeField(widget=forms.DateInput(format='%d-%m-%Y',attrs={'type': 'date',}))

    class Meta:
        model = RegisterLocation
        fields = '__all__'
        exclude = ('car','create_at',)
        
    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  
        for field_name, field in self.fields.items():   
              field.widget.attrs['class'] = 'form-control'