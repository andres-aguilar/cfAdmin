from django.conf.urls import url

from .views import DashboardView, LoginView, logout_view
from .views import CreateUserView, ShowUserView, EditUserView, edit_password

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', logout_view, name='logout'),

    url(r'^show/(?P<username>\w+)/$', ShowUserView.as_view(), name='show'),
    url(r'^create/', CreateUserView.as_view(), name='create'),
    url(r'^edit/', EditUserView.as_view(), name='edit'),
    url(r'^edit_password/', edit_password, name='edit_password'),
    url(r'^dashboard/', DashboardView.as_view(), name='dashboard'),
]