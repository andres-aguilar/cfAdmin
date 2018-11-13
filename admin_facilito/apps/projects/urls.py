from django.conf.urls import url

from .views import CreateProjectView, ListProjectsView, ShowProjectView
from .views import edit_project

urlpatterns = [
    url(r'^create/$', CreateProjectView.as_view(), name='create'),
    url(r'^projects/$', ListProjectsView.as_view(), name='my_projects'),
    url(r'^edit/(?P<slug>[\w-]+)/$', edit_project, name='edit'),
    url(r'^show/(?P<slug>[\w-]+)/$', ShowProjectView.as_view(), name='show'),
]