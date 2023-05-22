import json
from datetime import datetime


def load_json(json_data_path):
    """Открывает json-файл"""
    with open(json_data_path, 'r', encoding="utf8") as f:
        json_dict = json.load(f)
    return json_dict


def date_format(data_str: str, formatted_data: str = '%d.%m.%Y %H:%M:%S'):
    """Правильный формат времени"""
    parsed = datetime.strptime(data_str, '%Y-%m-%dT%H:%M:%S.%f')
    formatted_data = parsed.strftime(formatted_data)
    return formatted_data


def get_last_operations(sort_list: list) -> list:
    """Пять последних выполненных операций операций"""
    operations = [op for op in sort_list if op['state'] == 'EXECUTED']
    last_five_operations = operations[:5]
    return last_five_operations


def sort_by_date(json_dict=None):
    """Сортирует список"""
    sort_list = sorted(json_dict, key=lambda x: x.get("date"), reverse=True)
    return sort_list


def mask_card_number(operation_credintials: str) -> str:
    """
    Заменяет номер карты и номер счета на маску
    """
    if operation_credintials:
        credintials_name = " ".join(operation_credintials.split(" ")[:-1])
        credintials_number = operation_credintials.split(" ")[-1]

        if len(credintials_number) == 16:
            number_hide = credintials_number[:6] +  "*" * 6 + credintials_number[:-4]
            number_sep = [number_hide[i:i + 4] for i in range(0, len(credintials_number), 4)]
            return f'{credintials_name} {" ".join(number_sep)}'

        elif len(credintials_number) == 20:
            return f'{credintials_name} {credintials_number.replace(credintials_number[:-4], "**")}'

    return "N/A"


def print_info(operations):
    """Вывод"""
    for op in operations:
        print(f"{date_format(op['date'])} {op['description']}\n"
              f"{mask_card_number(op.get('from'))} -> {mask_card_number(op.get('to'))}\n"
              f"{op['operationAmount']['amount']} {op['operationAmount']['currency']['name']}\n")
