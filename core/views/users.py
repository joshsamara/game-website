from django.http import HttpResponseRedirect
from core.forms import RegisterUserForm
from django.shortcuts import render


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            # User needs to be Logged in after creation
            return HttpResponseRedirect("/")
    else:
        form = RegisterUserForm()

    return render(request, "registration/register.html", {
        'form': form,
    })
