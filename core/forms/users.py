"""Forms for users."""
from django import forms
from core.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class RegisterUserForm(forms.ModelForm):

    """A form that creates a user from the given email and password."""

    error_messages = {
        'duplicate_email': "A user with that email already exists.",
        'password_mismatch': "The two password fields didn't match.",
    }
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

    class Meta:
        model = User
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        """Setup the form to work with crispy_forms."""
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-registerForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_email(self):
        """Keep emails unique."""
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password2(self):
        """Ensure passwords are the same."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        """Create a user on success."""
        user = super(RegisterUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
