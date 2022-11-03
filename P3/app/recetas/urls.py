from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('result/', views.searchView, name="result"),
    path('receta/<nombre>/', views.recetaView, name="receta"),
    path(' ', views.modeView, name="mode_switch")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)