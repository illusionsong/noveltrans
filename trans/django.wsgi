 import os
 import sys
 
 path = '/home/ubuntu/noveltrans'     
 if path not in sys.path:
     sys.path.append(path)

 os.environ['DJANGO_SETTINGS_MODULE'] = 'noveltrans.settings'  // 프로젝트 이름.settings

 import django.core.handlers.wsgi
 application = django.core.handlers.wsgi.WSGIHandler()



