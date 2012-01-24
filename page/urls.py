from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('apartmentawesome.page.views',
   url(r'^$', 'index', name='page-index')
)