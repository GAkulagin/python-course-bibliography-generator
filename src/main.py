"""
Запуск приложения.
"""
from enum import Enum, unique

import click
from formatters.styles.gost import GOSTCitationFormatter
from logger import get_logger
from readers.reader import SourcesReader
from renderer import BaseRenderer, GOSTRenderer, APARenderer
from settings import INPUT_FILE_PATH, OUTPUT_FILE_PATH
from formatters.base import BaseCitationFormatter
from formatters.styles.apa import APACitationFormatter

logger = get_logger(__name__)


@unique
class CitationEnum(Enum):
    """
    Поддерживаемые типы цитирования.
    """

    GOST = "gost"  # ГОСТ Р 7.0.5-2008
    APA = "apa"  # American Psychological Association


@click.command()
@click.option(
    "--citation",
    "-c",
    "citation",
    type=click.Choice([item.name for item in CitationEnum], case_sensitive=False),
    default=CitationEnum.GOST.name,
    show_default=True,
    help="Стиль цитирования",
)
@click.option(
    "--path_input",
    "-pi",
    "path_input",
    type=str,
    default=INPUT_FILE_PATH,
    show_default=True,
    help="Путь к входному файлу",
)
@click.option(
    "--path_output",
    "-po",
    "path_output",
    type=str,
    default=OUTPUT_FILE_PATH,
    show_default=True,
    help="Путь к выходному файлу",
)
def process_input(
    citation: str = CitationEnum.GOST.name,
    path_input: str = INPUT_FILE_PATH,
    path_output: str = OUTPUT_FILE_PATH,
) -> None:
    """
    Генерация файла Word с оформленным библиографическим списком.

    :param str citation: Стиль цитирования
    :param str path_input: Путь к входному файлу
    :param str path_output: Путь к выходному файлу
    """

    logger.info(
        """Обработка команды с параметрами:
        - Стиль цитирования: %s.
        - Путь к входному файлу: %s.
        - Путь к выходному файлу: %s.""",
        citation,
        path_input,
        path_output,
    )

    models = SourcesReader(path_input).read()
    formatted_models = tuple(
        str(item) for item in get_formatter(citation)(models).format()
    )

    logger.info("Генерация выходного файла ...")
    get_renderer(citation)(formatted_models).render(path_output)

    logger.info("Команда успешно завершена.")


def get_formatter(style: str) -> type[BaseCitationFormatter]:
    """
    Возвращает форматтер для указанного стиля цитирования.

    :param str style: Стиль цитирования

    :return: форматтер для заданного стиля цитирования.
    """
    format_styles_map = {
        CitationEnum.GOST.name: GOSTCitationFormatter,
        CitationEnum.APA.name: APACitationFormatter
    }
    return format_styles_map.get(style)


def get_renderer(style: str) -> type[BaseRenderer]:
    """
    Возвращает объект BaseRenderer для указанного стиля цитирования.

    :param str style: Стиль цитирования

    :return: рендерер для заданного стиля цитирования.
    """
    render_styles_map = {
        CitationEnum.GOST.name: GOSTRenderer,
        CitationEnum.APA.name: APARenderer
    }
    return render_styles_map.get(style)


if __name__ == "__main__":
    try:
        # запуск обработки входного файла
        process_input()
    except Exception as ex:
        logger.error("При обработке команды возникла ошибка: %s", ex)
        raise
