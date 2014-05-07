'''
Created on 04/03/2014

@author: chengyu
'''
from django.conf.urls import patterns, url
from webPart import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^detailRegion$',views.regionDetail, name="detailRegion")

                       )