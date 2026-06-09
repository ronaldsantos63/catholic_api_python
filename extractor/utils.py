import re
from datetime import datetime
from typing import Optional

from bs4 import NavigableString, Tag
from markdownify import MarkdownConverter


class Utils:
    @staticmethod
    def convert_soup_to_markdown(soup: Tag, **options) -> str:
        return MarkdownConverter(**options).convert_soup(soup)

    @staticmethod
    def convert_liturgy_soup_to_markdown(soup: Tag, **options) -> str:
        Utils.remove_audio_embeds(soup)
        Utils.merge_adjacent_strong_tags(soup)
        return Utils.normalize_markdown(Utils.convert_soup_to_markdown(soup, **options))

    @staticmethod
    def remove_audio_embeds(soup: Tag) -> None:
        for embed in soup.select('.embeds-audio, iframe'):
            embed.decompose()

    @staticmethod
    def merge_adjacent_strong_tags(soup: Tag) -> None:
        for strong in list(soup.find_all('strong')):
            while True:
                sibling = Utils.next_significant_sibling(strong)
                if not isinstance(sibling, Tag) or sibling.name != 'strong':
                    break

                left_text = strong.get_text()
                right_text = sibling.get_text()
                if Utils.should_insert_space_between(left_text, right_text):
                    strong.append(' ')

                strong.append(sibling.get_text())
                sibling.decompose()

    @staticmethod
    def next_significant_sibling(tag: Tag):
        sibling = tag.next_sibling
        while isinstance(sibling, NavigableString) and not sibling.strip():
            sibling = sibling.next_sibling
        return sibling

    @staticmethod
    def should_insert_space_between(left_text: str, right_text: str) -> bool:
        if not left_text or not right_text:
            return False
        if left_text[-1].isspace() or right_text[0].isspace():
            return False
        if left_text[-1] in '([{/':
            return False
        if right_text[0] in ')]},.;:!?':
            return False
        return True

    @staticmethod
    def normalize_markdown(markdown: str) -> str:
        markdown = markdown.replace('\r\n', '\n').replace('\r', '\n')
        markdown = markdown.replace('\xa0', ' ')
        markdown = re.sub(r'[ \t]+\n', '\n', markdown)
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        markdown = '\n'.join(line.strip() for line in markdown.split('\n'))
        return markdown.strip()

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
    def clear_text(text: Optional[str]) -> str:
        if text:
            return text.strip()
        else:
            return ''

    @staticmethod
    def clear_date(date_text: Optional[str]) -> str:
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
        period = Utils.normalize_period(period)
        period_split = Utils.split_period(period)
        return {"sDia": int(period_split[0]), "sMes": int(period_split[1]), "sAno": period_split[2]}

    @staticmethod
    def split_period(period: str) -> list:
        return period.split('/')

    @staticmethod
    def normalize_period(period: Optional[str]) -> str:
        if not period:
            return datetime.now().strftime("%d/%m/%Y")

        period = period.strip()
        try:
            parsed_date = datetime.strptime(period, "%d/%m/%Y")
        except ValueError:
            raise ValueError("period must use dd/mm/yyyy and be a valid date")

        return parsed_date.strftime("%d/%m/%Y")

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
