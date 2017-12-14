from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from bs4 import BeautifulSoup

import time
import pymysql
import json
import MySQLdb

import re
import os

import threading



from home.controll.novel_content_commit_ori import novel_content_commit_ori
from home.controll.novel_content_commit_fragment_ori import novel_content_commit_fragment_ori


class Control():

    def __init__(self):

        #self.driver = webdriver.PhantomJS('C:/Users/egnis/trans/phantomjs/bin/phantomjs')
        self.driver = webdriver.PhantomJS(os.getcwd() + '/phantomjs/bin/phantomjs.exe')

        self.conn = pymysql.connect(host='logtest3.c7rrpzvpygvb.ap-northeast-2.rds.amazonaws.com', user='admin',
                               password='logtest3password',
                               db='trans', charset='utf8')

        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)


    def __str__(self):
        print('ab')




    #픽시브 처리
    def PixC(self,request):

        # 로그인 제어
        self.driver.get('https://accounts.pixiv.net/login?lang=ko&source=pc&view_type=page&ref=wwwtop_accounts_index')
        # driver.get('https://www.pixiv.net/novel/show.php?id=1206710')
        self.driver.implicitly_wait(5)

        # driver.find_element_by_name('id').send_keys('dpga@naver.com')

        self.driver.find_element_by_xpath("//div[@id='container-login']/div/form/div/div[1]/input").send_keys('dpga@naver.com')
        self.driver.find_element_by_xpath("//div[@id='container-login']/div/form/div/div[2]/input").send_keys('qazwsx123')
        self.driver.find_element_by_xpath("//div[@id='container-login']/div/form/button").click()

        # 로그인 종료



        # 페이지 1화 이동후 전 리스트 뽑아옴
        time.sleep(3)
        self.driver.get('https://www.pixiv.net/novel/show.php?id=1206710')
        self.driver.implicitly_wait(5)
        time.sleep(3)

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        novel_url = soup.find(class_='area_new').find_all('a')








        # 책갈피 생성후 삽입
        sql = """
                insert into	novel_label( novel_address, novel_address_code, novel_siteTag, novel_name_ori, novel_name_kor) values(%s,%s,%s,%s,%s)
            """
        # 책갈피 생성
        self.curs.execute(sql, ('https://www.pixiv.net/novel/show.php?id=1206710', 'pixiv', 'pixiv', '픽시브오리', '픽시브번역'))


        #픽시브의 링크 따오는 첫번째,마지막는 매인링크로 가기때문에 0,마지막 자를것
        del novel_url[0]
        del novel_url[len(novel_url)-1]
        
        i=0


        

        for url in novel_url:


            url = 'https://www.pixiv.net' + novel_url[i].get('href')

            #각 페이지 글따오기
            self.driver.get(url)
            self.driver.implicitly_wait(5)
            time.sleep(3)

            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')




            #소설 본문
            novel_content_ori = str((soup.find_all(class_='novel-page'))[0])

            #소설 화당 제목
            novel_pageTitle_ori = (soup.find_all('h1',class_='title'))[1].get_text()
            
            sql = """
                    insert into novel_content(novel_content_ori, novel_pageTitle_ori, novel_page, novel_content_url , novel_index_code)  values(%s , %s , %s , %s ,
        
                                    (select index_code 
                                        from novel_label 
                                        where novel_siteTag	= %s
                                    )
                                )
                """

            self.curs.execute(sql, (novel_content_ori ,novel_pageTitle_ori , i, url , 'pixiv') )


            i= i+1

         #for 종료


        # 페이지 내용
        # driver.get('https://www.pixiv.net%s'  %urlt)

        #novel = soup.find_all(class_='novel-page')

        self.conn.commit()

        return render(request, 'home/index.html', {'res': novel_pageTitle_ori})





    #소설 책갈피 만들기 작업
    def novel_label_insert(self,request):

        url = request.POST.get('url')

        novel_adult_check = request.POST.get('novel_adult_check')


        if url.find('pixiv') != -1:


            siteType = 'pixiv'


            # 로그인 제어
            self.driver.get('https://accounts.pixiv.net/login?lang=ko&source=pc&view_type=page&ref=wwwtop_accounts_index')
            # driver.get('https://www.pixiv.net/novel/show.php?id=1206710')
            self.driver.implicitly_wait(5)

            self.driver.find_element_by_xpath("//div[@id='container-login']/div/form/div/div[1]/input").send_keys('dpga@naver.com')
            self.driver.find_element_by_xpath("//div[@id='container-login']/div/form/div/div[2]/input").send_keys('qazwsx123')
            self.driver.find_element_by_xpath("//div[@id='container-login']/div/form/button").click()

            # 로그인 종료



            # 페이지 1화 이동후 전 리스트 뽑아옴
            time.sleep(3)

            self.driver.get(url)
            self.driver.implicitly_wait(5)
            time.sleep(3)

            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            novel_url = soup.find(class_='area_new').find_all('a')

            # 책갈피 생성후 삽입
            sql = """
                    insert into	novel_label( novel_address, novel_address_code, novel_siteTag, novel_name_ori , novel_adult_check) values(%s,%s,%s,%s ,%s)
                """
            # 책갈피 생성
            self.curs.execute(sql,   (url, 'pixiv', siteType , '픽시브오리', 0 )    )

            # 픽시브의 링크 따오는 첫번째,마지막는 매인링크로 가기때문에 0,마지막 자를것
            del novel_url[0]
            del novel_url[len(novel_url) - 1]

            i = 0

            for url in novel_url:
                url = 'https://www.pixiv.net' + novel_url[i].get('href')

                # 각 페이지 글따오기
                self.driver.get(url)
                self.driver.implicitly_wait(5)
                time.sleep(3)

                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                # 소설 본문
                novel_content_ori = str((soup.find_all(class_='novel-page'))[0])

                # 소설 화당 제목
                novel_pageTitle_ori = (soup.find_all('h1', class_='title'))[1].get_text()

                sql = """
                            insert into novel_content(novel_content_ori, novel_pageTitle_ori, novel_page, novel_content_url , novel_index_code)  values(%s , %s , %s , %s ,

                                            (select index_code 
                                                from novel_label 
                                                where novel_siteTag	= %s
                                            )
                                        )
                        """

                self.curs.execute(sql, (novel_content_ori, novel_pageTitle_ori, i, url, 'pixiv'))

                i = i + 1

                # for 종료

            # 페이지 내용
            # driver.get('https://www.pixiv.net%s'  %urlt)

            # novel = soup.find_all(class_='novel-page')

            self.conn.commit()






        elif    (url.find('ncode') != -1 ) or   (url.find('novel18.syosetu') != -1 )   :

            siteType = 'ncode'


            #마지막에 / 들어가있을 경우
            if url[ len(url) -1] == '/':
                indexControl    =   -2
            else:
                indexControl    =   -1

            novel_address_code = url.split('/')[    len( url.split('/'))  + indexControl ]



            #19금 되자소설일경우
            #1이면 성인
            if novel_adult_check == '1' or novel_adult_check == 1:

                novel_address = 'https://novel18.syosetu.com/%s/' % novel_address_code


            else:

                novel_address = 'https://ncode.syosetu.com/%s/' % novel_address_code



            self.driver.get(novel_address)

            # 대기
            time.sleep(4)



            # 19금 인증 넘어가기
            if novel_adult_check == '1' or novel_adult_check == 1:
                self.driver.implicitly_wait(5)

                self.driver.find_element_by_xpath("//a[@id='yes18']").click()

                self.driver.get(novel_address)

                self.driver.implicitly_wait(3)
                time.sleep(3)



            #self.driver.switch_to.frame('main_frame')

            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # 원문제목
            novel_name_ori = soup.title.string

            # 책갈피 생성후 삽입
            sql = """
                    insert into	novel_label( novel_address, novel_address_code, novel_siteTag, novel_name_ori , novel_adult_check) values(%s,%s,%s,%s ,%s)
                """

            # 라벨 생성
            self.curs.execute(sql, (url, novel_address_code, siteType, novel_name_ori , novel_adult_check))
            self.conn.commit()

            time.sleep(3)



            #스레드 형식으로 소설 오리지널 내용 처리
            thread = novel_content_commit_ori(
                {
                    'novel_siteTag': siteType
                    , 'novel_address': novel_address
                    , 'novel_address_code': novel_address_code
                    , 'novel_adult_check' : novel_adult_check

                }

            )

            thread.start()







        #하멜른의 경우
        elif url.find('syosetu.org/novel') != -1:


            siteType = 'hameln'

            self.driver.get(url)
            self.driver.implicitly_wait(3)
            time.sleep(3)


            # 성인채크
            # 상수 1로는 else로 빠짐.?
            if novel_adult_check == '1' or novel_adult_check == 1:

                self.driver.find_element_by_xpath("//div[@id='page']/center/a[1]").click()
                self.driver.implicitly_wait(3)
                time.sleep(3)

                #재삽입
                self.driver.get(url)
                self.driver.implicitly_wait(3)
                time.sleep(3)



            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')


            # 소설 원제목
            novel_name_ori = (soup.select('div.ss > span'))[0].get_text()

            # 마지막에 / 들어가있을 경우
            if url[len(url) - 1] == '/':
                indexControl = -2
            else:
                indexControl = -1


            #노블코드
            novel_address_code = url.split('/')[len(url.split('/')) + indexControl]

            #노블주소
            novel_address = 'https://syosetu.org/novel/%s/' % novel_address_code



            # 책갈피 생성후 삽입
            sql = """
                    insert into	novel_label( novel_address, novel_address_code, novel_siteTag, novel_name_ori , novel_adult_check) values(%s,%s,%s,%s ,%s)
                """

            # 라벨 생성
            self.curs.execute(sql, (url, novel_address_code, siteType, novel_name_ori, novel_adult_check))
            self.conn.commit()



            # 스레드 형식으로 소설 오리지널 내용 처리
            thread = novel_content_commit_ori(
                {
                    'novel_siteTag': siteType
                    , 'novel_address': novel_address
                    , 'novel_address_code': novel_address_code
                    , 'novel_adult_check': novel_adult_check

                }

            )

            thread.start()


        return '!'


    #책갈피 내용 삽입
    def novel_content_insert(self,request,data):

        #되자일경우
        if data['novel_siteTag']    == 'ncode':


            self.driver.get('http://sitetrans.naver.net/?rel=http://ncode.syosetu.com/%s/&srcLang=ja&tarLang=ko'  %data['novel_address_code'])
            self.driver.implicitly_wait(200)

            time.sleep(7)

            self.driver.switch_to.frame('main_frame')

            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            #각 제목들 따옴
            notices = soup.select('dd.subtitle')

            #제목 갯수
            title_list = soup.find_all('dd');



            #리스트형 생성
            #lib =   list()

            for i in range(0, len(title_list)):

                #소설주소 시작은 1부터
                index = i + 1
                novel_pageTitle = title_list[i].get_text()

                #각 소설 내용 페이지
                #http: // sitetrans.naver.net /?rel = http: // ncode.syosetu.com / n3191eh / 1 / & srcLang = ja & tarLang = ko
                self.driver.get('http://sitetrans.naver.net/?rel=http://ncode.syosetu.com/%s/%s/&srcLang=ja&tarLang=ko' % (data['novel_address_code'], index))

                time.sleep(7)
                self.driver.switch_to.frame('main_frame')
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')


                #기존택스트만 가져옴
                #novel_content = soup.find(id="novel_honbun").get_text()
                novel_content = soup.find(id="novel_honbun")

                sql = '''
                
                 insert into novel_content(novel_content, novel_pageTitle, novel_page, novel_index_code)  values(%s , %s , %s ,

                            (select index_code 
                                from novel_label 
                                where novel_address_code = %s
                                and novel_siteTag	= %s
                            )
                        )
                
                '''

                self.curs.execute(sql, (repr(novel_content), novel_pageTitle, i, data['novel_address_code'], data['novel_siteTag']))

                # 삽입
                self.conn.commit()
                #for

            #if

        #med
        return  'commit'





    # 책갈피 내용 업데이트
    def novel_content_update(self,request, data):

        self.driver.implicitly_wait(4)


        self.curs = self.conn.cursor()

        # 되자일경우
        if data['novel_siteTag'] == 'ncode':

            self.driver.get('http://sitetrans.naver.net/?rel=http://ncode.syosetu.com/%s/&srcLang=ja&tarLang=ko' % data[
                'novel_address'])
            self.driver.implicitly_wait(200)

            time.sleep(7)

            self.driver.switch_to.frame('main_frame')

            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # 각 제목들 따옴
            notices = soup.select('dd.subtitle')

            # 제목 갯수
            title_list = soup.find_all('dd');

            # 리스트형 생성
            # lib =   list()

            for i in range(0, len(title_list)):
                index = i + 1
                novel_pageTitle = title_list[i].get_text()

                # lib.append({'novel_pageTitle' : title})
                # 해당 형식으로 불림
                # lib[i]['novel_pageTitle23'] =   'asdas'





                # 각 소설 내용 페이지
                # http: // sitetrans.naver.net /?rel = http: // ncode.syosetu.com / n3191eh / 1 / & srcLang = ja & tarLang = ko
                self.driver.get('http://sitetrans.naver.net/?rel=http://ncode.syosetu.com/%s/%s/&srcLang=ja&tarLang=ko' % (
                data['novel_address'], index))

                time.sleep(7)
                self.driver.switch_to.frame('main_frame')
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                novel_content = soup.find(id="novel_honbun").get_text()

                sql = """
                
                    update novel_content

                        set novel_content	=	%s
                        where novel_page	=	%s
                        and		novel_index_code	=	
                                                (select index_code 
                                                    from novel_label 
                                                    where novel_address = 	%s
                                                    and novel_siteTag	= 	%s
                                                )	

                """

                self.curs.execute(sql, (novel_content, i, data['novel_address'], data['novel_siteTag']))
                # curs.execute(sql)

                # 삽입
                self.conn.commit()

                #for
            #if

        #med
        return 'commit'





    # 각 소설 리스트 뿌리기
    def Cont_novel_list(self,request):

        #curs    =   self.dbsetting()


        title = request.GET.get('title')

        #조건이 있다면 채크
        if title == None:

            sql = """
                SELECT novel_address_code,novel_name_kor , index_code 
                    FROM novel_label
                  group by novel_address_code
                  order by index_code 
                  
                  ;
    
               """

            self.curs.execute(sql)

        else:

            sql = """
                SELECT novel_address_code,novel_name_kor , index_code 
                    FROM novel_label
                        where novel_name_kor like  %s %s %s
                  group by novel_address_code
                  order by index_code 

                  ;

               """

            self.curs.execute(sql, ('%',title,'%'))



        # 삽입 변수가 나뉘기때문에 별도로
        self.conn.commit()

        res = self.curs.fetchall()

        # Connection 닫기
        self.conn.close()

        return res




    #각 소설 페이지 리스트
    def novel_page_list(self,request,title):


        sql = """
                SELECT a.novel_pageTitle,  a.novel_page
                    FROM novel_content a
                        , novel_label b	
                    where 
                        a.novel_index_code = b.index_code
                        and	b.novel_address_code	=	'%s'


           """ % title


        self.curs.execute(sql)


        # 삽입
        self.conn.commit()

        page = self.curs.fetchall()

        # Connection 닫기
        self.conn.close()

        return  page

    # 각 소설 내용 가져오기
    def novel_content_list(self, request,title,num):

        sql = """
                      SELECT a.novel_pageTitle, a.novel_content, a.novel_page
                    		FROM novel_content a
        			            , novel_label b	
        	                where 
        			            a.novel_index_code = b.index_code
        		                and	b.novel_address_code	=	'%s'
                                and a.novel_page	=	'%s'   

                      """ % (title, num)

        self.curs.execute(sql)

        # 삽입
        res = self.curs.fetchall()


        #네이버번역기로 바뀐 태그 처리
        res[0]['novel_content'] =   re.sub('<font.*?>.*?>', '' , res[0]['novel_content'] , 0)
        res[0]['novel_content'] =   re.sub('</font.*?.*?>', '', res[0]['novel_content'], 0)



        # Connection 닫기
        self.conn.close()

        return res



    # 소설

    #소설 내용 수정 요청 (1페이지만)
    def novel_content_update(self,request,data):


        #하멜른
        if data['novel_siteTag'] == 'ncode':

            # 각 소설 내용 페이지
            self.driver.get('http://sitetrans.naver.net/?rel=http://ncode.syosetu.com/%s/%s/&srcLang=ja&tarLang=ko' % (data['novel_address'], int(data['num'])+1))


            time.sleep(7)
            self.driver.switch_to.frame('main_frame')
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            novel_content = soup.find(id="novel_honbun").get_text()

            sql = """
                update 	novel_content
                
                    set novel_content	=	%s
                    
                    where	novel_page = %s
                        and novel_index_code = 
                        
                                (select  index_code 
                                        from novel_label
                                    where  novel_address = %s and  novel_siteTag = %s);

               """

            self.curs.execute(sql, ( novel_content, data['num'],data['novel_address'] , data['novel_siteTag'] ) )
            # curs.execute(sql)

            # 삽입


            self.conn.commit()
            #if 종료


        return ''

    # 원 사이트와 들어가있는 소설 분량 채크
    # 차이가 발생할경우 소설 신규 업데이트라 보고 다음 트리거 실행
    def novel_label_check(self,request):

        sql = """
                 SELECT b.index_code             as  index_code 
                    ,b.novel_adult_check         as novel_adult_check
                    ,b.novel_address            as novel_address
                    ,b.novel_siteTag            as novel_siteTag
                    ,b.novel_address_code            as novel_address_code
                    
                    , count(a.novel_page)       as novel_page
                    
                FROM 
                        novel_content a
                        ,
                        novel_label b
                
                where  a.novel_index_code = b.index_code
                
                    group by   b.index_code
                                ,b.novel_adult_check
                                ,b.novel_address
                                ,b.novel_siteTag
                                ,b.novel_address_code 

           """

        self.curs.execute(sql )


        #소설 정보 리스트
        check_list = self.curs.fetchall()


        for list in check_list:

            self.driver.get(list['novel_address'])

            title_list  =   ''

            #되자일경우 트리거
            if list['novel_siteTag'] == 'ncode':


                #19금일떄
                if list['novel_adult_check'] == 1 or list['novel_adult_check'] == '1':

                    self.driver.implicitly_wait(5)

                    self.driver.find_element_by_xpath("//a[@id='yes18']").click()

                    self.driver.get(list['novel_address'])

                    self.driver.implicitly_wait(3)
                    time.sleep(3)


                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')


                # 제목 목록
                title_list = soup.find_all('dd');

            #되자 종료

            #하멜른일 경우
            elif list['novel_siteTag'] == 'hameln':

                # 19금일떄
                if list['novel_adult_check'] == 1 or list['novel_adult_check'] == '1':

                    self.driver.find_element_by_xpath("//div[@id='page']/center/a[1]").click()
                    self.driver.implicitly_wait(3)
                    time.sleep(3)

                    # 재삽입
                    self.driver.get(list['novel_address'])
                    self.driver.implicitly_wait(3)
                    time.sleep(3)

                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')


                # 제목 목록
                title_list = soup.select('div.ss > table > tbody > tr > td > a')

                #하멜른일 경우 종료



            # 들어가있는 페이지 숫자와 원본 페이지 숫자 비교
            # 들어와있는 페이지 데이터가 많을경우에만 작동
            if len(title_list) <= list['novel_page']:

                pass

            else:

                sql = """
                     insert into novel_IncomingList( novel_index_code, novel_address, novel_siteTag, novel_count_trans, novel_count_ori, novel_adult_check,novel_address_code)
                            values(%s,%s,%s,%s,%s,%s,%s)
                   """

                self.curs.execute(sql, (
                    list['index_code'], list['novel_address'], list['novel_siteTag']
                    , list['novel_page'], len(title_list), list['novel_adult_check']
                    ,list['novel_address_code']
                ))

                self.conn.commit()
                # if 종료
            #for 종료

        return ''



    def novel_IncomingList_commit(self,request):

        #업데이트 요청 리스트 불러옴
        sql = """
                SELECT novel_index_code, novel_address, novel_siteTag, novel_count_trans
                , novel_count_ori, novel_adult_check, novel_address_code
                ,novel_index_code
                
                FROM novel_IncomingList;
              """

        self.curs.execute(sql)

        res = self.curs.fetchall()


        # 스레드 형식으로 소설 오리지널 내용 처리
        thread = novel_content_commit_fragment_ori(
            {
                'novel_siteTag':        res[0]['novel_siteTag']
                , 'novel_address':      res[0]['novel_address']
                , 'novel_address_code': res[0]['novel_address_code']
                , 'novel_adult_check': res[0]['novel_adult_check']

                , 'novel_index_code': res[0]['novel_index_code']

                , 'novel_count_ori': res[0]['novel_count_ori']
                , 'novel_count_trans': res[0]['novel_count_trans']

            }

        )

        thread.start()









