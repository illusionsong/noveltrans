import threading
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pymysql
import json
import MySQLdb
import re
import os

from home.controll.novel_content_commit_fragment_trans import novel_content_commit_fragment_trans



class novel_content_commit_fragment_ori(threading.Thread):


    def __init__(self, args):
        threading.Thread.__init__(self)

        self.args = args
        self.driver =   webdriver.PhantomJS(os.getcwd() + '/phantomjs/bin/phantomjs')
        self.conn   =   pymysql.connect(host='logtest3.c7rrpzvpygvb.ap-northeast-2.rds.amazonaws.com', user='admin',password='logtest3password',db='trans', charset='utf8')
        self.curs   =   self.conn.cursor(pymysql.cursors.DictCursor)


        '''
        
        'novel_siteTag':    각 사이트를 알려주는태그
                        되자   ncode
                        픽시브 pixiv
        
        , 'novel_address':  파싱을 위한 매인주소
        
                        되자  소설의 매인화면
                        픽시브 소설의 1화
                        
        , 'novel_address_code': 각 소설의 원래 페이지의 인덱스 코드
                        되자 각 소설 페이지당의 인덱스
                       픽시브 미정
                       
       , 'novel_adult_check' : 성인소설채크
                        1이면 성인 0이면 전연령
                        
                        
                        
                        
        ,novel_count_ori        : 현재 들어와있는 소설 페이지 갯수
        ,novel_count_trans      : 원 사이트에 올라온 소설 페이지 갯수
        
        전부 +1 처리할것
        
        '''

    def run (self):


        # 되자일경우
        if self.args['novel_siteTag'] == 'ncode':



            #메인 페이지(모든 글이 있는)
            self.driver.get(self.args['novel_address'])

            self.driver.implicitly_wait(3)
            time.sleep(4)


            # 19금 인증 넘어가기
            if self.args['novel_adult_check'] == 1 or self.args['novel_adult_check'] == '1':

                self.driver.find_element_by_xpath("//a[@id='yes18']").click()

                self.driver.implicitly_wait(3)
                time.sleep(4)


                self.driver.get(self.args['novel_address'])






            # 총 편의  갯수 + 각 편의 제목
            title_list = soup.find_all('dd');

            for i in range(novel_count_trans, novel_count_ori):

                # 소설주소 시작은 1부터
                index = i + 1
                novel_pageTitle = title_list[i].get_text()

                # 각 소설 내용 페이지

                if self.args['novel_adult_check'] == 1 or self.args['novel_adult_check'] == '1':

                    novel_content_url   =   'https://novel18.syosetu.com/%s/%s' % (self.args['novel_address_code'], index)

                else:

                    novel_content_url = 'http://ncode.syosetu.com/%s/%s/'% (self.args['novel_address_code'], index)


                self.driver.get(novel_content_url)
                time.sleep(4)


                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')


                # 기존택스트만 가져옴
                novel_content = soup.find(id="novel_honbun")


                sql = '''

                     insert into novel_content(novel_content_ori, novel_pageTitle_ori, novel_page, novel_content_url, novel_index_code)  values(%s , %s , %s , %s,

                                (select index_code 
                                    from novel_label 
                                    where novel_address_code = %s
                                )
                            )

                    '''

                self.curs.execute(sql, (repr(novel_content), novel_pageTitle, i,      novel_content_url ,    self.args['novel_address_code']))

                # 삽입
                self.conn.commit()
            # for
        #if 되자 종료



        #if 하멜른
        elif self.args['novel_siteTag'] == 'hameln':



            # 메인 페이지(모든 글이 있는)
            self.driver.get(self.args['novel_address'])

            self.driver.implicitly_wait(3)
            time.sleep(4)


            # 19금 인증 넘어가기
            if self.args['novel_adult_check'] == 1 or self.args['novel_adult_check'] == '1':


                # 성인채크
                self.driver.find_element_by_xpath("//div[@id='page']/center/a[1]").click()
                time.sleep(3)



                self.driver.get(self.args['novel_address'])
                self.driver.implicitly_wait(3)
                time.sleep(4)




            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')



            # 총 편의  갯수 + 각 편의 제목
            title_list = soup.select('div.ss > table > tbody > tr > td > a')

            for i in range(self.args['novel_count_trans'] , self.args['novel_count_ori']):


                # 소설주소 시작은 1부터
                index = i + 1
                novel_pageTitle = title_list[i].get_text()

                # 각 소설 내용 페이지
                novel_content_url   = 'https://syosetu.org/novel/%s/%s.html' % (self.args['novel_address_code'], index)
                self.driver.get(novel_content_url)


                time.sleep(4)

                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                # 기존택스트만 가져옴
                novel_content = soup.find('div', id='honbun')

                sql = '''
                     insert into novel_content(novel_content_ori, novel_pageTitle_ori, novel_page, novel_content_url,novel_index_code)  values(%s , %s , %s , %s , 

                                (select index_code 
                                    from novel_label 
                                    where novel_address_code = %s
                                )
                            )

                    '''

                self.curs.execute(sql, (repr(novel_content), novel_pageTitle, i,    novel_content_url     ,self.args['novel_address_code']))

                # 삽입
                self.conn.commit()

        #하멜른 끝
        # if
        elif self.args['novel_siteTag'] == 'pixiv':

            for i in range(0, len(novel_content_url)):

                # 각 소설 내용 페이지
                self.driver.get('http://sitetrans.naver.net/?rel=http://trpgclub.com/log2/a.php?index_code=%s&page=%s&srcLang=ja&tarLang=ko' % ( self.args['novel_address_code'],i  )  )

                time.sleep(5)


                self.driver.switch_to.frame('main_frame')
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')



                # 기존택스트만 가져옴
                novel_content = str((soup.select('div'))[0])
                novel_content = re.sub('<font.*?>.*?>', '', novel_content, 0)
                novel_content = re.sub('</font.*?.*?>', '', novel_content, 0)


                sql = '''
                        update novel_content
                            set novel_content =  %s
                            
                        where novel_index_code = %s
                            and novel_page  = %s
                    '''

                self.curs.execute(sql,  (  novel_content, self.args['novel_address_code'], i)  )


            # for
        #if






        # 스레드 형식으로 소설 번역 내용 처리
        threadTrans = novel_content_commit_fragment_trans(
            {
                'novel_index_code'           : self.args['novel_index_code']
                , 'novel_count_ori'           : self.args['novel_count_ori']
                , 'novel_count_trans'       : self.args['novel_count_trans']
                , 'novel_siteTag'               : self.args['novel_siteTag']

            }

        )


        threadTrans.start()





    # med

