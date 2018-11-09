from django.conf.urls import url

from .views import view, login_view, logout_view

urlpatterns = [
    url(r'^show/', view, name='show'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^dashboard/', view, name='dashboard'),
]