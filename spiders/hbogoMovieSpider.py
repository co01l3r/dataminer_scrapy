from typing import Iterator, Optional

import datetime
import scrapy

from ..items import HbogoMovieItem


class HbogoMovieSpider(scrapy.Spider):
    name = 'hbogo_movie'
    start_urls = [
        'https://hbogo.cz/filmy/temny-rytir'
    ]

    def parse(self, response: scrapy.http.HtmlResponse, **kwargs) -> Iterator[HbogoMovieItem]:

        yield HbogoMovieItem(
            title=HbogoMovieSpider.modify_title(HbogoMovieSpider.extract_origin_title(response), HbogoMovieSpider.extract_sub_title(response)),
            origin_year=HbogoMovieSpider.modify_year(HbogoMovieSpider.extract_year(response)),
            origin_country=HbogoMovieSpider.modify_country(HbogoMovieSpider.extract_country(response)),
            genre=HbogoMovieSpider.modify_genre(HbogoMovieSpider.extract_genre(response)),
            pegi=HbogoMovieSpider.modify_pegi(HbogoMovieSpider.extract_pegi(response)),
            imdb_rating=HbogoMovieSpider.modify_imdb_rating(HbogoMovieSpider.extract_imdb_rating(response)),  # /10
            description=HbogoMovieSpider.modify_description(HbogoMovieSpider.extract_description(response)),
            directors=HbogoMovieSpider.modify_directors(HbogoMovieSpider.extract_directors(response)),
            cast=HbogoMovieSpider.modify_cast(HbogoMovieSpider.extract_cast(response)),
            length_minutes=HbogoMovieSpider.modify_length_minutes(HbogoMovieSpider.extract_length_minutes(response))
        )

    # extract:
    @staticmethod
    def extract_origin_title(response: scrapy.http.HtmlResponse) -> str:
        return response.xpath(
            '//div[@class="meta"]/span[@class="original-title"]/text()'
        ).extract_first()

    @staticmethod
    def extract_sub_title(response: scrapy.http.HtmlResponse) -> str:
        return response.xpath(
            '//div[@class="text"]/h1/text()'
        ).extract_first()

    @staticmethod
    def extract_year(response: scrapy.http.HtmlResponse) -> str:
        return response.xpath(
            '//div[@class="meta"]/span[@class="original-title"]/following-sibling::text()[position()=1]'
        ).extract_first()

    @staticmethod
    def extract_country(response: scrapy.http.HtmlResponse) -> str:
        return response.xpath(
            '//div[@class="show-meta"]/table/tr[@class="meta-country"]/td[position()=2]/text()'
        ).extract_first()

    @staticmethod
    def extract_genre(response: scrapy.http.HtmlResponse) -> str:
        return response.xpath(
            '//div[@class="meta"]/span[@class="original-title"]/following-sibling::text()[position()=2]'
        ).extract_first()

    @staticmethod
    def extract_pegi(response: scrapy.http.HtmlResponse) -> str:
        return response.xpath(
            '//div[@class="meta"]/span[@class="separator"][2]/following-sibling::span[1]/text()'
        ).extract_first()

    @staticmethod
    def extract_imdb_rating(response: scrapy.http.HtmlResponse) -> str:
        return response.xpath(
            '//div[contains(@class, "fl-imdb")]/span[@class="rate-val"]/text()'
        ).extract_first()

    @staticmethod
    def extract_description(response: scrapy.http.HtmlResponse) -> str:
        return response.xpath(
            '//div[@class="show-synopsis"]/p/text()'
        ).extract_first()

    @staticmethod
    def extract_directors(response: scrapy.http.HtmlResponse) -> [list]:
        return response.xpath(
            '//tr[@class="meta-director"]/td/a/text()'
        ).extract()

    @staticmethod
    def extract_cast(response: scrapy.http.HtmlResponse) -> [list]:
        return response.xpath(
            '//tr[@class="meta-cast"]/td/a/text()'
        ).extract()

    @staticmethod
    def extract_length_minutes(response: scrapy.http.HtmlResponse) -> str:
        return response.xpath(
            '//tr[@class="meta-length"]/td/span/text()'
        ).extract_first()

    # modify:
    @staticmethod
    def modify_title(origin_title: Optional[str], substitute_title: Optional[str]) -> str:
        return (origin_title or substitute_title or '').title()

    @staticmethod
    def modify_year(year: Optional[str]) -> int:
        return int(year) if 1900 <= int(year) <= (datetime.datetime.now().year + 10) else None

    @staticmethod
    def modify_country(country: Optional[str]) -> str:
        return country

    @staticmethod
    def modify_genre(genre: Optional[str]) -> [list]:
        return list(dict.fromkeys([g.strip(' ') for g in genre.split(',')])) if genre is not None else None

    @staticmethod
    def modify_pegi(pegi: Optional[str]) -> int:
        return int(pegi.split('+')[0]) if pegi is not None else None

    @staticmethod
    def modify_imdb_rating(imdb_rating: Optional[str]) -> float:
        return float(imdb_rating) if imdb_rating is not None else None

    @staticmethod
    def modify_description(description: Optional[str]) -> Optional[str]:
        return description

    @staticmethod
    def modify_directors(directors: Optional[list]) -> [list]:
        return list(dict.fromkeys([d.strip(' ') for d in directors])) if directors is not None else None

    @staticmethod
    def modify_cast(cast: Optional[list]) -> [list]:
        return list(dict.fromkeys([c.strip(' ') for c in cast])) if cast is not None else None

    @staticmethod
    def modify_length_minutes(length: Optional[str]) -> Optional[int]:
        try:
            return int(length.split(' ')[0]) if length is not None else None
        except ValueError:
            return None
