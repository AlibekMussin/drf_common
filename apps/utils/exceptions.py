# Vendor
import json
from rest_framework.exceptions import APIException, _get_error_details
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from django.conf import settings

ru_messages_file = open(settings.BASE_DIR / 'help_files/message_translates/ru.json', encoding='utf-8')
kk_messages_file = open(settings.BASE_DIR / 'help_files/message_translates/kk.json', encoding='utf-8')
en_messages_file = open(settings.BASE_DIR / 'help_files/message_translates/en.json', encoding='utf-8')

ru_messages = json.load(ru_messages_file)
kk_messages = json.load(kk_messages_file)
en_messages = json.load(en_messages_file)


class CustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'invalid'

    def __init__(self, detail_en=None, detail_kk=None, detail_ru=None, code=None, translate_code=None, message=None):
        if detail_ru is None:
            detail_ru = ru_messages.get(translate_code, self.default_detail)
        if detail_en is None:
            detail_en = en_messages.get(translate_code, self.default_detail)
        if detail_kk is None:
            detail_kk = kk_messages.get(translate_code, self.default_detail)
        if code is None:
            code = self.default_code
        else:
            self.status_code = code

        if message is None:
            message = "ошибка"
        data = {
            'detail_ru': detail_ru.format(message),
            'detail_kk': detail_kk.format(message),
            'detail_en': detail_en.format(message),
            'translate_code': translate_code
        }
        self.detail = _get_error_details(data, code)
