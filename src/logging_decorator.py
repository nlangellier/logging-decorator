import logging
from logging import Logger
from typing import Any, Iterable, List, Optional, Type, Union

Loggers = Union[Logger, Iterable[Logger]]
Levels = Union[int, Iterable[int]]

Argument = Union[Loggers, Levels]
ArgumentClass = Union[Type[Logger], Type[int]]
ArgumentAsList = Union[List[Logger], List[int]]


class LoggerDict(dict):

    def __init__(self,
                 loggers: Optional[Loggers] = None,
                 levels: Optional[Levels] = logging.DEBUG,
                 *args: Any,
                 **kwargs: Any
                 ) -> None:
        super().__init__(*args, **kwargs)

        self.add_loggers(loggers=loggers, levels=levels)

    @staticmethod
    def _parse_argument(argument: Argument,
                        argument_type: ArgumentClass
                        ) -> ArgumentAsList:
        if argument is None:
            argument_list = []
        elif isinstance(argument, argument_type):
            argument_list = [argument]
        elif isinstance(argument, Iterable):
            argument_list = list(argument)
            assert all(isinstance(arg, argument_type) for arg in argument_list)
        else:
            raise TypeError(f'{type(argument)} does not match {argument_type}')
        return argument_list

    def add_loggers(self,
                    loggers: Loggers,
                    levels: Optional[Levels] = logging.DEBUG,
                    ) -> None:
        loggers = self._parse_argument(loggers, argument_type=logging.Logger)
        levels = self._parse_argument(levels, argument_type=int)

        if len(levels) == 1:
            levels = len(loggers) * levels

        error_message = 'loggers and levels must be the same length'
        assert len(loggers) == len(levels), error_message

        for logger, level in zip(loggers, levels):
            self[logger.name] = (logger, level)

    def remove_loggers(self, logger_names: Iterable[str]):
        for logger_name in logger_names:
            self.pop(key=logger_name)
