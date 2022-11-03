from datetime import datetime
from .models import ImagenReceta, Ingrediente, Receta
from .forms import RecetaForm
from django.shortcuts import render, redirect, get_object_or_404


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

    if 'night_mode' not in request.session:
        request.session['night_mode'] = True
    else:
        if request.session['night_mode'] == False: 
            request.session['night_mode'] = True
        else:
            request.session['night_mode'] = False

    request.session.modified = True
    #return render(request,'plantilla.html')
    return redirect(request.META['HTTP_REFERER'])

def receta_new(request):
    if request.method == "POST":
        form = RecetaForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = datetime.now()
            post.save()
            return redirect('receta', nombre=post.nombre)
    else:
        form = RecetaForm()
        
    return render(request, 'receta_edit.html', {'form': form})

def receta_edit(request,nombre):
    post = get_object_or_404(Receta,nombre=nombre)
    if request.method == "POST":
        form = RecetaForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = datetime.now()
            post.save()
            return redirect('receta', nombre=post.nombre)
    else:
        form = RecetaForm(instance=post)
    return render(request, 'receta_edit.html', {'form': form})

