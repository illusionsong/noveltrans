import threading
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pymysql
import json
import MySQLdb
import re



class novel_content_insertAll(threading.Thread):


    def __init__(self, args):
        threading.Thread.__init__(self)

        self.args = args
        self.driver =   webdriver.PhantomJS('C:/Users/egnis/trans/phantomjs/bin/phantomjs')
        self.conn   =   pymysql.connect(host='logtest3.c7rrpzvpygvb.ap-northeast-2.rds.amazonaws.com', user='admin',password='logtest3password',db='trans', charset='utf8')
        self.curs   =   self.conn.cursor(pymysql.cursors.DictCursor)

    def run (self):




        sql = """
            SELECT novel_content_ori
					FROM novel_content
				where novel_index_code = %s;
					

           """

        self.curs.execute(sql , self.args['novel_address_code'])

        self.conn.commit()

        novel_content_url = self.curs.fetchall()





        # 되자일경우
        if self.args['novel_siteTag'] == 'ncode':

            # 각 소설 내용 페이지
            self.driver.get('http://sitetrans.naver.net/?rel=http://trpgclub.com/log2/a.php?index_code=%s&page=%s&srcLang=ja&tarLang=ko' % (self.args['novel_address_code'], i))


            self.driver.get('http://sitetrans.naver.net/?rel=http://ncode.syosetu.com/%s/&srcLang=ja&tarLang=ko' % self.args['novel_address_code'])
            self.driver.implicitly_wait(10)

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
                # 소설주소 시작은 1부터
                index = i + 1
                novel_pageTitle = title_list[i].get_text()

                # 각 소설 내용 페이지
                self.driver.get(
                    'http://sitetrans.naver.net/?rel=http://ncode.syosetu.com/%s/%s/&srcLang=ja&tarLang=ko' % (
                        self.args['novel_address_code'], index))

                time.sleep(7)
                self.driver.switch_to.frame('main_frame')
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                # 기존택스트만 가져옴
                # novel_content = soup.find(id="novel_honbun").get_text()
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

                self.curs.execute(sql, (
                    repr(novel_content), novel_pageTitle, i, self.args['novel_address_code'], self.args['novel_siteTag']))

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

                print(i)
                # for
            #if

        # 삽입
        self.conn.commit()

    # med

