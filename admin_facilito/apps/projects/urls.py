from django.conf.urls import url

from .views import CreateProjectView, ListProjectsView, ShowProjectView

urlpatterns = [
    url(r'^create/$', CreateProjectView.as_view(), name='create'),
    url(r'^projects/$', ListProjectsView.as_view(), name='my_projects'),
    url(r'^show/(?P<slug>[\w-]+)/$', ShowProjectView.as_view(), name='show'),
]