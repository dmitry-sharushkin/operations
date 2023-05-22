import json
import datetime
import os.path

JSON_DATA_PATH = "../json_data/operations.json"


def load_json(JSON_DATA_PATH):
    """Открывает json-файл"""
    with open(JSON_DATA_PATH, encoding="utf8") as f:
        json_dict = json.load(f)
    return json_dict


def get_last_operations(json_dict):
    operations = [op for op in json_dict if op['state'] == 'EXECUTED']
    last_operations = sorted(operations, key=lambda op: op['date'], reverse=True)[:5]
    return last_operations


def format_operation(operation):
    """
       Форматирует операцию в строку вида:
       <дата перевода> <описание перевода>
       <откуда> -> <куда>
       <сумма перевода> <валюта>
       """
    date = datetime.fromisoformat(operation['date'][:-1]).strftime('%d.%m.%Y')
    description = operation['description']
    from_ = mask_card_number(operation['from'].split()[-1]) if 'card' in operation['from'].lower() else operation[
        'from']
    to = mask_account_number(operation['to'].split()[-1]) if 'счет' in operation['to'].lower() else operation['to']
    amount = float(operation['operationAmount']['amount'])
    currency = operation['operationAmount']['currency']['name']
    return f"{date} {description}\n{from_} -> {to}\n{amount:.2f} {currency}"


def mask_card_number(card_number):
    """
    Заменяет номер карты на маску вида XXXX XX ** XXXX
    """
    return f"{card_number[:6]} XX ** {card_number[-4:]}"


def mask_account_number(account_number):
    """
    Заменяет номер счета на маску вида **XXXX
    """
    return f"**{account_number[-4:]}"


def print_last_operations(data, n=5):
    """
    Выводит на экран список из n последних выполненных операций
    """
    last_operations = get_last_operations(data, n)
    for operation in last_operations:
        print(format_operation(operation))
        print()
