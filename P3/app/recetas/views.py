from .models import ImagenReceta, Ingrediente, Receta
from .forms import RecetaForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test

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

@user_passes_test(lambda u: u.is_superuser, redirect_field_name=None)
def receta_new(request):

    titulo = "Nueva receta"

    if request.method == "POST":
        form = RecetaForm(request.POST)
        if form.is_valid():

            '''
            nombre = form.cleaned_data['nombre']

            try:
                Receta.objects.get(nombre=nombre)
                messages.error(request, "La receta con nombre "+nombre+" ya existe")
            except ObjectDoesNotExist:
                receta = form.save()
                messages.success(request, 'La receta '+ receta.nombre +' ha sido añadida')
                return redirect('receta', nombre=receta.nombre)
            '''
            receta = form.save()
            messages.success(request, 'La receta '+ receta.nombre +' ha sido añadida')
            return redirect('receta', nombre=receta.nombre)

    else:
        form = RecetaForm()
        
    return render(request, 'receta_edit.html', {'form': form, 'titulo': titulo})


@staff_member_required(login_url='/accounts/login/',redirect_field_name=None)
def receta_edit(request,nombre):
    titulo = "Editar receta"

    receta = Receta.objects.get(nombre=nombre)

    if request.method == "POST":
        #Después de esto, receta ya ha cambiado de valores a los valores del formulario
        form = RecetaForm(request.POST, instance=receta)
        if form.is_valid():
            
            '''
            nombre_form = form.cleaned_data['nombre']

            #Si el nombre nuevo introducido no coincide con el actual (que es nombre y no receta.nombre pues receta.nombre ya está cambiada)
            if nombre_form!=nombre:
                try:
                    #Y existe ya una receta en la base de datos con el mismo nombre, dar mensaje de error y volver a renderizar view de edición
                    Receta.objects.get(nombre=nombre_form)
                    messages.error(request, "La receta con nombre "+nombre_form+" ya existe")
                    return render(request, 'receta_edit.html', {'form': form, 'titulo': titulo})
                except ObjectDoesNotExist:
                    pass
            '''
            
            #En otro caso, el nombre es el mismo o no está en la base de datos, luego se guarda los datos
            receta = form.save()
            messages.success(request, 'La receta '+ nombre + ' ha sido editada')
            return redirect('receta', nombre=receta.nombre)
            
    else:
        form = RecetaForm(instance=receta)
    
    #Comtemplar el caso de que el form no es válido
    return render(request, 'receta_edit.html', {'form': form, 'titulo': titulo})

@user_passes_test(lambda u: u.is_superuser, redirect_field_name=None)
def receta_delete(request,nombre):
    receta = get_object_or_404(Receta,nombre=nombre)
    receta.delete()
    messages.success(request, 'La receta ' + receta.nombre + ' ha sido eliminada')
    return redirect('/result/')
