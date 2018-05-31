from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from decouple import config

class SignUpForm(UserCreationForm):

    # Sign Up Form fields, add extra info you'd like the user to put in their profile here
    first_name = forms.CharField( max_length=30, required=True, help_text='' )
    last_name = forms.CharField( max_length=30, required=True, help_text='' )
    email = forms.EmailField( max_length=300, help_text='*Required. Must be valid email address.' )
    password1 = forms.CharField( label='Password', widget=forms.PasswordInput, help_text='Must be at least 8 characters.' )
    #bio = forms.CharField( label='bio', help_text='Enter tags here.', widget=forms.Textarea(attrs={'cols': 80, 'rows': 4}) )
    owner_key = forms.CharField( max_length=32, required=False, help_text='If you have a upgrade to a Business Profile, enter your key here.') #, validators=[valid_owner_key] )
    #profile_image = forms.ImageField(help_text='Upload a profile image')

    def valid_owner_key(self):
        attempted_key = self.cleaned_data['owner_key']
        real_key = config('OWNER_KEY')
        if real_key != attempted_key:
            raise ValidationError({'owner_key': ["Wrong Owner Key",]})
        return attempted_key
    # Be sure to add extra fields here
    class Meta:
        model = User
        fields = (  'username',
                    'first_name',
                    'last_name',
                    'email',
                    'password1',
                    'password2',
                    #'bio',
                    'owner_key'
                    #'profileimage',
                    )

class UpdateUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        #Prefill form with old info
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['first_name'].initial = kwargs['instance'].first_name
            self.fields['last_name'].initial = kwargs['instance'].last_name
            self.fields['email'].initial = kwargs['instance'].email
            self.fields['bio'].inital = kwargs['instance'].bio

    first_name = forms.CharField( max_length=30, required=True, )
    last_name = forms.CharField( max_length=30, required=True, )
    email = forms.EmailField( max_length=300, help_text='*Required. Must be a vaild email address.' )
    bio = forms.CharField( label='About Me', widget=forms.Textarea(attrs={'cols':80, 'rows': 4}) )

    class Meta:
        model = User
        fields = (  'first_name',
                    'last_name',
                    'email',
                    'bio',
                    )