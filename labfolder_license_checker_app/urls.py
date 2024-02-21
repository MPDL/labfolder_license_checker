from django.conf.urls import include
from django.urls import re_path

from labfolder_license_checker_app import views

urlpatterns = [

    re_path(r'^$', views.instance_overview, name='view_instances'),

    re_path(r'add_report/$', views.add_report, name='add_report'),

    re_path(r'add_reports_batch/$', views.add_reports_batch, name='add_reports_batch'),

    re_path(r'instance/(?P<instance_id>[a-zA-Z0-9_-]+)/$', views.view_instance, name='view_instance')

    #url(r'^show/(?P<slug>[a-zA-Z0-9_-]+)/$', views.show_survey, name='show_survey_page'),

    #url(r'^api/', include(router.urls)),

    #url(r'^api/surveys/(?P<pk>[0-9]+)/questions/$', views.api_survey_questions, name='api-survey-questions'),

    #url(r'^api/surveys/(?P<pk>[0-9]+)/answer/$', views.api_survey_answer, name='api-survey-answer')
]