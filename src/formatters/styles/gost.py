"""
Стиль цитирования по ГОСТ Р 7.0.5-2008.
"""
from string import Template
from typing import Dict

from pydantic import BaseModel

from formatters.base import BaseCitationFormatter
from formatters.models import BookModel, InternetResourceModel, ArticlesCollectionModel, DissertationModel, \
    NormativeActModel
from formatters.styles.base import BaseCitationStyle
from logger import get_logger


logger = get_logger(__name__)


class GOSTBook(BaseCitationStyle):
    """
    Форматирование для книг.
    """

    data: BookModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $title. – $edition$city: $publishing_house, $year. – $pages с."
        )

    def substitute(self) -> str:

        logger.info('Форматирование книги "%s" ...', self.data.title)

        return self.template.substitute(
            authors=self.data.authors,
            title=self.data.title,
            edition=self.get_edition(),
            city=self.data.city,
            publishing_house=self.data.publishing_house,
            year=self.data.year,
            pages=self.data.pages,
        )

    def get_edition(self) -> str:
        """
        Получение отформатированной информации об издательстве.

        :return: Информация об издательстве.
        """

        return f"{self.data.edition} изд. – " if self.data.edition else ""


class GOSTInternetResource(BaseCitationStyle):
    """
    Форматирование для интернет-ресурсов.
    """

    data: InternetResourceModel

    @property
    def template(self) -> Template:
        return Template(
            "$article // $website URL: $link (дата обращения: $access_date)."
        )

    def substitute(self) -> str:

        logger.info('Форматирование интернет-ресурса "%s" ...', self.data.article)

        return self.template.substitute(
            article=self.data.article,
            website=self.data.website,
            link=self.data.link,
            access_date=self.data.access_date,
        )


class GOSTCollectionArticle(BaseCitationStyle):
    """
    Форматирование для статьи из сборника.
    """

    data: ArticlesCollectionModel

    @property
    def template(self) -> Template:
        return Template(
            "$authors $article_title // $collection_title. – $city: $publishing_house, $year. – С. $pages."
        )

    def substitute(self) -> str:

        logger.info('Форматирование сборника статей "%s" ...', self.data.article_title)

        return self.template.substitute(
            authors=self.data.authors,
            article_title=self.data.article_title,
            collection_title=self.data.collection_title,
            city=self.data.city,
            publishing_house=self.data.publishing_house,
            year=self.data.year,
            pages=self.data.pages,
        )


class GOSTDissertation(BaseCitationStyle):
    """
    Форматирование для диссертации.
    """

    data: DissertationModel

    @property
    def template(self) -> Template:
        return Template(
            "$author $title : дис. ... $author_degree $science_branch наук: $branch_code. $city,"
            " $year. $page_count с."
        )

    def substitute(self) -> str:

        logger.info('Форматирование диссертации "%s" ...', self.data.title)

        return self.template.substitute(
            author=self.data.author,
            title=self.data.title,
            author_degree=self.data.author_degree,
            science_branch=self.data.science_branch,
            branch_code=self.data.branch_code,
            city=self.data.city,
            year=self.data.year,
            page_count=self.data.page_count
        )


class GOSTNormativeAct(BaseCitationStyle):
    """
    Форматирование для нормативно-правовых актов.
    """

    data: NormativeActModel

    @property
    def template(self) -> Template:
        return Template(
            "$title : $type от $acceptance_date г. №$number // $publication_source. $publication_year. "
            "№$source_number. Ст. $article_number. $edition_date."
        )

    def substitute(self) -> str:

        logger.info('Форматирование НПА "%s" ...', self.data.title)

        return self.template.substitute(
            type=self.data.type,
            title=self.data.title,
            acceptance_date=self.data.acceptance_date,
            number=self.data.number,
            publication_source=self.data.publication_source,
            publication_year=self.data.publication_year,
            source_number=self.data.source_number,
            article_number=self.data.article_number,
            edition_date=self.get_edition_date()
        )

    def get_edition_date(self) -> str:
        """
        Получение отформатированной информации о дате редакции НПА.

        :return: Дата редакции.
        """

        return f"ред. от {self.data.edition_date}" if self.data.edition_date else ""


class GOSTCitationFormatter(BaseCitationFormatter):
    """
    Класс для форматирования списка источников по ГОСТ 7.0.5-2008.
    """

    formatters_map: Dict[BaseModel, BaseCitationStyle] = {
        BookModel: GOSTBook,
        InternetResourceModel: GOSTInternetResource,
        ArticlesCollectionModel: GOSTCollectionArticle,
        DissertationModel: GOSTDissertation,
        NormativeActModel: GOSTNormativeAct
    }

