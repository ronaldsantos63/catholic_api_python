import os
from typing import Dict


def get_float_env(name: str, default: float) -> float:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    try:
        value = float(raw_value)
    except ValueError:
        return default

    return value if value > 0 else default


class Config:
    BASE_URL: str = os.getenv('BASE_URL', "https://liturgia.cancaonova.com")
    REQUEST_TIMEOUT: float = get_float_env('REQUEST_TIMEOUT', 10.0)
    COOKIES_AJAX: Dict[str, str] = {
        'qtrans_front_language': 'pb',
        'cookielawinfo-checkbox-necessary': 'yes',
        'cookielawinfo-checkbox-functional': 'no',
        'cookielawinfo-checkbox-performance': 'no',
        'cookielawinfo-checkbox-analytics': 'no',
        'cookielawinfo-checkbox-advertisement': 'no',
        'cookielawinfo-checkbox-others': 'no',
    }
    HEADERS_AJAX: Dict[str, str] = {
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'qtrans_front_language=pb; cookielawinfo-checkbox-necessary=yes; cookielawinfo-checkbox-functional=no; cookielawinfo-checkbox-performance=no; cookielawinfo-checkbox-analytics=no; cookielawinfo-checkbox-advertisement=no; cookielawinfo-checkbox-others=no',
        'dnt': '1',
        #'origin': 'https://liturgia.cancaonova.com',
        'priority': 'u=1, i',
        #'referer': 'https://liturgia.cancaonova.com/pb/liturgia/7a-semana-tempo-comum-quinta-feira-3/?sDia=23&sMes=05&sAno=2024',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'x-kl-saas-ajax-request': 'Ajax_Request',
        'x-requested-with': 'XMLHttpRequest',
    }
