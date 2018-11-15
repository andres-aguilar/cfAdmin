from django.conf.urls import url

from .views import DashboardView, LoginView, logout_view, EditSocialMediaView
from .views import CreateUserView, ShowUserView, edit_password,  edit_client, user_filter

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', logout_view, name='logout'),

    url(r'^show/(?P<username>\w+)/$', ShowUserView.as_view(), name='show'),
    url(r'^create/', CreateUserView.as_view(), name='create'),
    url(r'^edit/', edit_client, name='edit_client'),
    url(r'^edit_social/', EditSocialMediaView.as_view(), name='edit_social'),
    url(r'^edit_password/', edit_password, name='edit_password'),

    url(r'^filter$', user_filter, name='filter'),

    url(r'^dashboard/', DashboardView.as_view(), name='dashboard'),
]