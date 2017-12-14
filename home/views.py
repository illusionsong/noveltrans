from django.shortcuts import render

from django.http import HttpResponse
from django.http.response import HttpResponseRedirect, HttpResponse


from selenium import webdriver
from bs4 import BeautifulSoup

import time
import pymysql
import json
import MySQLdb

import re
import os



from home.controll.controller import Control



from home.controll.novel_content_insertAll import novel_content_insertAll




def dddd(request):

    # driver = webdriver.PhantomJS('C:/Users/egnis/trans/phantomjs/bin/phantomjs')
    # driver.get('http://sitetrans.naver.net/?rel=http://trpgclub.com/log2/a.php?index_code=%s&page=%s&srcLang=ja&tarLang=ko' % (101, 1))





    return render(request, 'home/index.html')



#로그인하기 (임시로 바로 로그인 상태로 전환됨
def login(request):


    request.session['id'] = 'idIN'

    return HttpResponseRedirect('index')
    # return render(request, 'home/index.html')


#로그아웃하기 (임시로 바로 로그인 상태로 전환됨
def logout(request):


    del request.session['id']

    return HttpResponseRedirect('index')
    # return render(request, 'home/index.html')



# Create your views here.
def index(request):
    msg = 'My Message'
    return render(request, 'home/index.html', {'message': msg})



def tttt(request):


    driver = webdriver.PhantomJS(os.getcwd() + '/phantomjs/bin/phantomjs')
    driver.implicitly_wait(4)

    driver.get('https://novel18.syosetu.com/n8897dt/2')
    driver.implicitly_wait(4)

    #19금 판넬 채크
    element = driver.find_element_by_id("yes18").click()

    driver.get('https://novel18.syosetu.com/n8897dt/2')
    driver.implicitly_wait(4)


    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')


    # 각 제목들 따옴
    #notices = soup.select('dd.subtitle')
    novel_content = soup.find(id="novel_honbun")




    return render(request, 'home/index.html', {'res':str(novel_content)})








#view단 제어




#소설번역요청 페이지 view 제어
def Cont_novel_trans_req(request):

    return render(request, 'home/input.html')


# 들어가있는 소설 리스트 보여주기 view 제어
def Cont_novel_list(request):
    mvc = Control()

    res = mvc.Cont_novel_list(request)

    return render(request, 'home/list.html', {'res': res})



#들어가있는 소설 하나의  페이지 보여주기
def Cont_novel_page_list(request,title):

    mvc = Control()
    res = mvc.novel_page_list(request,title)

    return render(request, 'home/page.html',{'res' : res, 'title' : title})



#들어가있는 소설 내용 보여주기
def Cont_novel_content_view(request,title,num):

    mvc = Control()
    res = mvc.novel_content_list(request, title,num)


    return render(request, 'home/view.html', {'value' : res})



#소설 초기화 작업 페이지
def Cont_novel_contente_reset(request):

    conn = pymysql.connect(host='logtest3.c7rrpzvpygvb.ap-northeast-2.rds.amazonaws.com', user='admin',
                                password='logtest3password',
                                db='trans', charset='utf8')

    curs = conn.cursor(pymysql.cursors.DictCursor)



    sql =   'SELECT index_code, novel_address, novel_siteTag, novel_name_kor FROM trans.novel_label;	'

    curs.execute(sql)

    # 삽입
    conn.commit()

    res = curs.fetchall()





    return render(request, 'home/reset.html',{'res':res})




# view 단 정리 끝

#######################################################################################################################################################################################################################


#논리단


# 소설 새로운 책갈피 만들고 원본따고 번역처리함
def novel_label_insert(request):



    mvc = Control()
    res = mvc.novel_label_insert(request)

    return render(request, 'home/index.html', {'message': res})





def pix(request):
    mvc = Control()
    res = mvc.PixC(request)


    return render(request, 'home/index.html', {'res': res})



def pixin(request):


    # 스레딩 테스트
    t = novel_content_insertAll(
        {
            'novel_siteTag': 'pixiv'
            , 'novel_address_code': 48
        }

    )

    t.start()


    res= 'comp'

    return render(request, 'home/index.html', {'res': res})




    '''

    timeout   =  10

    try:

        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'caption'))

        WebDriverWait(driver, timeout).until(element_present)

        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")

    


    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # novel   =   soup.find_all(id=True)


    #novel_title = soup.find_all('a')
    #novel_title = soup.find(class_='layout-body')
    #novel_title = soup.select('div')
    #aa = driver.find_element_by_tag_name('li')


    '''








#소설 초기화작업요청
def novel_reset(request):

    index_code = request.POST.get('index_code')


    conn = pymysql.connect(host='logtest3.c7rrpzvpygvb.ap-northeast-2.rds.amazonaws.com', user='admin',
                           password='logtest3password',
                           db='trans', charset='utf8')

    curs = conn.cursor(pymysql.cursors.DictCursor)

    sql = '''
            SELECT index_code, novel_address, novel_siteTag, novel_name_kor, novel_address_code 
                    FROM trans.novel_label
                   where index_code = %s
            '''
    curs.execute(sql,index_code)

    novelData = curs.fetchall()


    index_code = request.POST.get('index_code')

    sql = """
           delete from novel_content
                where novel_index_code	=	%s
       """
    curs.execute(sql, index_code)
    conn.commit()


    data    =   {'novel_siteTag' : novelData[0]['novel_siteTag']
                ,'novel_address' : novelData[0]['novel_address']
                , 'novel_address_code': novelData[0]['novel_address_code']

                 }

    mvc =   Control()
    a = mvc.novel_content_insert(request,data)

    return render(request, 'home/index.html')




#1페이지만 갱신
def novel_content_update(request,title,num):

    mvc = Control()

    data = {'novel_address': title
            ,'num' : num
            , 'novel_siteTag' : 'ncode'}

    mvc.novel_content_update(request, data)

    return render(request, 'home/index.html')





#원 사이트와 들어가있는 소설 분량 채크
#차이가 발생할경우 소설 신규 업데이트라 보고 다음 트리거 실행
def novel_label_check(request):


    mvc =   Control()

    a   =   mvc.novel_label_check(request)



    return render(request, 'home/index.html')

#소설 분량 채크리스트 처리
def novel_IncomingList_commit(request):


    mvc =   Control()

    a   =   mvc.novel_IncomingList_commit(request)



    return render(request, 'home/index.html')