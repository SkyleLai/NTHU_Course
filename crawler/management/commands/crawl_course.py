from django.core.management.base import BaseCommand

from crawler.crawler import crawl_course, crawl_dept
from crawler.course import get_cou_codes
try:
    from crawler.decaptcha import Entrance, DecaptchaFailure
except ImportError:
    Entrance = None
from data_center.models import Course, Department
from utils.config import get_config


def get_auth_pair(url):
    if Entrance is not None:
        try:
            return Entrance(url).get_ticket()
        except DecaptchaFailure:
            print('Automated decaptcha failed.')
    else:
        print('crawler.decaptcha not available (requires tesseract >= 3.03).')
    print('Please provide valid ACIXSTORE and auth_num from')
    print(url)
    ACIXSTORE = input('ACIXSTORE: ')
    auth_num = input('auth_num: ')
    return ACIXSTORE, auth_num


class Command(BaseCommand):
    args = ''
    help = 'Help crawl the course data from NTHU.'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear'] == False:
            import time
            start_time = time.time()
            cou_codes = get_cou_codes()
            for ys in [get_config('crawler', 'semester')]:
                ACIXSTORE, auth_num = get_auth_pair(
                    'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE'
                    '/JH/6/6.2/6.2.9/JH629001.php'
                )
                print('Crawling course for ' + ys)
                crawl_course(ACIXSTORE, auth_num, cou_codes, ys)

                ACIXSTORE, auth_num = get_auth_pair(
                    'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE'
                    '/JH/6/6.2/6.2.3/JH623001.php'
                )
                print('Crawling dept for ' + ys)
                crawl_dept(ACIXSTORE, auth_num, cou_codes, ys)
                print('===============================\n')
            elapsed_time = time.time() - start_time
            print('Total %.3f second used.' % elapsed_time)
        else:
            Course.objects.all().delete()
            Department.objects.all().delete()
