from django.conf.urls import url
from . import views
from django.contrib.auth.views import *
from django.urls import path, re_path
from django_filters.views import FilterView
from .filters import UserFilter
from .models import Profile
from django.conf.urls import handler404, handler500
from django.urls import reverse_lazy
# from participante.views import gerarticket
from django.contrib.auth.views import LoginView, LogoutView
app_name = 'participante'
from .views import consulta_cep

urlpatterns = [
    # url(r'^login/$', views.user_login, name='login'),
    path('login/', views.homepage, name='login'),
    path('logout/', LogoutView.as_view(next_page='participante:homepage'), name='logout'),
    #Relatorios
    path('dados_campanha/', views.dados_campanha, name="dados_campanha"),
    path('checkout/', views.checkout, name="checkout"),
    path('checkout/pagamento/',  views.pagamento, name='pagamento'),
    path('confirmacao_pagamento/<int:transacao_id>/', views.confirmacao_pagamento, name='confirmacao_pagamento'),
    path('resumo_lojistas/', views.resumo_lojistas, name='resumo_lojistas'),
    path('relatorios_camp/', views.relatorios_camp, name='relatorios_camp'),
    path('graficos/', views.graficos, name="graficos"),
    path('', views.homepage, name='homepage'),
    path('main/', views.main_page, name='main_page'),
    path('dash/', views.dashboard, name='dashboard'),
    #path('lojista/', views.lojista, name='notfound'),
    # path('search/', FilterView.as_view(filterset_class=UserFilter,
    #     template_name='participante/participante_list.html'), name='search'),
    path('search/', views.search, name='search'),
    path('participante/cpf', views.search_by_cpf, name='search_by_cpf'),

    url(r'^list$', views.participante_list, name='list'),
    path('backoffice/', views.backoffice, name='backoffice'),
    path('impressao/', views.print_detail, name='impressao'),


    re_path(r'^participante/(?P<id>[-\w]+)/$', views.user_detail, name='user_detail'),
    re_path(r'^participante/edit/(?P<id>[-\w]+)/$', views.user_edit, name='user_edit'),
    # Coupons paths
    path('docsfiscais/', views.doclist, name='docsfiscais'),

    # Coupons paths
    path('coupons/', views.coupons, name='coupons'),


    # Premios paths
    path('premios/', views.premios, name='premios'),


    # path('cadastrar/', views.register, name='register'),
    # Removido final de campanha
    path('cadastro/', views.register, name='register'),
    path('register/', views.register2, name='register-op'),
    path('edit/', views.edit, name='edit'),

    # Documentos Fiscais paths
    # Removido para final da campanha
    path('adddocfiscal/', views.adddocfiscal, name='adddocfiscal'),
    re_path(r'^adddocfiscal/(?P<id>[-\w]+)/$', views.adddocfiscalbyop, name='adddocfiscalbyop'),
    path('editdocfiscal/', views.editdocfiscal, name='editdocfiscal'),
    re_path(r'^editdocfiscal/(?P<id>[-\w]+)/$', views.editdocfiscal, name='editdocfiscal'),
    re_path(r'^editdocfiscalbyop/(?P<id>[-\w]+)/$', views.editdocfiscalbyop, name='editdocfiscalbyop'),
    re_path(r'^validadocfiscal/(?P<id>[-\w]+)/$', views.validadocfiscal, name='validadocfiscal'),

    # login / logout paths
    # path('login/', login, name='login'),
    # path('logout/', logout, name='logout'),
    path('logout-then-login/', logout_then_login, name='logout_then_login'),    

    # change password paths
    url(r'^password-change/$', PasswordChangeView.as_view(
        template_name= 'registration/password_change_form.html',
        success_url = 'done/'),name='password_change'),
    url(r'^password-change/done/', PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html', extra_context=None
        ),name='password_change_done'),


    # restore password paths
    url(r'^password-reset/$',PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        success_url = reverse_lazy('participante:password_reset_done')),name='password_reset'),
    url(r'^password-reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html', extra_context=None
       ), name='password_reset_done'),

    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'
        , success_url=reverse_lazy('participante:password_reset_complete')), name='password_reset_confirm'),
    url(r'^password-reset/complete/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html',  extra_context=None
        ), name='password_reset_complete'),


    path('consulta-cep/', consulta_cep, name='consulta_cep'),

    #TICKET
    # path('gerarticket/', views.gerarticket, name='gerarticket'),

]


# handler404 = 'views.not_found_page_view'
# handler500 = 'views.server_error_view'


