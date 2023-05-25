from json import JSONDecodeError
import json
import pytest

from utils.services import load_json, date_format, get_last_operations, mask_card_number, sort_by_date


# def test_load_json():
# assert load_json('../json_data_test/correct.json') == []

# with pytest.raises(JSONDecodeError):
# assert load_json('../json_data_test/wrong.json')


def test_load_json_with_valid_file():
    json_data = {"name": "John", "age": 30, "city": "New York"}
    with open("test.json", "w") as f:
        json.dump(json_data, f)
    assert load_json("test.json") == json_data


def test_load_json_with_invalid_file():
    with pytest.raises(FileNotFoundError):
        load_json("nonexistent_file.json")


def test_load_json_with_invalid_json():
    with open("test.json", "w") as f:
        f.write("invalid json")
    with pytest.raises(json.JSONDecodeError):
        load_json("test.json")


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


def test_mask_card_number_with_invalid_input():
    assert mask_card_number("") == "N/A"
    assert mask_card_number("John Doe") == "N/A"
    assert mask_card_number("John Doe 1234 5678 9012") == "N/A"
    assert mask_card_number("John Doe 1234 5678 9012 3456 7890 1234") == "N/A"


def test_sort_by_date():
    # Проверяем, что функция возвращает список
    assert isinstance(sort_by_date([]), list)

    # Проверяем, что функция правильно сортирует список по дате
    input_list = [
        {"date": "2022-01-01", "name": "A"},
        {"date": "2021-12-31", "name": "B"},
        {"date": "2022-01-02", "name": "C"}
    ]
    expected_output = [
        {"date": "2022-01-02", "name": "C"},
        {"date": "2022-01-01", "name": "A"},
        {"date": "2021-12-31", "name": "B"}
    ]
    assert sort_by_date(input_list) == expected_output

    # Проверяем, что функция правильно обрабатывает пустой список
    assert sort_by_date([]) == []
