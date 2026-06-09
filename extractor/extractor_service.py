import re
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

from extractor.config import Config
from extractor.exceptions import ExternalSourceError, InvalidLiturgySourceError, LiturgyNotFoundError
from extractor.utils import Utils


class ExtractorService:
    __config: Config

    def __init__(self, config: Config):
        self.__config = config

    def __get_liturgy_url(self, period: Optional[str]) -> str:
        period = Utils.normalize_period(period)
        query_params = Utils.map_period_to_query_params(period)

        data = {
            'action': 'widget-ajax',
            'sDia': query_params['sDia'],
            'sMes': query_params['sMes'],
            'sAno': query_params['sAno'],
            'title': '',
            'type': 'liturgia',
            'ajax': 'true',
        }

        try:
            calendar = requests.post(
                f"{self.__config.BASE_URL}/wp-admin/admin-ajax.php",
                cookies=self.__config.COOKIES_AJAX,
                headers=self.__config.HEADERS_AJAX,
                data=data,
                timeout=self.__config.REQUEST_TIMEOUT
            )
            calendar.raise_for_status()
        except requests.RequestException as exc:
            raise ExternalSourceError("Could not fetch liturgy calendar") from exc

        calendar_soup = BeautifulSoup(calendar.content, 'html.parser')
        href_pattern = re.compile(re.escape(Utils.map_period_to_query_params_str(period)))
        a_tag = calendar_soup.find(name="a", attrs=dict(href=href_pattern))
        if not a_tag or not a_tag.get('href'):
            raise LiturgyNotFoundError(f"No liturgy found for the period: {period}")

        return urljoin(self.__config.BASE_URL, a_tag['href'])

    def __parse_liturgy(self, element: Tag) -> dict:
        all_reading = element.find_all('p')

        reading = {'title': all_reading[1].get_text(),
                   'head': all_reading[2].get_text(),
                   'footer': all_reading[-2].get_text().replace("- ", ""),
                   'footer_response': all_reading[-1].get_text().replace("- ", ""),
                   'all_html': ' '.join(child.prettify() for child in element.find_all())}

        text = all_reading[2].find_next()

        reading['text'] = ' '.join(p.get_text() for p in text)
        reading['text'] = reading['text'].replace("  ", " ")

        return reading

    def __parse_response(self, period: Optional[str] = None) -> BeautifulSoup:
        try:
            page = requests.get(
                self.__get_liturgy_url(period),
                timeout=self.__config.REQUEST_TIMEOUT
            )
            page.raise_for_status()
        except requests.RequestException as exc:
            raise ExternalSourceError("Could not fetch liturgy page") from exc

        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    def __parse_header_scrapy(self, soup: BeautifulSoup) -> dict:
        data = dict(date_string=dict())

        data['date_string']['day'] = self.__required_text(soup, id='dia-calendar')
        data['date_string']['month'] = self.__required_text(soup, id='mes-calendar')
        data['date_string']['year'] = self.__required_text(soup, id='ano-calendar')

        data['date'] = Utils.date_dict_to_str(data['date_string'])

        color_text = self.__required_text(soup, class_='cor-liturgica')
        _, separator, color = color_text.partition(":")
        data['color'] = Utils.clean_html(color if separator else color_text)

        data['entry_title'] = Utils.clean_html(self.__required_text(soup, class_='entry-title'))
        return data

    @staticmethod
    def __required_text(soup: BeautifulSoup, **kwargs) -> str:
        element = soup.find(**kwargs)
        if not element:
            raise InvalidLiturgySourceError(f"Missing expected liturgy field: {kwargs}")
        return element.get_text()

    def daily_liturgy_markdown(self, period: Optional[str] = None) -> dict:
        soup = self.__parse_response(period)
        data = self.__parse_header_scrapy(soup)
        data['readings'] = dict()

        find_first_reading = soup.find(id='liturgia-1')
        if find_first_reading:
            data['readings']['first_reading'] = Utils.convert_liturgy_soup_to_markdown(find_first_reading)

        find_psalm = soup.find(id='liturgia-2')
        if find_psalm:
            data['readings']['psalm'] = Utils.convert_liturgy_soup_to_markdown(find_psalm)

        find_second_reading = soup.find(id='liturgia-3')
        if find_second_reading:
            data['readings']['second_reading'] = Utils.convert_liturgy_soup_to_markdown(find_second_reading)

        find_gospel = soup.find(id='liturgia-4')
        if find_gospel:
            data['readings']['gospel'] = Utils.convert_liturgy_soup_to_markdown(find_gospel)

        return data

    def daily_liturgy(self, period: Optional[str] = None) -> dict:
        """

        :param period: pattern dd/mm/yyyy
        :return: data
        """
        soup = self.__parse_response(period)
        data = self.__parse_header_scrapy(soup)

        data['readings'] = dict()

        find_first_reading = soup.find(id='liturgia-1')
        if find_first_reading:
            data['readings']['first_reading'] = self.__parse_liturgy(find_first_reading)

        find_psalm = soup.find(id='liturgia-2')
        if find_psalm:
            all_psalm = find_psalm.find_all('p')

            psalm = dict()

            psalm['title'] = all_psalm[0].get_text()
            psalm['response'] = all_psalm[1].get_text().replace("— ", "")

            psalm['all_html'] = ' '.join(p.prettify() for p in all_psalm)

            list_content_psalm = []

            content_psalm = all_psalm[2:]
            for phrase in content_psalm:
                for strong in phrase.find_all('strong'):
                    strong.decompose()

                text = phrase.get_text().replace("— ", "")
                if text:
                    list_content_psalm.append(text)

            psalm['content_psalm'] = list_content_psalm

            data['readings']['psalm'] = psalm

        find_second_reading = soup.find(id='liturgia-3')
        if find_second_reading:
            data['readings']['second_reading'] = self.__parse_liturgy(find_second_reading)

        find_gospel = soup.find(id='liturgia-4')
        if find_gospel:
            all_gospel = find_gospel.find_all('p')

            gospel = dict()

            gospel['title'] = all_gospel[1].get_text()
            gospel['head'] = all_gospel[2].get_text().replace("— ", "")
            gospel['head_response'] = all_gospel[5].get_text().replace("— ", "")
            gospel['footer'] = all_gospel[-2].get_text().replace(" — ", "")
            gospel['footer_response'] = all_gospel[-1].get_text().replace(" — ", "")

            gospel['all_html'] = ' '.join(p.prettify() for p in all_gospel)

            text = all_gospel[5:-2]
            for phrase in text:
                for strong in phrase.find_all('strong'):
                    strong.decompose()

            gospel['text'] = ' '.join(p.get_text() for p in text)
            gospel['text'] = gospel['text'].replace("  ", " ")

            data['readings']['gospel'] = gospel

        return data
