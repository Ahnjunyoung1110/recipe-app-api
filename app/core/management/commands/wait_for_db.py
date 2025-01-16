# DB가 작동될때까지 기다리게 하는 장고 코드

import time
from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    #  DB를 기다리게 하는 장고 커맨드
    def handle(self, *args, **options):
        self.stdout.write('Waiting for DB')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                #  check 로 인해 오류가 발생할 수 있음. default라는 이름의 데이터베이스를 검사
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('DB사용불가. 1초 대기')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('DB사용 가능'))
