from multiprocessing import context
from queue import Empty
from .models import ImagenReceta, Ingrediente, Receta
from django.shortcuts import  HttpResponse, render, redirect
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def index(request):
    return render(request,'plantilla.html')

def searchView(request):
    query_dict = request.GET
    query = query_dict.get('query')
    
    result = None

    if query!= '':
        result = Receta.objects.filter(nombre=query)

        if not result:
                ingres = Ingrediente.objects.filter(nombre=query)
                if ingres is not None:
                    result=[ingre.receta for ingre in ingres]



    context = {"result":result}
    return render(request,'search.html', context=context)


def recetaView(request, nombre):

    result = None
    imagenes = None

    if nombre!= '':
        result = Receta.objects.get(nombre=nombre)
        imagenes = ImagenReceta.objects.filter(receta=result)
    
    context = {"result":result, "imagenes":imagenes}
    return render(request,'receta.html', context=context)

def modeView(request):

    if request.session['night_mode'] == False or 'night_mode' not in request.session:
        request.session['night_mode'] = True
    else:
        request.session['night_mode'] = False

    request.session.modified = True
    #return render(request,'plantilla.html')
    return redirect(request.META['HTTP_REFERER'])
