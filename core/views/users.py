from django.views.generic import View, ListView, DetailView
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
        return self.request.user.group_set.all()

    def get_context_data(self, **kwargs):
        context = super(UserGroupsView, self).get_context_data(**kwargs)
        context["page_title"] = "My Groups"
        return context


class GroupsView(ListView):
    template_name = "user/groups.html"

    def get_queryset(self):
        return Group.objects.all()

    def get_context_data(self, **kwargs):
        context = super(GroupsView, self).get_context_data(**kwargs)
        context["page_title"] = "Groups"
        return context


class GroupDetailView(DetailView):
    template_name = "user/group.html"
    model = Group

    def get_object(self):
        pk = self.kwargs.get('pk')
        # TODO: 404 when object not found
        return Group.objects.get(id=pk)

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        context["in_group"] = self.request.user in self.object.members.all()
        return context


class GroupJoinView(LoginRequiredMixin, View):
    model = Group

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        group = Group.objects.get(id=pk)
        group.members.add(self.request.user)
        group.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class GroupLeaveView(View):
    model = Group

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        group = Group.objects.get(id=pk)
        group.members.remove(self.request.user)
        group.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
