import os
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from .forms import GuideForm
from snowReview.forms import SnowboardForm, CommentForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ReviewForm
from .models import Snowboard, Profile, Review, Comment, Terrain

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'

# Create your views here.
def index(request):
    # active query set
    snowboards = Snowboard.objects.all()
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
    # Check if the request method is POST
    if request.method == 'POST':
        # Create an instance of CustomAuthenticationForm with the POST data
        form = CustomAuthenticationForm(request, data=request.POST)

        # Validate the form
        if form.is_valid():
            # Get the cleaned data for 'username' and 'password'
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Authenticate the user
            user = authenticate(username=username, password=password)
            # If the user is authenticated
            if user is not None:
                # Log the user in
                login(request, user)
                # Show a success message
                messages.success(request, f'You are now logged in as {username}.')
                # Redirect to the home view
                return redirect('home_view')
            else:
                # Show an error message
                messages.error(request,"Invalid username or password.")
        else:
            # Show an error message
            messages.error(request,"Invalid username or password.")
    # Create an instance of CustomAuthenticationForm without any data
    form = CustomAuthenticationForm()
    # render the login page with the form
    return render(request = request, template_name = "registration/login.html", context={"login_form":form})

# logout view to log out the user and redirect to the home page
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home_view')

# The login_required decorator ensures that only logged-in users can access this view
@login_required
def profile_view(request):
    # Get the Profile object for the current user
    profile = Profile.objects.get(user=request.user)
    # Get all Comment objects for the current user, ordered by 'updated_at' in descending order
    comments = Comment.objects.filter(user=request.user).order_by('-updated_at')
    # If the user is a reviewer
    if profile.is_reviewer:
        # Get all Review objects for the current user
        reviews = Review.objects.filter(reviewer=profile)
    else:
        # Set 'reviews' to None
        reviews = None
    # Render the 'profile.html' template with the 'comments', 'reviews', and 'profile' context variables
    return render(request, 'snowReview/profile.html', {'comments': comments, 'reviews': reviews, 'profile': profile})

def do_nothing(request):
    return HttpResponse("This is a view that does nothing.")

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


# using the built in django detail view to show the snowboard details
class SnowboardDetailView(DetailView):
    model = Snowboard

# using the built in django update view to update the snowboard details
# Define a ListView for the Snowboard model
class SnowboardListView(ListView):
    model = Snowboard  # Specify the model to use
    template_name = 'snowReview/snowboard_list.html'  # Specify the template to use
    paginate_by = 12  # Specify the number of items to display per page

    # Override the get_queryset method to customize the queryset
    def get_queryset(self):
        # Get the 'shape' parameter from the GET request
        shape = self.request.GET.get('shape')
        # Get the 'terrain' parameter from the GET request as a list
        terrain_names = self.request.GET.getlist('terrain')
        # Get the 'season' parameter from the GET request, defaulting to an empty string if it's not present
        season = self.request.GET.get('season', '')

        # Get all Snowboard objects
        queryset = Snowboard.objects.all()

        # If a shape was specified in the GET request
        if shape:
            # Filter the queryset to only include Snowboards with that shape
            queryset = queryset.filter(shape=shape)

        # If one or more terrains were specified in the GET request
        if terrain_names:
            # Get all Terrain objects with those names
            terrains = Terrain.objects.filter(name__in=terrain_names)
            # Filter the queryset to only include Snowboards with those terrains
            queryset = queryset.filter(terrain__in=terrains)

        # If a season was specified in the GET request
        if season:
            # Filter the queryset to only include Snowboards from that season
            queryset = queryset.filter(season=season)

        # Return the filtered queryset
        return queryset

    # Override the get_paginate_by method to customize the number of items per page
    def get_paginate_by(self, queryset):
        # Get the 'items_per_page' parameter from the GET request, defaulting to self.paginate_by if it's not present
        items_per_page = self.request.GET.get('items_per_page', self.paginate_by)
        # If 'items_per_page' is not specified or is an empty string
        if not items_per_page:
            # Set 'items_per_page' to self.paginate_by
            items_per_page = self.paginate_by
        # Return 'items_per_page' as an integer
        return int(items_per_page)
    
    # Override the get_context_data method to add additional context variables
    def get_context_data(self, **kwargs):
        # Get the base context data from the superclass
        context = super().get_context_data(**kwargs)
        # Add the current user to the context
        context['user'] = self.request.user
        # Add a list of all possible snowboard shapes to the context
        context['shapes'] = [shape[0] for shape in Snowboard.SHAPES]

        # Get a list of all terrain names
        terrain_names = Terrain.objects.values_list('name', flat=True)
        # Split each terrain name into a list of names, resulting in a list of lists
        terrain_list = [name.split(', ') for name in terrain_names]
        # Flatten the list of lists and remove duplicates to get a list of unique terrain names
        unique_terrains = list(set(sum(terrain_list, [])))
        # Add the list of unique terrain names to the context
        context['terrains'] = unique_terrains
        # Add the list of selected terrains from the GET request to the context
        context['selected_terrains'] = self.request.GET.getlist('terrain')
        context['selected_season'] = self.request.GET.get('season', '')

        # If the user is authenticated
        if self.request.user.is_authenticated:
            # Get or create a Profile object for the current user and add it to the context
            context['profile'], created = Profile.objects.get_or_create(user=self.request.user)
        # Return the context
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
            shapes = [form.cleaned_data['shape']]  # Wrap the shape value in a list
            print(f"Shapes: {shapes}")  # Debug line
            if shapes:
                snowboards = snowboards.filter(shape__in=shapes)

    items_per_page = request.GET.get('items_per_page', 12)
    if not items_per_page:
        items_per_page = 12
    
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

# Define a view function for creating a new Snowboard
def createSnowboard(request):
    # If the request method is POST
    if request.method == 'POST':
        # Create an instance of SnowboardForm with the POST data and files
        form = SnowboardForm(request.POST, request.FILES)
        # Validate the form
        if form.is_valid():
            # Save the form, creating a new Snowboard
            form.save()
            # Redirect to the snowboard list view
            return redirect('snowboard-list')
        else:
            # Print the form errors for debugging purposes
            print(f"Form errors: {form.errors}")
    else:
        # If the request method is not POST, create an empty instance of SnowboardForm
        form = SnowboardForm()

    # Define the context for the template
    context = {'form': form, 'action': 'Add', 'object_type': 'Snowboard'}
    # Render the 'addBoard_form.html' template with the context
    return render(request, 'snowReview/addBoard_form.html', context)

# Define a view function for deleting a Snowboard
def delete_snowboard(request, snowboard_id):
    # If the user is authenticated and is a staff member
    if request.user.is_authenticated and request.user.is_staff:
        # Get the Snowboard with the given ID, or raise a 404 error if it doesn't exist
        snowboard = get_object_or_404(Snowboard, id=snowboard_id)
        # Delete the Snowboard
        snowboard.delete()
        # Show a success message
        messages.success(request, f'{snowboard} successfully deleted.')
        # Redirect to the snowboard list view
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
# The login_required decorator ensures that only logged-in users can access this view
@login_required(login_url='login')
def add_comment(request, snowboard_id):
    # Get the Snowboard with the given ID, or raise a 404 error if it doesn't exist
    snowboard = get_object_or_404(Snowboard, pk=snowboard_id)
    if request.method == "POST":
        # Print the POST data for debugging purposes
        print(request.POST)
        # Create an instance of CommentForm with the POST data
        form = CommentForm(request.POST)
        # Validate the form
        if form.is_valid():
            # Save the form, but don't commit to the database yet
            comment = form.save(commit=False)
            comment.user = request.user
            comment.snowboard = snowboard
            comment.save()
            messages.success(request, 'Comment added.')
            # Redirect to the snowboard detail view for the current snowboard
            return redirect('snowboard-detail', pk=snowboard.id)
        else:
            # Print the form errors for debugging purposes
            print(form.errors)
    else:
        # If the request method is not POST, create an empty instance of CommentForm
        form = CommentForm()
    # Render the 'snowReview/snowboard_detail.html' template with the 'snowboard' and 'form' context variables
    return render(request, 'snowReview/snowboard_detail.html', {'snowboard': snowboard, 'form': form})

@login_required(login_url='login')
def edit_comment(request, comment_id):
    # Get the comment or 404 if not found
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the user is staff or the author of the comment
    if request.user.is_staff or request.user == comment.user:
        if request.method == "POST":
            # Create form with POST data and existing comment instance
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                messages.success(request, 'Comment updated.')
                return redirect('snowboard-detail', pk=comment.snowboard.id)
            else:
                print(form.errors)
        else:
            # Create form with existing comment instance for GET request
            form = CommentForm(instance=comment)
        
        # Render the template with the snowboard, form, and comment context
        return render(request, 'snowReview/snowboard_detail.html', {'snowboard': comment.snowboard, 'form': form, 'comment': comment})
    else:
        messages.error(request, 'You do not have permission to edit this comment.')
        return redirect('snowboard-detail', pk=comment.snowboard.id)
    
# Delete Comment
def delete_comment(request, comment_id): 
    comment = get_object_or_404(Comment, id=comment_id) 
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