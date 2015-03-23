from django.views.generic import View, ListView
from django.http import HttpResponseRedirect
from core.forms import RegisterUserForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from core.models import Group
from . import LoginRequiredMixin


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


class Profile(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "user/profile.html")


class UserGroupsView(LoginRequiredMixin, ListView):
    template_name = "user/groups.html"

    def get_queryset(self):
        return self.request.user.groups.all()

    def get_context_data(self, **kwargs):
        context = super(UserGroupsView, self).get_context_data(**kwargs)
        context["page_title"] = "My Groups"
        return context


class GroupsView(LoginRequiredMixin, ListView):
    template_name = "user/groups.html"

    def get_queryset(self):
        return Group.objects.all()

    def get_context_data(self, **kwargs):
        context = super(GroupsView, self).get_context_data(**kwargs)
        context["page_title"] = "Groups"
        return context
