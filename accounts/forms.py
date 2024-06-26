# forms.py
from django import forms
from .models import player

class playerRegistrationForm(forms.ModelForm):
    class Meta:
        
        model = player
        fields = ['last_name', 'first_name', 'school', 'id_card', 'password']

        
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}), 
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'token': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(playerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].label = 'Nom'
        self.fields['first_name'].label = 'Prénom'
        self.fields['school'].label = 'École (renseignez "sans école" si vous n\'êtes pas étudiant)'
        self.fields['id_card'].label = 'Carte étudiant'
        self.fields['password'].label = 'Mot de passe'
        self.fields['password'].widget = forms.PasswordInput()
        # make sure id_card is an image or a pdf
        self.fields['id_card'].widget.attrs.update({'accept': 'image/*'})
        
        # set all fields as required
        for field in self.fields.values():
            field.widget.attrs.update({'required': 'required'})

        # set id for all fields taht is the same as the name
        for field in self.fields.values():
            field.widget.attrs.update({'id': field.label.lower().replace(' ', '_')})
            

class updateProfile(forms.ModelForm):
    """Form that allows players to change their profile picture and biography"""
    clear_pp = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'id': 'clear_pp'}))

    class Meta:
        model = player
        fields = ['profile_picture', 'biography']

        widgets = {
            'profile_picture': forms.FileInput(attrs={'accept': 'image/*', 'enctype': 'multipart/form-data'}),
        }

    def __init__(self, *args, **kwargs):
        super(updateProfile, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].label = 'Photo de profil'
        self.fields['biography'].label = 'Biographie'
        self.fields['clear_pp'].label = 'Supprimer la photo de profil'

        # Set id for all fields that is the same as the name
        for field in self.fields.values():
            field.widget.attrs.update({'id': field.label.lower().replace(' ', '_')})

        # change order to put clear_pp right after profile_picture
        self.fields = {
            'profile_picture': self.fields['profile_picture'],
            'clear_pp': self.fields['clear_pp'],
            'biography': self.fields['biography'],
        }

    class Media:
        enctype = 'multipart/form-data'