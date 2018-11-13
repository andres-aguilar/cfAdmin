from django.conf.urls import url

from .views import edit_project
from .views import CreateProjectView, ListProjectsView, ShowProjectView

urlpatterns = [
    url(r'^mine/$', ListProjectsView.as_view(), name='my_projects'),
    url(r'^show/(?P<slug>[\w-]+)/$', ShowProjectView.as_view(), name='show'),
    url(r'^create/$', CreateProjectView.as_view(), name='create'),
    url(r'^edit/(?P<slug>[\w-]+)/$', edit_project, name='edit'),
]