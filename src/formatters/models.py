"""
Описание схем объектов (DTO).
"""

from typing import Optional
from pydantic import BaseModel, Field


class BookModel(BaseModel):
    """
    Модель книги:

    .. code-block::

        BookModel(
            authors="Иванов И.М., Петров С.Н.",
            title="Наука как искусство",
            edition="3-е",
            city="СПб.",
            publishing_house="Просвещение",
            year=2020,
            pages=999,
        )
    """

    authors: str
    title: str
    edition: Optional[str]
    city: str
    publishing_house: str
    year: int = Field(..., gt=0)
    pages: int = Field(..., gt=0)


class InternetResourceModel(BaseModel):
    """
    Модель интернет ресурса:

    .. code-block::

        InternetResourceModel(
            article="Наука как искусство",
            website="Ведомости",
            link="https://www.vedomosti.ru/",
            access_date="01.01.2021",
        )
    """

    article: str
    website: str
    link: str
    access_date: str


class ArticlesCollectionModel(BaseModel):

    """
    Модель сборника статей:

    .. code-block::

        ArticlesCollectionModel(
            authors="Иванов И.М., Петров С.Н.",
            article_title="Наука как искусство",
            collection_title="Сборник научных трудов",
            city="СПб.",
            publishing_house="АСТ",
            year=2020,
            pages="25-30",
        )
    """

    authors: str
    article_title: str
    collection_title: str
    city: str
    publishing_house: str
    year: int = Field(..., gt=0)
    pages: str


class DissertationModel(BaseModel):
    """
        Модель научной диссертации:

        .. code-block::

            DissertationModel(
                author="Иванов И.М.",
                title="Наука как искусство",
                author_degree="канд.",
                science_branch="экон.",
                branch_code="01.01.01",
                city="СПб.",
                year=2020,
                page_count=200,
            )
        """

    author: str
    title: str
    author_degree: str
    science_branch: str
    branch_code: str
    city: str
    year: int = Field(..., gt=0)
    page_count: int = Field(..., gt=0)


class NormativeActModel(BaseModel):
    """
            Модель нормативно-правового акта:

            .. code-block::

                NormativeActModel(
                    type="Указ Президента Российской Федерации",
                    title="Концепция перехода Российской Федерации к устойчивому развитию",
                    acceptance_date="01.01.2000",
                    number="1234-56",
                    publication_source="Парламентская газета",
                    publication_year=2020,
                    source_number=5,
                    article_number=15,
                    edition_date="11.09.2002"
                )
            """

    type: str
    title: str
    acceptance_date: str
    number: str
    publication_source: str
    publication_year: int = Field(..., gt=0)
    source_number: int = Field(..., gt=0)
    article_number: int = Field(..., gt=0)
    edition_date: Optional[str]
