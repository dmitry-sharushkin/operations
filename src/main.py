from utils.services import load_json, get_last_operations, sort_by_date, print_info

json_data_path = "../json_data/operations.json"

if __name__ == '__main__':
    json_dict = load_json(json_data_path)
    sorted_data = sort_by_date(json_dict)
    last_five = get_last_operations(sorted_data)
    print_info(last_five)
