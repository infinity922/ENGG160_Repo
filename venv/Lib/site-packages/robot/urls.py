from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^robot/', include('robot.foo.urls')),

    # Uncomment this for admin:
	(r'^login/$', 'django.contrib.auth.views.login', 
		{ 'template_name' : 'robot/login.html' }),
	(r'^robot/$', 'robot.views.request_list'),
	(r'^robot/new/$', 'robot.views.request_new'),
	(r'^robot/([0-9]+)/$', 'robot.views.request_view'),
	(r'^robot/([0-9]+)/txt/$', 'robot.views.request_txt'),
	(r'^admin/', include('django.contrib.admin.urls')),
)
