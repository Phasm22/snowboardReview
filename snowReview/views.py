from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from .forms import GuideForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from snowReview.forms import SnowboardForm
from .models import *

# Create your views here.
def index(request):
    # active query set
    snowboards = Snowboard.objects.all()
    print(snowboards)
    return render(request, 'snowReview/home.html', {'snowboards': snowboards})


def home_view(request):
    context = {
        'user': request.user,
    }
    return render(request, 'snowReview/home.html', context)

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home_view')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = CustomAuthenticationForm()
    return render(request = request, template_name = "snowReview/login.html", context={"login_form":form})

def logout_view(request):
    logout(request)
    return redirect('home_view')

class SnowboardDetailView(DetailView):  # new line
    model = Snowboard  # new line


class SnowboardListView(ListView):
    model = Snowboard
    template_name = 'snowReview/snowboard_list.html'

class GuideView(FormView):
    template_name = 'snowReview/Guide.html'
    form_class = GuideForm

def snowboard_view(request):
    form = GuideForm(request.GET)

    snowboards = Snowboard.objects.all()

    if form.is_valid():
        if form.cleaned_data['rider']:
            snowboards = snowboards.filter(rider=str(form.cleaned_data['rider']))  # Ensure the value is a string

        if form.cleaned_data['terrain']:
            # Ensure each value in the list is a string
            terrains = [str(terrain) for terrain in form.cleaned_data['terrain']]
            snowboards = snowboards.filter(terrain__name__in=terrains)

        print(snowboards)
    else:
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

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
