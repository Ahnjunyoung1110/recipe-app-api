# 장고 테스트 코드

from unittest.mock import patch
# 코드의 특정 부분을 분리해서 테스트 하게 해주는 함수수
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
# 장고의 관리 명령어를 실행시킬 수 있게 해줌
from django.db.utils import OperationalError
# 예외외
from django.test import SimpleTestCase
#  데이터베이스 사용이 아니라 단순히 파이썬 코드만으로 로직 테스트


@patch('core.management.commands.wait_for_db.Command.check')
# check라는 메서드는 기본 제공
class CommandTests(SimpleTestCase):
    # 테스트 코드

    def test_wait_for_db_ready(self, patched_check):
        #  DB가 준비되었는지를 테스트 하는 코드
        patched_check.return_value = True
        #  patched_check 는 patch라는 mock를 사용하면 자동으로 전달되는 객체
        #  항상 True를 반환하도록 설정정
        call_command('wait_for_db')
        #  call_command 로 wait_for_db를 테스트

        patched_check.assert_called_once_with(databases=['default'])
        #  check가 한번만 호출되었는지 검증

    @patch('time.sleep')
    #sleep호출을 방지하기 위해서 patch로 가져옴
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        #  가까운 patch일수록 매개변수를 앞에다 적용
        #  time.sleep이 patched_sleep, 저 위에 코어 커맨드가 patched_check로 적용용
        #  DB가 작동할때 까지 확인
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        #  예외를 반환하도록 설정. 2번의 호출에 Psycopg2Error 3번은 OperationalError 그다음 true
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
