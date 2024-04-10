from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views
from .forms import GuideForm
from snowReview.forms import SnowboardForm, CommentForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ReviewForm
from .models import Snowboard, Profile, Review, Comment

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
    paginate_by = 10  # Default to 10 items per page

    def get_queryset(self):
        return Snowboard.objects.all()

    def get_paginate_by(self, queryset):
        items_per_page = self.request.GET.get('items_per_page', self.paginate_by)
        if not items_per_page:
            items_per_page = self.paginate_by
        return int(items_per_page)  # Convert items_per_page to an integer

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
    # Create an instance of the GuideForm using the GET request data
    form = GuideForm(request.GET)
    
    # Retrieve all Snowboard objects from the database
    snowboards = Snowboard.objects.all()
    if form.is_valid():
        if form.cleaned_data['rider']:
            rider = str(form.cleaned_data['rider'])
            if rider:  # Only filter by rider if rider is not an empty string
                snowboards = snowboards.filter(rider=rider)
        if form.cleaned_data['terrain']:
            terrains = [str(terrain) for terrain in form.cleaned_data['terrain']]
            if terrains:  # Only filter by terrain if terrains is not an empty list
                snowboards = snowboards.filter(terrain__name__in=terrains).distinct()
        if form.cleaned_data['shape']:
            shapes = form.cleaned_data['shape']
            print(f"Shapes: {shapes}")  # Debug line
            if shapes:
                snowboards = snowboards.filter(shape__in=shapes)
                print(f"Snowboards after shape filter: {snowboards}")  # Debug line

    items_per_page = request.GET.get('items_per_page', 10)
    if not items_per_page:
        items_per_page = 10
    
    items_per_page = int(items_per_page)  # Convert items_per_page to an integer
    print(f"items_per_page: {items_per_page}")
    paginator = Paginator(snowboards, items_per_page)

    #print the total number of object pagintor has
    print(f"paginator.count: {paginator.count}")    
    # print the total pages
    print(f"paginator.num_pages: {paginator.num_pages}")
    page_number = request.GET.get('page', 1)  # Default to the first page if 'page' is not in the request
    print(f"\npage_number: {page_number}")
    page_obj = paginator.get_page(page_number)


    return render(request, 'snowReview/snowboard.html', {'form': form, 'snowboards': page_obj, 'total_items': snowboards.count()})

def createSnowboard(request):
    form = SnowboardForm()

    if request.method == 'POST':
        form = SnowboardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('snowboard-list')
        else:
            print(f"Form errors: {form.errors}")  # Debug line

    context = {'form': form, 'action': 'Add', 'object_type': 'Snowboard'}
    return render(request, 'snowReview/addBoard_form.html', context)

def delete_snowboard(request, snowboard_id):
    if request.user.is_authenticated and request.user.is_staff:
        snowboard = get_object_or_404(Snowboard, id=snowboard_id)
        snowboard.delete()
        messages.success(request, f'{snowboard} successfully deleted.')
        return redirect('snowboard-list')

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
@login_required(login_url='login')
def add_comment(request, snowboard_id):
    snowboard = get_object_or_404(Snowboard, pk=snowboard_id)
    if request.method == "POST":
        print(request.POST)  # Print POST data
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.snowboard = snowboard
            comment.save()
            messages.success(request, 'Comment added.')
            return redirect('snowboard-detail', pk=snowboard.id)
        else:
            print(form.errors)  # Print form errors
    else:
        form = CommentForm()
    return render(request, 'snowReview/snowboard_detail.html', {'snowboard': snowboard, 'form': form})

# Edit Comment
@login_required(login_url='login')
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user.is_staff or request.user == comment.user:
        if request.method == "POST":
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                messages.success(request, 'Comment updated.')
                return redirect('snowboard-detail', pk=comment.snowboard.id)
            else:
                print(form.errors)  # Print form errors
        else:
            form = CommentForm(instance=comment)
        return render(request, 'snowReview/snowboard_detail.html', {'snowboard': comment.snowboard, 'form': form, 'comment': comment})
    else:
        messages.error(request, 'You do not have permission to edit this comment.')
        return redirect('snowboard-detail', pk=comment.snowboard.id)
# Delete Comment
def delete_comment(request, snowboard_id):
    comment = get_object_or_404(Comment, id=snowboard_id)
    if request.user.is_staff or request.user == comment.user:
        comment.delete()
        messages.success(request, 'Comment Deleted')
    return redirect('snowboard-detail', comment.snowboard.id)


# no path traversal allowed :)
@login_required(login_url='login')
def add_review(request, snowboard_id):
    # init review_posted
    review_posted = False

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
                
                # Redirect to the snowboard detail page with the reviews section in view
                # its really just the url + snowboard id + #reviews
                return redirect(reverse('snowboard-detail', kwargs={'pk': snowboard_id}) + '#reviews')

            review = form.save(commit=False)
            review.snowboard = Snowboard.objects.get(pk=snowboard_id)
            review.reviewer = request.user.profile
            review.save()
            review_posted = True
            messages.success(request, 'Review added.')
            return redirect(reverse('snowboard-detail', kwargs={'pk': snowboard_id}) + '#reviews')

    else:
        form = ReviewForm()
    print(review_posted)
    return render(request, 'snowReview/add_review.html', {'form': form, 'review_posted': review_posted, 'snowboard': snowboard})

    #Delete Review
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user.is_staff or request.user == review.reviewer.user:
        review.delete()
        messages.success(request, 'Review Deleted')
    return redirect('snowboard-detail', review.snowboard.id)


@login_required
def edit_review(request, review_id):
    # get review object
    review = get_object_or_404(Review, id=review_id)
    # if user is admin or post author
    if request.user.is_staff or request.user == review.reviewer.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, 'Review Updated')
                return redirect('snowboard-detail', review.snowboard.id)
        else:
            form = ReviewForm(instance=review)
        return render(request, 'snowReview/add_review.html', {'form': form, 'snowboard': review.snowboard})
    else:
        messages.error(request, 'You are not authorized to edit this review')
        return redirect('snowboard-detail', review.snowboard.id)