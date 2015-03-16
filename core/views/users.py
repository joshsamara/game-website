from django.http import HttpResponseRedirect
from core.forms import RegisterUserForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['email']
            password = request.POST['password1']
            user = authenticate(username=username,
                                password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('core:home'))
    else:
        form = RegisterUserForm()

    return render(request, "registration/register.html", {
        'form': form,
    })
