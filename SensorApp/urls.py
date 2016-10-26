from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin
from SensorApp import views
from SensorApp.views import SignalDataList
admin.autodiscover()


urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r'^create_user/$', views.create_user, name='create_user_api'),
    url(r'^login_user/$', views.login_user, name='login_user_api'),
    url(r'^save_signal_data/$', views.save_signal_data, name='save_signal_data_api'),
    url(r'^signal_data/$', SignalDataList.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
