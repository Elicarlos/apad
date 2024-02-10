from django.conf.urls import url
from . import views
from django.urls import path, re_path
from django.conf.urls import handler404, handler500

app_name = 'cupom'

urlpatterns = [
    # cupom urlpatterns = [
    #path('', views.addcupom, name='detail'),
    re_path(r'^(?P<numerodocumento>[-\w]+)/$', views.addcupom, name='addcupom'),
    re_path(r'^cupons/(?P<username>[-\w]+)/$', views.cupomlist, name='list'),
]

# handler404 = 'participante.views.not_found_page_view'
# handler500 = 'participante.views.server_error_view'
