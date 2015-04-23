"""Forms for users."""
from collections import OrderedDict
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import SetPasswordForm
from django.forms import ModelForm, RadioSelect
from django.utils.translation import ugettext_lazy as _


from core.models import User


class RegisterUserForm(ModelForm):
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
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'birthday', 'public')

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


class EditUserForm(ModelForm):
    """Form to allow users to edit their profiles"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'public', 'birthday']
        widgets = {
            'gender': RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        """Setup the form to work with crispy_forms."""
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))


class CustomPasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.

    A slightly modified version of Django's default PasswordChangeForm
    set up for Crispy Forms
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
    })
    old_password = forms.CharField(label=_("Old password"),
                                   widget=forms.PasswordInput)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    def __init__(self, *args, **kwargs):
        """Setup the form to work with crispy_forms."""
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))

CustomPasswordChangeForm.base_fields = OrderedDict(
    (k, CustomPasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
)
