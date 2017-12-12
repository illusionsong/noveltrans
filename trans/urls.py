"""trans URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from home import views

urlpatterns = [

    url(r'^admin/', admin.site.urls),

    url(r'^$', views.index),
    url(r'index', views.index , name='index'),
    url(r'^ni', views.tttt),


    url(r'^dddd', views.dddd),
    url(r'^tttt', views.tttt),







    #mvc view단 제어리스트


    #로그인 호출
    url(r'^login'              ,     views.login            ,name = 'login'),
    url(r'^logout'              ,     views.logout          ,name = 'logout'),






    #들어가있는 소설 리스트 불러오기
    url(r'^novel_list'              , views.Cont_novel_list                                          ,name = 'novel_list'),




    #소설 번역 요청 페이지 불러오기
    url(r'^novel_trans_req'        , views.Cont_novel_trans_req                                     ,name = 'novel_trans_req'),

    #번역된 소설 한개의 전편 가져오기
    url(r'^novel_page_list/(?P<title>\w+)/', views.Cont_novel_page_list                           ,name = 'novel_page_list'),


    #번역된 소설 한개의 한 편 내용 가져오기
    url(r'^novel_content_view/(?P<title>\w+)/(?P<num>\d+)/$', views.Cont_novel_content_view     ,name = 'novel_content_view'),






    url(r'^novel_content_update/(?P<title>.+)/(?P<num>\d+)/$', views.novel_content_update),

    #번역된 소설 한개의 내용 초기화(원본 사이트의 내용으로 교채)
    url(r'^novel_contente_reset', views.Cont_novel_contente_reset                                     ,name  =   'novel_contente_reset'),



    #view단 제어 끝



    #논리단 제어


    #url(r'pix', views.pix),

    url(r'pixin', views.pixin),





    #url(r'^novel_label_input^$', views.novel_label_input),
    url(r'^novel_label_insert', views.novel_label_insert),
    url(r'^novel_IncomingList_commit', views.novel_IncomingList_commit),





    url(r'^novel_reset', views.novel_reset),



    #업데이트 리스트 만들기(전부 채크)
    url(r'^novel_label_check', views.novel_label_check , name='novel_label_check'),
    # url(r'^novel_label_check/(?P<index_code>\d+)', views.novel_label_check , name='novel_label_check'),

    #업데이트 리스트 처리
    url(r'^novel_IncomingList_commit', views.novel_IncomingList_commit, name='novel_IncomingList_commit'),











]
