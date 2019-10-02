from virustotal_python import Virustotal
import requests


class Virustotal_App:
    def __init__(self):
        self.api_key = 'cc9bd463018a4de98c4652c7c433a04b0fa91a8196057db03b0009a515046de7'


    def judge(self, filepath):
        '''
            virustotal에 특정 파일 검사
            :param filepath: 검사 대상 path
            :param api_key: virustotal API_KEY
            :return: 결과 boolean True : Non-malware, False : malware
        '''
        # Normal Initialisation.
        vtotal = Virustotal(self.api_key)
        result = vtotal.file_scan(filepath)

        print('>> Virustotal Search report. <<')
        json_resp = result['json_resp']
        md5 = json_resp['md5'].strip()
        print('result link : ', json_resp['permalink'])

        url = 'https://www.virustotal.com/vtapi/v2/file/report'
        params = {'apikey': self.api_key, 'resource': md5}
        response = requests.get(url, params=params)

        total = response.json()['total']
        positives = response.json()['positives']
        print('Result : (' + str(total) + ' / ' + str(positives) + ')')

        if positives == 0:
            vtotal_judge = True
        else:
            vtotal_judge = False

        # 최종 검사 결과, 탐지 횟 수
        return vtotal_judge, positives, total, json_resp['permalink']