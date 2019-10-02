from Malware_Classification.Malware_Classification_App import Malware_Classification_App
from Malware_Classification.Virustotal_App import Virustotal_App
import time


# __main__은 테스팅 코드로 별 의미가 없는 부분임.
if __name__ == '__main__':
    malware_app = Malware_Classification_App()
    virustotal_app = Virustotal_App()

    while True:
        print('악성코드 자동 탐지 모델')
        print('1. 악성코드 판단')
        print('2. 종료')

        user_input = int(input('입력 : ').strip())

        if user_input == 1:
            print('start')
            before = time.time()
            mresult = malware_app.judge('D:/Skyrim/ssce5432.dll')
            vresult = virustotal_app.judge('D:/Skyrim/ssce5432.dll')
            after = time.time()

            print('실행 시간 : ', after - before)
            print('mymodel : ', mresult)
            print('virustotal : ', vresult)



        if user_input == 2:
            break
