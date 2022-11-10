from datetime import datetime
from .models import ImagenReceta, Ingrediente, Receta
from .forms import RecetaForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

# Create your views here.

def index(request):
    if 'night_mode' not in request.session:
        request.session['night_mode'] = False
    return render(request,'plantilla.html')

def searchView(request):
    query_dict = request.GET
    query = query_dict.get('query')
    
    result = Receta.objects.all()

    if query!= '' and query!=None:
        qset = (Q(nombre__contains=query))
        result = Receta.objects.filter(qset).distinct()

        if not result:
                ingres = Ingrediente.objects.filter(nombre=query)
                if ingres is not None:
                    result=[ingre.receta for ingre in ingres]

    context = {"result":result, "query":query}
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

    if 'night_mode' not in request.session:
        request.session['night_mode'] = True
    else:
        if request.session['night_mode'] == False: 
            request.session['night_mode'] = True
        else:
            request.session['night_mode'] = False

    request.session.modified = True
    return redirect(request.META['HTTP_REFERER'])

def receta_new(request):
    if request.method == "POST":
        form = RecetaForm(request.POST)
        if form.is_valid():            
            receta = form.save()
            messages.success(request, 'La receta '+ receta.nombre +' ha sido añadida')
            return redirect('receta', nombre=receta.nombre)
    else:
        form = RecetaForm()
        
    return render(request, 'receta_edit.html', {'form': form, 'titulo': "Nueva receta"})

def receta_edit(request,nombre):
    receta = get_object_or_404(Receta,nombre=nombre)
    if request.method == "POST":
        form = RecetaForm(request.POST, instance=receta)
        if form.is_valid():
            receta = form.save()
            messages.success(request, 'La receta '+ receta.nombre + ' ha sido editada')
            return redirect('receta', nombre=receta.nombre)
    else:
        form = RecetaForm(instance=receta)
    return render(request, 'receta_edit.html', {'form': form, 'titulo': "Editar receta"})


def receta_delete(request,nombre):
    receta = get_object_or_404(Receta,nombre=nombre)
    receta.delete()
    messages.success(request, 'La receta ' + receta.nombre + ' ha sido eliminada')
    return redirect('/result/')
