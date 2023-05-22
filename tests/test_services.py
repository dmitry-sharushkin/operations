from json import JSONDecodeError
import pytest

from utils.services import load_json, date_format, get_last_operations, mask_card_number


def test_load_json():
    assert load_json('json_data_test/correct.json') == []

    with pytest.raises(JSONDecodeError):
        assert load_json('json_data_test/wrong.json')


def test_date_format():
    assert date_format('2022-01-01T12:00:00.000000') == '01.01.2022 12:00:00'
    assert date_format('2022-01-01T12:00:00.000000', '%Y-%m-%d') == '2022-01-01'
    assert date_format('2022-01-01T12:00:00.000000', '%H:%M:%S') == '12:00:00'
    assert date_format('2022-01-01T12:00:00.000000', '%d.%m.%Y %H:%M') == '01.01.2022 12:00'
    with pytest.raises(ValueError):
        date_format('2022-01-01T12:00:00')  # Неправильный формат даты


def test_get_last_operations():
    operations = [
        {"state": "EXECUTED", "name": "operation1"},
        {"state": "PENDING", "name": "operation2"},
        {"state": "EXECUTED", "name": "operation3"},
        {"state": "EXECUTED", "name": "operation4"},
        {"state": "EXECUTED", "name": "operation5"},
        {"state": "FAILED", "name": "operation6"}
    ]

    assert get_last_operations(operations) == [
        {"state": "EXECUTED", "name": "operation1"},
        {"state": "EXECUTED", "name": "operation3"},
        {"state": "EXECUTED", "name": "operation4"},
        {"state": "EXECUTED", "name": "operation5"}
    ]

    assert get_last_operations([]) == []

    assert get_last_operations([
        {"state": "PENDING", "name": "operation1"},
        {"state": "FAILED", "name": "operation2"}
    ]) == []

    assert get_last_operations([
        {"state": "EXECUTED", "name": "operation1"},
        {"state": "EXECUTED", "name": "operation2"}
    ]) == [
               {"state": "EXECUTED", "name": "operation1"},
               {"state": "EXECUTED", "name": "operation2"}
           ]


def test_mask_card_number():
    assert mask_card_number("") == "N/A"
    assert mask_card_number(None) == "N/A"
