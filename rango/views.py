from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index(request):
    # Queries the Category model to retrive the top five categories; '-lies' in desceding order
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories':category_list,
    'pages':page_list}
    # Return a rendered response to send to the client
    return render(request, 'rango/index.html', context = context_dict)

def about(request):
    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in, prints 'AnonymousUser'
    print(request.user)
    #return HttpResponse('Rango says here is the about page. <br/> <a href="http://127.0.0.1:8000/rango/">Index</a>')
    return render(request, 'rango/about.html', {})

def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages. 
        # filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages

        # Also add the category object from the database to the context dictionary
        # Use this in the template to verify that the category exists
        context_dict['category'] = category

    except Category.DoesNotExist:
        # Got here if we didn't find the specified category
        context_dict['category'] = None
        context_dict['pages'] = None
    
    # Go render the response and return it to the client
    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    # A HTTP POST? Check if the user submitted data via the form
    # POST reqiest supply additional data from the client(browser) 
    # to the server in the message body
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database
            form.save(commit=True)
            # Direct the user back to the index page.
            return index(request)
        else:
            # If the supplied form had errors print them to the terminal
            print(form.errors)

    # Will handle the bad form, new form, or no form supllied cases
    # Render the form with errors messages (if any)
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'category':category, 'category_name_slug': category_name_slug}
    return render(request, 'rango/add_page.html', context_dict)


def register(request):
    # A boolean value for telling the template
    registered = False

    # If it's a HTTP POST, we're interested in processing form data
    if request.method == 'POST':
        # Attempt to grab information from raw form information.
        # Note that we make use of both USerForm and UserProfileForm
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # if the two forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # save the users form data to the database
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            # Sort out the UserProfile instance. Since you need to set the user
            # attribute yourself, set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # Sorting out the profile picture
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            #Invalid form or forms; print problems to the terminal
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so render the form using two ModelForm instances
        # These forms will be blank, ready for user input
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', 
                            {'user_form' : user_form,
                            'profile_form' : profile_form,
                            'registered': registered})


def user_login(request):
    if request.method == 'POST':
        # request.POST.get('variable') will return None if the value doesnt exist
        username = request.POST.get('username')
        password = request.POST.get('password')

        # see if the combination is valid - User object is returned if it is
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")

        else:
            # Bad login details
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login  details supplied.")

        # The requets is not HTTP POST, so display the login form
    else:
            # No context variabels to pass to the template system, hence 
            # the blank dictionary object..
            return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))