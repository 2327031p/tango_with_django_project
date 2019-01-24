from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page

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

