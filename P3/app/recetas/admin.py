from django.contrib import admin
from .models import Receta, Ingrediente, ImagenReceta
# Register your models here.

class ImagenRecetaAdmin(admin.StackedInline):
    model = ImagenReceta
    extra = 0

class RecetaAdmin(admin.ModelAdmin):
    inlines = [ImagenRecetaAdmin]


admin.site.register(ImagenReceta)
admin.site.register(Ingrediente)
admin.site.register(Receta,RecetaAdmin)
