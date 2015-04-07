"""User related views."""
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, DetailView, CreateView, RedirectView
from django.http import HttpResponseRedirect
from core.forms import RegisterUserForm, EditUserForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from core.models import Group, User, Game
from . import LoginRequiredMixin


def register(request):
    """Register a user account."""
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


@login_required
def edit(request):
    """Edit a user account."""
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('core:profile:base'))
    else:
        form = EditUserForm(instance=request.user)

    return render(request, "user/edit_profile.html", {
        'form': form,
    })

@login_required
def change_password(request):
    """Edit a user password."""
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('core:profile:base'))
    else:
        form = EditUserForm(instance=request.user)

    return render(request, "user/../templates/registration/change_password.html", {
        'form': form,
    })


class ProfileRedirectView(LoginRequiredMixin, RedirectView):
    """Redirect to the user profile page."""

    permanent = False
    pattern_name = 'core:profile:user-profile'

    def get_redirect_url(self, *args, **kwargs):
        """Redirect to the user's page."""
        kwargs['pk'] = self.request.user.pk
        return super(ProfileRedirectView, self).get_redirect_url(*args, **kwargs)


class ProfileView(DetailView):
    """Display the user profile page."""

    template_name = "user/profile.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs.get('pk'))
        groups = Group.objects.filter(members=user)
        context['games_list'] = Game.objects.filter(group__in=groups)
        context['show_edit'] = user.pk is self.request.user.pk
        return context


class UserGroupsView(LoginRequiredMixin, ListView):
    """Display a list of user's groups."""

    template_name = "user/groups.html"

    def get_queryset(self):
        """Get all of the user's groups."""
        return self.request.user.group_set.all()

    def get_context_data(self, **kwargs):
        """Set the page title."""
        context = super(UserGroupsView, self).get_context_data(**kwargs)
        context["page_title"] = "My Groups"
        return context


class GroupsView(ListView):
    """Display a list of ALL groups."""

    template_name = "user/groups.html"

    def get_queryset(self):
        """Get ALL groups."""
        return Group.objects.all()

    def get_context_data(self, **kwargs):
        """Set the page title."""
        context = super(GroupsView, self).get_context_data(**kwargs)
        context["page_title"] = "Groups"
        return context


class GroupDetailView(DetailView):
    """Display a single group."""

    template_name = "user/group.html"
    model = Group

    def get_object(self, **kwargs):
        """Get the specific group.
        :param **kwargs:
        """
        pk = self.kwargs.get('pk')
        # TODO: 404 when object not found
        return Group.objects.get(id=pk)

    def get_context_data(self, **kwargs):
        """Set the page title."""
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        context["in_group"] = self.request.user in self.object.members.all()
        return context


class GroupJoinView(LoginRequiredMixin, View):
    """Allow a user to join a given group."""

    model = Group

    def get(self, request, *args, **kwargs):
        """Add the logged in user to this group."""
        pk = self.kwargs.get('pk')
        group = Group.objects.get(id=pk)
        group.members.add(self.request.user)
        group.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class GroupLeaveView(LoginRequiredMixin, View):
    """Allow a user to leave a given group."""

    model = Group

    def get(self, request, *args, **kwargs):
        """Remove the logged in user to this group."""
        pk = self.kwargs.get('pk')
        group = Group.objects.get(id=pk)
        group.members.remove(self.request.user)
        group.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class GroupCreateView(LoginRequiredMixin, CreateView):
    """Create a group."""

    model = Group
    fields = ['name']
    template_name = "user/new_group.html"
