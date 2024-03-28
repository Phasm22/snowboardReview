from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.shortcuts import get_object_or_404
from snowReview.forms import SnowboardForm
from .models import *

# Create your views here.
def index(request):
    # active query set
    snowboards = Snowboard.objects.all()
    print(snowboards)
    return render(request, 'snowReview/home.html', {'snowboards': snowboards})


def home_view(request):
    return render(request, 'snowReview/home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
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
    form = AuthenticationForm()
    return render(request = request, template_name = "snowReview/login.html", context={"login_form":form})

def logout_view(request):
    logout(request)
    return redirect('home_view')

class SnowboardDetailView(DetailView):  # new line
    model = Snowboard  # new line


class SnowboardListView(ListView):
    model = Snowboard
    template_name = 'snowReview/snowboard_list.html'

def createSnowboard(request):
    form = SnowboardForm()

    if request.method == 'POST':
        form = SnowboardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('snowboard-list')  # Redirect to the list  snowboards

    context = {'form': form, 'action': 'Add', 'object_type': 'Snowboard'}
    return render(request, 'snowReview/addBoard_form.html', context)

