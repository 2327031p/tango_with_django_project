from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # The dictionary passes to the template engine as its context
    # They key boldmessage is the same as {{ boldmessage }} in the template
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}

    # Return a rendered response to send to the client
    return render(request, 'rango/index.html', context = context_dict)

def about(request):
    return HttpResponse('Rango says here is the about page. <br/> <a href="http://127.0.0.1:8000/rango/">Index</a>')
