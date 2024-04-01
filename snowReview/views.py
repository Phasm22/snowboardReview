from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.db.models import Q

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from .forms import GuideForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ReviewForm
from snowReview.forms import SnowboardForm, CommentForm
from .models import Snowboard, Profile, Review

# Create your views here.
def index(request):
    # active query set
    snowboards = Snowboard.objects.all()
    print(snowboards)
    return render(request, 'snowReview/home.html', {'snowboards': snowboards})

# Hope page view
def home_view(request):
    # for user to see their name
    context = {
        'user': request.user,
    }
    return render(request, 'snowReview/home.html', context)

# login page
def login_view(request):
    # using djangos built in login form
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'You are now logged in as {username}.')
                return redirect('home_view')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = CustomAuthenticationForm()
    # render the login page with the form
    return render(request = request, template_name = "snowReview/login.html", context={"login_form":form})

# logout view to log out the user and redirect to the home page
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home_view')

# using the built in django detail view to show the snowboard details
class SnowboardDetailView(DetailView):
    model = Snowboard

# using the built in django update view to update the snowboard details
class SnowboardListView(ListView):
    model = Snowboard
    template_name = 'snowReview/snowboard_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        # only show the profile if the user is authenticated
        if self.request.user.is_authenticated:
            context['profile'], created = Profile.objects.get_or_create(user=self.request.user)
        return context
    
# using the built in django form view to filter the snowboards
class GuideView(FormView):
    template_name = 'snowReview/Guide.html'
    form_class = GuideForm

# filtered snowboard view
def snowboard_view(request):
    # get the form
    form = GuideForm(request.GET)

    # get all the snowboards
    snowboards = Snowboard.objects.all()

    if form.is_valid():
        # filter the snowboards based on the form data
        if form.cleaned_data['rider']:
            snowboards = snowboards.filter(rider=str(form.cleaned_data['rider']))  # Ensure the value is a string
        if form.cleaned_data['terrain']:
            # Ensure each value in the list is a string
            terrains = [str(terrain) for terrain in form.cleaned_data['terrain']]
            # filter by terrains and distinct to avoid duplicates
            snowboards = snowboards.filter(terrain__name__in=terrains).distinct()
    else:
        # if there are any errors in the form
        print(form.errors)

    return render(request, 'snowReview/snowboard.html', {'form': form, 'snowboards': snowboards})

def createSnowboard(request):
    form = SnowboardForm()

    if request.method == 'POST':
        form = SnowboardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('snowboard-list')

    context = {'form': form, 'action': 'Add', 'object_type': 'Snowboard'}
    return render(request, 'snowReview/addBoard_form.html', context)

# for creating a user account
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# For adding comments
def add_comment(request, snowboard_id):
    # to link the comment to the snowboard
    snowboard = get_object_or_404(Snowboard, pk=snowboard_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.snowboard = snowboard
            comment.save()
            # to get location and confirmation of message
            messages.success(request, 'Comment added.')

            return redirect('snowboard-detail', pk=snowboard.id)
    else:
        form = CommentForm()
    return render(request, 'snowReview/snowboard_detail.html', {'snowboard': snowboard, 'form': form})


def add_review(request, snowboard_id):
    # to get the current snowboard to display it during the form
    snowboard = get_object_or_404(Snowboard, pk=snowboard_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():

            # Limit the number of reviews per snowboard
            review_limit = 3
            existing_reviews = Review.objects.filter(snowboard=snowboard).count()
            if existing_reviews >= review_limit:
                messages.error(request, 'Review limit for this snowboard has been reached.')
                return redirect('snowboard-detail', pk=snowboard_id)

            review = form.save(commit=False)
            review.snowboard = snowboard
            review.reviewer = request.user.profile
            review.save()

            # for the window location scroll pos
            review_posted = True
            messages.success(request, 'Review added.')
            return redirect('snowboard-detail', pk=snowboard_id)
    else:
        review_posted = False
        form = ReviewForm()
    return render(request, 'snowboard_detail.html', {'form': form, 'review_posted': review_posted})