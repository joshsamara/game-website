# from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            #User needs to be Logged in after creation
            return HttpResponseRedirect("/core/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })
