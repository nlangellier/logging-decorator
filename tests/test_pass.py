from src.logging_decorator import LoggerDict


def test_logger_dict_subclassing():
    assert issubclass(LoggerDict, dict)
