import threading
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pymysql
import json
import MySQLdb
import re
import os


class novel_content_commit_fragment_trans(threading.Thread):


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

               , 'novel_index_code': 
               
               번역사이트의 고유 소설인댁스
                              

               '''


    def run (self):

        for i in range(self.args['novel_count_trans'], self.args['novel_count_ori']):

            if self.args['novel_siteTag'] == 'ncode':

                self.driver.get(
                    'http://sitetrans.naver.net/?rel=http://trpgclub.com/log2/a.php?index_code=%s&page=%s&srcLang=ja&tarLang=ko' % (
                    self.args['novel_index_code'], i))

                self.driver.implicitly_wait(3)
                time.sleep(4)

                self.driver.switch_to.frame('main_frame')
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                # 기존택스트만 가져옴
                novel_content = soup.find(id="novel_honbun")

                novelTitle = (soup.select('div.transtitle'))[0].get_text()




            elif self.args['novel_siteTag'] == 'hameln':

                # 각 소설 내용 페이지
                self.driver.get(
                    'http://sitetrans.naver.net/?rel=http://trpgclub.com/log2/a.php?index_code=%s&page=%s&srcLang=ja&tarLang=ko' % (
                    self.args['novel_index_code'], i))

                time.sleep(5)

                self.driver.switch_to.frame('main_frame')
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                # 편당 제목
                novelTitle = (soup.select('div.transtitle'))[0].get_text()
                # 소설 내용
                novel_content = soup.find(id="honbun")

                # 기존택스트만 가져옴
                novel_content = str(novel_content)
                novel_content = re.sub('<font.*?>.*?>', '', novel_content, 0)
                novel_content = re.sub('</font.*?.*?>', '', novel_content, 0)




            sql = '''
                 update novel_content
                    set novel_content = %s
                    ,   novel_pageTitle = %s

                    where novel_index_code = %s
                        and novel_page = %s
                '''

            self.curs.execute(sql, (repr(novel_content), novelTitle,   self.args['novel_index_code']  , i))

            # 삽입
            self.conn.commit()

        # for



        # 되자일경우
        if self.args['novel_siteTag'] == 'ncode':


            for i in range(self.args['novel_count_trans'] , self.args['novel_count_ori']):

                self.driver.get('http://sitetrans.naver.net/?rel=http://trpgclub.com/log2/a.php?index_code=%s&page=%s&srcLang=ja&tarLang=ko' % (self.args['novel_index_code'] , i))

                self.driver.implicitly_wait(3)
                time.sleep(4)


                self.driver.switch_to.frame('main_frame')
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')


                #기존택스트만 가져옴
                novel_content = soup.find(id="novel_honbun")

                novelTitle = (soup.select('div.transtitle'))[0].get_text()


                sql = '''
                     update novel_content
                        set novel_content = %s
                        ,   novel_pageTitle = %s
                        
                        where novel_index_code = %s
                            and novel_page = %s
                    '''

                self.curs.execute(sql, (repr(novel_content), novelTitle,  novel_index_code[i]['novel_index_code'], i))

                # 삽입
                self.conn.commit()

            # for




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
        #if 픽시브 끝



            # if








    # class

