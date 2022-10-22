from multiprocessing import context
from .models import Receta
from django.shortcuts import  HttpResponse, render

# Create your views here.

def index(request):
    return render(request,'plantilla.html')

def searchView(request):
    query_dict = request.GET
    query = query_dict.get('query')
    
    result = None

    if query!= '':
        result = Receta.objects.get(nombre=query)


    context = {"result":result}
    return render(request,'search.html', context=context)
