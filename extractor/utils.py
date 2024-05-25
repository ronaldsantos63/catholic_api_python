import re
from datetime import datetime

from bs4 import Tag
from markdownify import MarkdownConverter


class Utils:
    @staticmethod
    def convert_soup_to_markdown(soup: Tag, **options) -> str:
        return MarkdownConverter(**options).convert_soup(soup)

    @staticmethod
    def date_dict_to_str(date_dict: dict) -> str:
        return f"{Utils.parse_day(date_dict['day'])}/{Utils.parse_month(date_dict['month'])}/{date_dict['year']}"

    @staticmethod
    def parse_month(month) -> str:
        month_list = {
            'Jan': '01', 'Fev': '02', 'Mar': '03', 'Abr': '04', 'Mai': '05', 'Jun': '06',
            'Jul': '07', 'Ago': '08', 'Set': '09', 'Out': '10', 'Nov': '11', 'Dez': '12'
        }

        return month_list[month]

    @staticmethod
    def parse_day(day: str) -> str:
        if len(day) == 1:
            day = '0' + day

        return day

    @staticmethod
    def clear_text(text: str | None) -> str:
        if text:
            return text.strip()
        else:
            return ''

    @staticmethod
    def clear_date(date_text: str | None) -> str:
        if date_text:
            date = datetime.fromisoformat(date_text)
            return date.strftime('%d/%m/%Y')
        else:
            return ''

    @staticmethod
    def map_period_to_query_params_str(period: str) -> str:
        return Utils.map_query_params_to_str(Utils.map_period_to_query_params(period))

    @staticmethod
    def map_query_params_to_str(query_params: dict) -> str:
        return "&".join([f"{k}={v}" for k, v in query_params.items()])

    @staticmethod
    def map_period_to_query_params(period: str) -> dict:
        period_split = Utils.split_period(period)
        return {"sDia": int(period_split[0]), "sMes": int(period_split[1]), "sAno": period_split[2]}

    @staticmethod
    def split_period(period: str) -> list:
        return period.split('/')

    @staticmethod
    def clean_html(html: str) -> str:
        if not html:
            return html

        cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
        cleaned = re.sub(r"(?s)<!--(.*?)-->\n?", "", cleaned)
        cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
        cleaned = re.sub(r"&nbsp;", " ", cleaned)

        cleaned = cleaned.replace(";", ":")
        cleaned = cleaned.replace("\n", " ")
        cleaned = cleaned.replace("\r", " ")
        cleaned = cleaned.replace("\t", " ")

        for i in range(10):
            cleaned = cleaned.replace("  ", " ")

        cleaned = cleaned.strip()
        return cleaned
