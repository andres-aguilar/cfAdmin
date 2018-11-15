from django.conf.urls import url

from .views import edit_project
from .views import CreateProjectView, ListUserProjectsView, ShowProjectView, ListAllProjectsView, ListContributors

urlpatterns = [
    url(r'^$', ListAllProjectsView.as_view(), name='projects'),
    url(r'^mine/$', ListUserProjectsView.as_view(), name='my_projects'),
    url(r'^show/(?P<slug>[\w-]+)/$', ShowProjectView.as_view(), name='show'),
    url(r'^create/$', CreateProjectView.as_view(), name='create'),
    url(r'^edit/(?P<slug>[\w-]+)/$', edit_project, name='edit'),
    url(r'^contributors/(?P<slug>[\w-]+)/$', ListContributors.as_view(), name='contributors'),
]