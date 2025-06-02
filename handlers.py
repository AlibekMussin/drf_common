import requests
from logging import StreamHandler
from django.conf import settings
import logging


class TelegramHandler(StreamHandler):
    def emit(self, record):
        logger = logging.getLogger('telegram_failed')
        tg_token = settings.LOG_TO_TELEGRAM_BOT_TOKEN
        chat_id = settings.LOG_TO_TELEGRAM_CHAT_ID
        if any([not tg_token, not chat_id]):
            return
        chars_to_remove = ['<', '>', "'"]
        msg = ''
        msg += f"<strong>SPK BACK</strong>\n"
        try:
            msg += f"<strong>Пользователь: </strong> {record.request.user.username} (user_id={record.request.user.id})\n"
        except Exception as e:
            logger.info(f"[TELEGRAM BOT ERROR 1]: Can not get request attributes: {e}: text{msg}")
            print(f"[TELEGRAM BOT ERROR]: Can not get request attributes: {e}")

        # print("record:{}".format(record.message))
        record_lines = self.format(record).split('\n')
        # print("record_lines: {}".format(record_lines))

        host_header_error = False
        if record_lines[0]:
            # print("record_lines[0]: {}".format(record_lines[0]))
            error = '\n'.join([x for x in record_lines[-4:] if not x.startswith('  ')])
            for char in chars_to_remove:
                error = error.replace(char, '')
            msg += f"<strong>Ошибка: </strong> {error}\n"

            if record_lines[0]:
                splitted_record = record_lines[0].split('/', 1)
                # print("splitted_record: {}".format(splitted_record))
                if splitted_record:
                    s_r_num = 0
                    url = "не определен"
                    for s_r in splitted_record:
                        url = s_r
                        if s_r_num == 1:
                            break
                        s_r_num += 1
                    if "Invalid HTTP_HOST header:" in url:
                        host_header_error = True
                    msg += f"<strong>URL: </strong> {url}\n"
            traceback = '\n'.join(
                [f'{x}\n{record_lines[2:-1][i+1]}' for i, x in enumerate(record_lines[2:-1]) if 'apps' in x]
            )
            # print("msg:{}".format(msg))
        else:
            traceback = ', '.join(record_lines)

        # print("traceback:{}".format(traceback))
        error = ''
        for char in chars_to_remove:
            traceback = traceback.replace(char, '')
        msg += f'<strong>Traceback:</strong> <pre>{traceback}</pre>\n'

        try:
            if len(record.request.GET) > 0:
                query_params = []
                for k, v in record.request.GET.items():

                    if isinstance(v, str):
                        query_params.append("{}: {}".format(k,v))
                    else:
                        query_params.append("{}: {}".format(k,v[0]))
                params = '; '.join(query_params)
                # params = '; '.join([f"{k}:{v[0]}" for k, v in record.request.GET.items()])
                msg += f'<strong>Query params:</strong> <pre>{params}</pre>\n'
        except Exception as e:
            logger.info(f"[TELEGRAM BOT ERROR 2]: Can not get request attributes: {e}: text{msg}")
            print(f"[TELEGRAM BOT ERROR]: Can not get request query params: {e}")

        # print("MSG: {}".format(msg))
        try:
            if not host_header_error:
                resp = requests.post(
                    f'https://api.telegram.org/bot{tg_token}'
                    f'/sendMessage?chat_id={chat_id}'
                    f'&text={msg}'
                    f'&parse_mode=HTML'
                )

                if resp.status_code != 200:
                    logger.info(f"[TELEGRAM BOT SEND ERROR 3]: {resp.text}: text{msg}")
                    print(f"[TELEGRAM BOT SEND ERROR]: {resp.text}")
        except Exception as e:
            logger.info(f"[TELEGRAM BOT SEND ERROR 5]: ERROR SENDING MESSAGE TO TELEGRAM: {e} | TEXT: {msg}")
            print(f"[TELEGRAM BOT SEND ERROR 5]: {e}")