from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

def index(request):
    # Queries the Category model to retrive the top five categories; '-lies' in desceding order
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories':category_list,
    'pages':page_list}
    # Return a rendered response to send to the client
    return render(request, 'rango/index.html', context = context_dict)

def about(request):
    #return HttpResponse('Rango says here is the about page. <br/> <a href="http://127.0.0.1:8000/rango/">Index</a>')
    return render(request, 'rango/about.html')

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
