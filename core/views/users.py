"""User related views."""
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, DetailView, CreateView, RedirectView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from core.forms import RegisterUserForm, EditUserForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from core.models import Group, User, Game, GroupInvitation
from django.shortcuts import get_object_or_404
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
        if self.request.user and self.request.user != user and hasattr(self.request.user, 'group_set'):
            invite_groups = set(self.request.user.group_set.all())
            invite_groups -= set(groups)
            pending_invites = set(i.group for i in GroupInvitation.objects.filter(user=user))
            invite_groups -= pending_invites
            context['invite_groups'] = invite_groups
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
        context["request_sent"] = GroupInvitation.objects.filter(user=self.request.user, group=self.object).exists()
        context["games"] = self.object.game_set.all()
        return context


class GroupInvitationView(LoginRequiredMixin, DetailView):
    """View a group invitation."""

    model = GroupInvitation
    template_name = "user/invitation.html"

    def get_object(self, **kwargs):
        """Get the specific group.
        """
        pk = self.kwargs.get('pk')
        invitation = get_object_or_404(GroupInvitation, id=pk)
        return invitation

    # We need this to override django's defaults for posting.
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(GroupInvitationView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """Set the page title."""
        context = super(GroupInvitationView, self).get_context_data(**kwargs)
        invite = self.object
        group = invite.group
        user = invite.user
        inviting = invite.inviting

        # Simplify our checks here
        in_group = self.request.user in group.members.all()
        is_user = self.request.user == user

        # not inviting === this is a request to join the group
        viewable = (inviting and is_user) or (not inviting and in_group)
        context["viewable"] = viewable

        context["in_group"] = in_group
        context["is_user"] = is_user
        context["invite"] = invite
        return context

    def post(self, request, *args, **kwargs):
        # Don't do anything about invalid posts
        invite = self.get_object()
        group = invite.group
        if invite.valid_user(request.user):
            accept = request.POST.get('accept')
            # Convert from a string here
            accept = {'True': True, 'False': False}.get(accept)
            if accept:
                invite.accept()
            elif accept is False:
                invite.decline()
        return JsonResponse({'url': reverse('core:groups-detail',
                                            kwargs={'pk': group.id})})


class GroupJoinView(LoginRequiredMixin, View):
    """Allow a user to join a given group."""

    model = Group

    # We need this to override django's defaults for posting.
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(GroupJoinView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Add the logged in user to this group."""
        pk = self.kwargs.get('pk')
        group = Group.objects.get(id=pk)
        user = self.request.user
        GroupInvitation.create(user=user, group=group, inviting=False)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        group = Group.objects.get(id=pk)
        user_pk = self.request.POST.get('user')
        if user_pk:
            user = User.objects.get(id=user_pk)
            GroupInvitation.create(user=user, group=group, inviting=True)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})


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

    def form_valid(self, form):
        response = super(GroupCreateView, self).form_valid(form)
        self.object.members.add(self.request.user)
        self.object.save()
        return response
