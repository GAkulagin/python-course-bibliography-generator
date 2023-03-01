"""
Базовые функции форматирования списка источников
"""
from typing import Dict
from formatters.styles.base import BaseCitationStyle
from logger import get_logger
from pydantic import BaseModel


logger = get_logger(__name__)


class BaseCitationFormatter:
    """
    Базовый класс для итогового форматирования списка источников.
    """

    formatters_map: Dict[BaseModel, BaseCitationStyle]

    def __init__(self, models: list[BaseModel]) -> None:
        """
        Конструктор.

        :param models: Список моделей для итогового форматирования
        """

        self.formatted_items = []
        for model in models:
            self.formatted_items.append(self.formatters_map.get(type(model))(model))  # type: ignore

    def format(self) -> list[BaseCitationStyle]:
        """
        Форматирование списка источников.

        :return:
        """

        logger.info("Общее форматирование ...")

        return sorted(self.formatted_items, key=lambda item: item.formatted)
