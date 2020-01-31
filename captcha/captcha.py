import requests
import time


class Captcha:
    def __init__(self, api_key):
        self.api_key = api_key
        self.captcha_id = None

    def solve_recaptcha(self, g_key, page_url):
        try:
            id_result = requests.post('http://2captcha.com/in.php',
                                      data={'method': 'userrecaptcha', 'key': self.api_key, 'googlekey': g_key,
                                            'pageurl': page_url,
                                            'json': 0, 'here': 'now', 'CapMonsterModule': 'ReCaptchaWord'}).text
            if self.captcha_response(id_result) is False:
                return None
            id_result = id_result.split('|')
            self.captcha_id = id_result[1]

            recaptcha_answer = requests.get(
                "http://2captcha.com/res.php?key=" + self.api_key + "&action=get&id=" + self.captcha_id).text
            if self.captcha_response(recaptcha_answer) is False:
                return None

            while 'CAPCHA_NOT_READY' in recaptcha_answer:
                time.sleep(20)
                recaptcha_answer = requests.get(
                    "http://2captcha.com/res.php?key=" + self.api_key + "&action=get&id=" + self.captcha_id).text
            if self.captcha_response(recaptcha_answer) is False:
                return None
            text = recaptcha_answer
            if '|' in text:
                text = recaptcha_answer.split('|')
                text = text[1]
                return text
            else:
                return None
        except requests.exceptions.ConnectionError:
            return None

    def captcha_response(self, status):
        if status == 'ERROR_CAPTCHA_UNSOLVABLE':
            print('ERROR_CAPTCHA_UNSOLVABLE')
            return False
        elif status == 'ERROR_WRONG_USER_KEY':
            print('ERROR_WRONG_USER_KEY')
            return False
        elif status == 'ERROR_KEY_DOES_NOT_EXIST':
            print('ERROR_KEY_DOES_NOT_EXIST')
            return False
        elif status == 'ERROR_WRONG_ID_FORMAT':
            print('ERROR_WRONG_ID_FORMAT')
            return False
        elif status == 'ERROR_WRONG_CAPTCHA_ID':
            print('ERROR_WRONG_CAPTCHA_ID')
            return False
        elif status == 'ERROR_BAD_DUPLICATES':
            print('ERROR_BAD_DUPLICATES')
            return False
        elif status == 'REPORT_NOT_RECORDED':
            print('REPORT_NOT_RECORDED')
            return False
        elif status == 'ERROR_BAD_TOKEN_OR_PAGEURL':
            print('ERROR_BAD_TOKEN_OR_PAGEURL')
            return False
        elif status == 'ERROR_ZERO_BALANCE':
            print('ERROR_ZERO_BALANCE')
            return False
        elif status == 'ERROR_PAGEURL':
            print('ERROR_PAGEURL')
            return False
        elif status == 'ERROR_NO_SLOT_AVAILABLE':
            print('ERROR_NO_SLOT_AVAILABLE')
            return False
        elif status == 'ERROR_ZERO_CAPTCHA_FILESIZE':
            print('ERROR_ZERO_CAPTCHA_FILESIZE')
            return False
        elif status == 'ERROR_TOO_BIG_CAPTCHA_FILESIZE':
            print('ERROR_TOO_BIG_CAPTCHA_FILESIZE')
            return False
        elif status == 'ERROR_WRONG_FILE_EXTENSION':
            print('ERROR_WRONG_FILE_EXTENSION')
            return False
        elif status == 'ERROR_IMAGE_TYPE_NOT_SUPPORTED':
            print('ERROR_IMAGE_TYPE_NOT_SUPPORTED')
            return False
        elif status == 'ERROR_UPLOAD':
            print('ERROR_UPLOAD')
            return False
        elif status == 'ERROR_IP_NOT_ALLOWED':
            print('ERROR_IP_NOT_ALLOWED')
            return False
        elif status == 'IP_BANNED':
            print('IP_BANNED')
            return False
        elif status == 'ERROR_GOOGLEKEY':
            print('ERROR_GOOGLEKEY')
            return False
        elif status == 'ERROR_CAPTCHAIMAGE_BLOCKED':
            print('ERROR_CAPTCHAIMAGE_BLOCKED')
            return False
        elif status == 'MAX_USER_TURN':
            print('MAX_USER_TURN')
            return False
        else:
            return True

    def report_captcha(self):
        try:
            if self.captcha_id is not None:
                report_answer = requests.get(
                    "http://2captcha.com/res.php?key=" + self.api_key + "&action=reportbad&id=" + self.captcha_id).text
                if report_answer == 'OK_REPORT_RECORDED':
                    return True
            else:
                return None
        except requests.exceptions.ConnectionError:
            return None
