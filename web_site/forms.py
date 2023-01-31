from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Prijava, User, Smjer, Predmet



class NewUserForm(UserCreationForm):
    ime = forms.CharField(required=True)
    prezime = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("ime", "prezime", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.ime = self.cleaned_data['ime']
        user.prezime = self.cleaned_data['prezime']
        if commit:
            user.save()
        return user



class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.naziv



class PredmetForm(forms.ModelForm):
    #choice filed za smjerove, ovisno koliko ih ima
    smjer = MyModelChoiceField(
        queryset=Smjer.objects.all(),
    )

    class Meta:
        model = Predmet
        fields = ('ime_predmeta', 'ects', 'smjer')
        labels = {'ime_predmeta': 'Ime predmeta', 'ects': 'ECTS bodovi',
                     'smjer': 'Pripadajući smjer' }


class PrijavaForm(forms.ModelForm):
    smjer = MyModelChoiceField(
        queryset=Smjer.objects.all(),
    )
    
    class Meta:
        model = Prijava
        fields = ('datum_ro', 'mjesto_ro', 'molba', 'dokument',
                     'prosjek', 'ocjena_matura', 'smjer')
        labels = {
                'datum_ro': 'Datum rođenja',
                'mjesto_ro': 'Mjesto rođenja',
                'molba': 'Molba za upis na smjer',
                'dokument': 'Dokument o završenoj školi',
                'prosjek': 'Prosjek ocjena',
                'ocjena_matura': 'Ocjena na maturi (ukupna)',
                'smjer': 'Odabir smjera',
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['datum_ro'].widget = DateInput()
        self.user = user
    
    def save(self, commit=True):
        prijava = super(PrijavaForm, self).save(commit=False)
        prijava.user = self.user 
        if commit:
            prijava.save()
        return prijava


#login forma
class NewAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']
    

class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%d-%m-Y%"
        super().__init__(**kwargs)