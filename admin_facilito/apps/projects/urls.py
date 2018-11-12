from django.conf.urls import url

from .views import CreateProjectView

urlpatterns = [
    url(r'^create/$', CreateProjectView.as_view(), name='create')
]