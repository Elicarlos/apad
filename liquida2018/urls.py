"""liquida2018 URL Configuration
"""
from django.urls import include, path
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from participante import urls as purls
from lojista import urls as lurls
from cupom import urls as curls
from bcp import urls as burls
from django.conf.urls import handler404, handler500

# handler404 = 'participante.views.not_found_page_view'
# handler500 = 'participante.views.server_error_view'

urlpatterns = [
    path('', include(purls)),
    path('op-admin-nimda-solu/', admin.site.urls),
    url('cupom/', include(curls, namespace='cupom')),
    path('lojista/', include(lurls, namespace='lojista')),
    path('barcode/', include(burls, namespace='bcp')),
    # python-social-auth
    #url('social-auth/', include('social.apps.django_app.urls', namespace='social')),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Administração Sorteio"
admin.site.site_title = "Sorteio"
admin.site.index_title = "Bem vindo a administração do Sorteio"
