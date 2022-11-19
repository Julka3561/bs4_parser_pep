import logging

from requests import RequestException

from constants import EXPECTED_STATUS
from exceptions import ParserFindTagException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def logging_status_error(errors):
    if errors:
        err_desciption = ''
        for row in errors:
            err_desciption += row[0]
            err_desciption += f'\nСтатус в карточке: {row[2]}'
            err_desciption += (f'\nОжидаемые статусы: '
                               f'{", ".join(EXPECTED_STATUS[row[1]])}\n')

        msg = 'Несовпадающие статусы:\n' + err_desciption
        logging.warning(msg)
