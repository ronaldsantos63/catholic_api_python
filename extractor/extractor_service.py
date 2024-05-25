import re
from collections import OrderedDict
from datetime import datetime

import bs4.element
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify, MarkdownConverter

from extractor.config import Config
from extractor.utils import Utils


class ExtractorService:
    __config: Config

    def __init__(self, config: Config):
        self.__config = config

    def __get_liturgy_url(self, period: str | None) -> str | None:
        if not period:
            period = datetime.now().strftime("%d/%m/%Y")

        data = {
            'action': 'widget-ajax',
            'sMes': int(Utils.split_period(period)[1]),
            'sAno': int(Utils.split_period(period)[2]),
            'title': '',
            'type': 'liturgia',
            'ajax': 'true',
        }

        calendar = requests.post(
            f"{self.__config.BASE_URL}/wp-admin/admin-ajax.php",
            cookies=self.__config.COOKIES_AJAX,
            headers=self.__config.HEADERS_AJAX,
            data=data
        )

        calendar_soup = BeautifulSoup(calendar.content, 'html.parser')
        a_tag = calendar_soup.find(name="a", attrs=dict(href=re.compile(Utils.map_period_to_query_params_str(period))))
        return a_tag['href']

    def __parse_liturgy(self, element: bs4.Tag) -> dict:
        all_reading = element.find_all('p')

        reading = {'title': all_reading[1].get_text(),
                   'head': all_reading[2].get_text(),
                   'footer': all_reading[-2].get_text().replace("- ", ""),
                   'footer_response': all_reading[-1].get_text().replace("- ", ""),
                   'all_html': ' '.join(child.prettify() for child in element.findChildren())}

        text = all_reading[2].find_next()
        # for div in text:
        #     div.get_text()
        #     # for strong in phrase.find_all('strong'):
        #     #     strong.decompose()

        reading['text'] = ' '.join(p.get_text() for p in text)
        reading['text'] = reading['text'].replace("  ", " ")

        return reading

    def __parse_response(self, period: str | None = None) -> BeautifulSoup:
        page = requests.get(self.__get_liturgy_url(period))
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    def __parse_header_scrapy(self, soup: BeautifulSoup) -> dict:
        data = dict(date_string=dict())

        data['date_string']['day'] = soup.find(id='dia-calendar').get_text()
        data['date_string']['month'] = soup.find(id='mes-calendar').get_text()
        data['date_string']['year'] = soup.find(id='ano-calendar').get_text()

        data['date'] = Utils.date_dict_to_str(data['date_string'])

        data['color'] = soup.find(class_='cor-liturgica').get_text()
        data['color'] = Utils.clean_html(
            data['color'].split(":")[1] if len(data['color'].split(":")) > 0 else data['color'])

        data['entry_title'] = Utils.clean_html(soup.find(class_='entry-title').get_text())
        return data

    def daily_liturgy_markdown(self, period: str | None = None) -> dict:
        soup = self.__parse_response(period)
        data = self.__parse_header_scrapy(soup)
        data['readings'] = dict()

        find_first_reading = soup.find(id='liturgia-1')
        if find_first_reading:
            # data['readings']['first_reading'] = markdownify(find_first_reading.get_text())
            data['readings']['first_reading'] = Utils.convert_soup_to_markdown(find_first_reading)

        find_psalm = soup.find(id='liturgia-2')
        if find_psalm:
            data['readings']['psalm'] = Utils.convert_soup_to_markdown(find_psalm)[2:]

        find_second_reading = soup.find(id='liturgia-3')
        if find_second_reading:
            data['readings']['second_reading'] = Utils.convert_soup_to_markdown(find_second_reading)[2:]

        find_gospel = soup.find(id='liturgia-4')
        if find_gospel:
            data['readings']['gospel'] = Utils.convert_soup_to_markdown(find_gospel)[2:]

        return data

    def daily_liturgy(self, period: str | None = None) -> dict:
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
