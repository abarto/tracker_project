from django.conf.urls import patterns, url

from .views import (
    incident_list, incident_detail, incident_create, incident_update, incident_delete,
    area_of_interest_list, area_of_interest_detail, area_of_interest_create, area_of_interest_update,
    area_of_interest_delete, incident_feature_collection, area_of_interest_feature_collection,
    report_incident, report_incident_success, incident_export_report
)

urlpatterns = patterns(
    '',
    url(r'^incident/$', incident_list, name='incident-list'),
    url(
        r'^incident/feature_collection/$',
        incident_feature_collection,
        name='incident-feature-collection'
    ),
    url(r'^incident/(?P<pk>\d+)/$', incident_detail, name='incident-detail'),
    url(r'^incident/create/$', incident_create, name='incident-create'),
    url(r'^incident/report/$', report_incident, name='report-incident'),
    url(r'^incident/report_success/$', report_incident_success, name='report-incident-success'),
    url(r'^incident/update/(?P<pk>\d+)/$', incident_update, name='incident-update'),
    url(r'^incident/delete/(?P<pk>\d+)/$', incident_delete, name='incident-delete'),
    url(r'^incident/export_report$', incident_export_report, name='incident-export-report'),
    url(r'^area_of_interest/$', area_of_interest_list, name='area-of-interest-list'),
    url(
        r'^area_of_interest/feature_collection/$',
        area_of_interest_feature_collection,
        name='area-of-interest-feature-collection'
    ),
    url(r'^area_of_interest/(?P<pk>\d+)/$', area_of_interest_detail, name='area-of-interest-detail'),
    url(r'^area_of_interest/create/$', area_of_interest_create, name='area-of-interest-create'),
    url(r'^area_of_interest/update/(?P<pk>\d+)/$', area_of_interest_update, name='area-of-interest-update'),
    url(r'^area_of_interest/delete/(?P<pk>\d+)/$', area_of_interest_delete, name='area-of-interest-delete'),
)